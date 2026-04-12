# grader.py - complete fixed file

EPS = 0.1  # ✅ meaningful minimum, not near-zero

def safe_score(score: float) -> float:
    return max(0.1, min(0.9, float(score)))  # strictly inside (0,1) with big margin

def grade_easy(env) -> float:
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return 0.1
    assigned = sum(1 for j in env.jobs if j.assigned)
    raw = assigned / total_jobs
    # Map 0→0.1, 1→0.9
    mapped = 0.1 + (raw * 0.8)
    return round(mapped, 6)

def grade_medium(env) -> float:
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return 0.1
    success = sum(
        1 for j in env.jobs
        if j.assigned and env.time <= j.deadline
    )
    raw = success / total_jobs
    mapped = 0.1 + (raw * 0.8)
    return round(mapped, 6)

def grade_hard(env) -> float:
    total_jobs = len(env.jobs)
    if total_jobs == 0:
        return 0.1
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
    # Map 0→0.1, 1→0.9
    mapped = 0.1 + (final_score * 0.8)
    return round(mapped, 6)

GRADERS = {
    "easy":   grade_easy,
    "medium": grade_medium,
    "hard":   grade_hard,
}
