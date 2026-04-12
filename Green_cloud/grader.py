from math import isfinite

EPS = 1e-4


def strict_score(value: float) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return 0.5

    if not isfinite(x):
        return 0.5

    if x <= 0.0:
        return EPS
    if x >= 1.0:
        return 1.0 - EPS
    return max(EPS, min(1.0 - EPS, x))


def easy(env) -> float:
    total_jobs = len(getattr(env, "jobs", []))
    if total_jobs <= 0:
        return 0.1

    assigned = sum(1 for j in env.jobs if getattr(j, "assigned", False))
    raw_score = assigned / total_jobs
    return round(strict_score(raw_score), 6)


def medium(env) -> float:
    total_jobs = len(getattr(env, "jobs", []))
    if total_jobs <= 0:
        return 0.1

    current_time = getattr(env, "time", 0)

    success = sum(
        1
        for j in env.jobs
        if getattr(j, "assigned", False)
        and current_time <= getattr(j, "deadline", current_time)
    )

    raw_score = success / total_jobs
    return round(strict_score(raw_score), 6)


def hard(env) -> float:
    total_jobs = len(getattr(env, "jobs", []))
    if total_jobs <= 0:
        return 0.1

    success = 0
    total_carbon = 0.0

    for j in env.jobs:
        if not getattr(j, "assigned", False):
            continue

        assigned_region = getattr(j, "assigned_region", None)
        if not assigned_region:
            continue

        region = next(
            (r for r in getattr(env, "regions", []) if getattr(r, "name", None) == assigned_region),
            None
        )
        if region is None:
            continue

        energy_mix = getattr(region, "energy_mix", {}) or {}
        carbon = 0.0

        for source_name, ratio in energy_mix.items():
            source = getattr(env, "energy_sources", {}).get(source_name)
            if source is None:
                continue
            carbon += getattr(source, "carbon_intensity", 0.0) * float(ratio)

        success += 1
        total_carbon += carbon

    completion_score = strict_score(success / total_jobs)

    if success == 0:
        carbon_score = EPS
    else:
        avg_carbon = total_carbon / success
        carbon_score = strict_score(1.0 - avg_carbon)

    final_score = (0.6 * completion_score) + (0.4 * carbon_score)
    return round(strict_score(final_score), 6)


GRADERS = {
    "easy": easy,
    "medium": medium,
    "hard": hard,
}
