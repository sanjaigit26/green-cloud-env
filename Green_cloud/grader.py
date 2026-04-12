from math import isfinite

def _safe(value: float) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return 0.5
    if not isfinite(x):
        return 0.5
    if x <= 0.0:
        return 0.21
    if x >= 1.0:
        return 0.79
    if x < 0.21:
        return 0.21
    if x > 0.79:
        return 0.79
    return round(x, 4)

def easy(env=None, observation=None, **kwargs) -> float:
    try:
        obj = env if env is not None else observation
        jobs = getattr(obj, "jobs", None) or []
        total_jobs = len(jobs)
        if total_jobs <= 0:
            return 0.5
        assigned = sum(1 for j in jobs if getattr(j, "assigned", False))
        raw = assigned / total_jobs
        return _safe(0.21 + raw * 0.58)
    except Exception:
        return 0.5

def medium(env=None, observation=None, **kwargs) -> float:
    try:
        obj = env if env is not None else observation
        jobs = getattr(obj, "jobs", None) or []
        current_time = getattr(obj, "time", 0)
        total_jobs = len(jobs)
        if total_jobs <= 0:
            return 0.5
        success = sum(
            1 for j in jobs
            if getattr(j, "assigned", False)
            and current_time <= getattr(j, "deadline", current_time)
        )
        raw = success / total_jobs
        return _safe(0.21 + raw * 0.58)
    except Exception:
        return 0.5

def hard(env=None, observation=None, **kwargs) -> float:
    try:
        obj = env if env is not None else observation
        jobs = getattr(obj, "jobs", None) or []
        regions = getattr(obj, "regions", None) or []
        energy_sources = getattr(obj, "energy_sources", None) or {}
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
        completion = _safe(0.21 + (success_count / total_jobs) * 0.58)
        if success_count == 0:
            carbon = 0.5
        else:
            avg_carbon = total_carbon / success_count
            carbon = _safe(0.21 + (1.0 - avg_carbon) * 0.58)
        return _safe(0.6 * completion + 0.4 * carbon)
    except Exception:
        return 0.5

GRADERS = {
    "easy":   easy,
    "medium": medium,
    "hard":   hard,
}
