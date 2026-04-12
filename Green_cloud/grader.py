from math import isfinite

# TIGHTER EPS for validator safety
EPS = 5e-5  # Even safer than 1e-4


def strict_score(value: float) -> float:
    """Guaranteed (EPS, 1-EPS) output for ANY input."""
    try:
        x = float(value)
    except (TypeError, ValueError):
        return 0.5

    if not isfinite(x):
        return 0.5

    # CLAMP EVERYTHING to strict open interval
    if x <= 0.0:
        return EPS
    if x >= 1.0:
        return 1.0 - EPS
    return max(EPS, min(1.0 - EPS, x))


def _get_attr(obj, name, default=None):
    if obj is None:
        return default
    return getattr(obj, name, default)


def _get_jobs(obj):
    jobs = _get_attr(obj, "jobs", [])
    return jobs if jobs is not None else []


def easy(env=None, observation=None, **kwargs) -> float:
    """Easy: % jobs assigned. Never 0.0 or 1.0."""
    obj = env if env is not None else observation
    jobs = _get_jobs(obj)

    total_jobs = len(jobs)
    if total_jobs <= 0:
        return 0.1  # Safe minimum

    assigned = sum(1 for j in jobs if _get_attr(j, "assigned", False))
    raw_ratio = assigned / total_jobs
    return round(strict_score(raw_ratio), 6)


def medium(env=None, observation=None, **kwargs) -> float:
    """Medium: % jobs assigned before deadline. Never 0.0 or 1.0."""
    obj = env if env is not None else observation
    jobs = _get_jobs(obj)
    current_time = _get_attr(obj, "time", 0)

    total_jobs = len(jobs)
    if total_jobs <= 0:
        return 0.1  # Safe minimum

    success = sum(
        1
        for j in jobs
        if _get_attr(j, "assigned", False)
        and current_time <= _get_attr(j, "deadline", current_time)
    )

    raw_ratio = success / total_jobs
    return round(strict_score(raw_ratio), 6)


def hard(env=None, observation=None, **kwargs) -> float:
    """Hard: 60% completion + 40% carbon optimization. Never 0.0 or 1.0."""
    obj = env if env is not None else observation
    jobs = _get_jobs(obj)
    regions = _get_attr(obj, "regions", [])
    energy_sources = _get_attr(obj, "energy_sources", {})

    total_jobs = len(jobs)
    if total_jobs <= 0:
        return 0.1  # Safe minimum

    success_count = 0
    total_carbon = 0.0

    for j in jobs:
        if not _get_attr(j, "assigned", False):
            continue

        assigned_region = _get_attr(j, "assigned_region", None)
        if not assigned_region:
            continue

        region = next(
            (r for r in regions if _get_attr(r, "name", None) == assigned_region),
            None
        )
        if region is None:
            continue

        energy_mix = _get_attr(region, "energy_mix", {}) or {}
        carbon = 0.0

        for source_name, ratio in energy_mix.items():
            source = energy_sources.get(source_name)
            if source is None:
                continue
            carbon += _get_attr(source, "carbon_intensity", 0.0) * float(ratio)

        success_count += 1
        total_carbon += carbon

    # Safe completion score
    completion_raw = success_count / total_jobs
    completion_score = strict_score(completion_raw)

    # Safe carbon score  
    if success_count == 0:
        carbon_score = EPS
    else:
        avg_carbon = total_carbon / success_count
        carbon_raw = 1.0 - avg_carbon
        carbon_score = strict_score(carbon_raw)

    # Weighted combination, then final clamp
    weighted = 0.6 * completion_score + 0.4 * carbon_score
    return round(strict_score(weighted), 6)


# Direct exports matching openenv.yaml graders
GRADERS = {
    "easy": easy,
    "medium": medium,
    "hard": hard,
}
