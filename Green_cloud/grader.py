EPS = 1e-4

def safe_score(score: float) -> float:
    return max(EPS, min(1.0 - EPS, float(score)))

def grade_easy(env) -> float:
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return EPS
    assigned = sum(1 for j in env.jobs if j.assigned)
    return safe_score(assigned / total_jobs)

def grade_medium(env) -> float:
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return EPS
    success = sum(
        1 for j in env.jobs
        if j.assigned and env.time <= j.deadline
    )
    return safe_score(success / total_jobs)

def grade_hard(env) -> float:
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return EPS
    success = 0
    total_carbon = 0.0
    for j in env.jobs:
        if j.assigned:
            success += 1
            region = next(r for r in env.regions if r.name == j.assigned_region)
            carbon = sum(
                env.energy_sources[s].carbon_intensity * ratio
                for s, ratio in region.energy_mix.items()
            )
            total_carbon += carbon
    completion_score = success / total_jobs
    avg_carbon = total_carbon / max(success, 1)
    carbon_score = max(0.0, min(1.0, 1.0 - avg_carbon))
    final_score = (0.6 * completion_score) + (0.4 * carbon_score)
    return safe_score(final_score)

GRADERS = {
    "easy":   grade_easy,
    "medium": grade_medium,
    "hard":   grade_hard,
}
