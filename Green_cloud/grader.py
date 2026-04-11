EPS = 1e-6  # much smaller buffer — keeps score well inside (0,1)

def safe_score(score):
    if score <= 0.0:
        return EPS
    if score >= 1.0:
        return 1.0 - EPS
    return float(score)

def grade_easy(env):
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return EPS
    assigned_jobs = sum(1 for j in env.jobs if j.assigned)
    score = assigned_jobs / total_jobs
    return safe_score(score)

def grade_medium(env):
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return EPS
    success = sum(
        1 for j in env.jobs
        if j.assigned and env.time <= j.deadline
    )
    score = success / total_jobs
    return safe_score(score)

def grade_hard(env):
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
                env.energy_sources[source].carbon_intensity * ratio
                for source, ratio in region.energy_mix.items()
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
