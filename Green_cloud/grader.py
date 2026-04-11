def grade_easy(env):
    total_jobs = len(env.jobs)
    assigned_jobs = sum(1 for j in env.jobs if j.assigned)

    score = assigned_jobs / total_jobs if total_jobs > 0 else 0.0
    score = max(min(score, 0.99), 0.01)
    return round(score, 2)


def grade_medium(env):
    total_jobs = len(env.jobs)
    success = 0

    for j in env.jobs:
        if j.assigned and env.time <= j.deadline:
            success += 1

    score = success / total_jobs if total_jobs > 0 else 0.0
    score = max(min(score, 0.99), 0.01)
    return round(score, 2)


def grade_hard(env):
    total_jobs = len(env.jobs)
    success = 0
    total_carbon = 0

    for j in env.jobs:
        if j.assigned:
            success += 1
            region = next(r for r in env.regions if r.name == j.assigned_region)

            carbon = 0
            for source, ratio in region.energy_mix.items():
                energy = env.energy_sources[source]
                carbon += energy.carbon_intensity * ratio

            total_carbon += carbon

    if total_jobs == 0:
        return 0.01

    completion_score = success / total_jobs
    avg_carbon = total_carbon / max(success, 1)
    carbon_score = 1 - avg_carbon

    final_score = (0.6 * completion_score) + (0.4 * carbon_score)
    final_score = max(min(final_score, 0.99), 0.01)

    return round(final_score, 2)


GRADERS = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard
}
