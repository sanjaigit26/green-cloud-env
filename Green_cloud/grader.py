from math import isfinite

def clamp(value: float) -> float:
    return max(0.01, min(0.99, float(value)))

def strict_score(value: float) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return 0.5
    if not isfinite(x):
        return 0.5
    return clamp(x)

def easy(env=None, observation=None, **kwargs) -> float:
    obj = env if env is not None else observation
    jobs = getattr(obj, "jobs", []) or []
    total_jobs = len(jobs)
    if total_jobs <= 0:
        return 0.5
    assigned = sum(1 for j in jobs if getattr(j, "assigned", False))
    score = round(strict_score(assigned / total_jobs), 6)
    return max(0.001, min(0.999, score))

def medium(env=None, observation=None, **kwargs) -> float:
    obj = env if env is not None else observation
    jobs = getattr(obj, "jobs", []) or []
    current_time = getattr(obj, "time", 0)
    total_jobs = len(jobs)
    if total_jobs <= 0:
        return 0.5
    success = sum(
        1 for j in jobs
        if getattr(j, "assigned", False)
        and current_time <= getattr(j, "deadline", current_time)
    )
    score = round(strict_score(success / total_jobs), 6)
    return max(0.001, min(0.999, score))

def hard(env=None, observation=None, **kwargs) -> float:
    obj = env if env is not None else observation
    jobs = getattr(obj, "jobs", []) or []
    regions = getattr(obj, "regions", []) or []
    energy_sources = getattr(obj, "energy_sources", {}) or {}
    total_jobs = len(jobs)
    if total_jobs <= 0:
        return 0.5
    success_count = 0
    total_carbon = 0.0
    for j in jobs:
        if not getattr(j, "assigned", False):
            continue
        assigned_region = getattr(j, "assigned_region", None)
        if not assigned_region:
            continue
        region = next(
            (r for r in regions if getattr(r, "name", None) == assigned_region),
            None
        )
        if region is None:
            continue
        energy_mix = getattr(region, "energy_mix", {}) or {}
        carbon = 0.0
        for source_name, ratio in energy_mix.items():
            source = energy_sources.get(source_name)
            if source is None:
                continue
            carbon += getattr(source, "carbon_intensity", 0.0) * float(ratio)
        success_count += 1
        total_carbon += carbon
    completion_score = strict_score(success_count / total_jobs)
    if success_count == 0:
        carbon_score = 0.5
    else:
        avg_carbon = total_carbon / success_count
        carbon_score = strict_score(1.0 - avg_carbon)
    weighted = 0.6 * completion_score + 0.4 * carbon_score
    score = round(strict_score(weighted), 6)
    return max(0.001, min(0.999, score))

GRADERS = {
    "easy":   easy,
    "medium": medium,
    "hard":   hard,
}
