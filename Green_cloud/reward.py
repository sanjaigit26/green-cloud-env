def calculate_reward(job, region, energy_sources, current_time):
    carbon = 0.0
    cost = 0.0
    for source, ratio in region.energy_mix.items():
        energy = energy_sources[source]
        carbon += energy.carbon_intensity * ratio
        cost   += energy.cost * ratio
    carbon_score  = max(0.21, min(0.79, 1 - carbon))
    cost_score    = max(0.21, min(0.79, 1 - (cost / 3)))
    if current_time <= job.deadline:
        deadline_score = 0.75
    else:
        delay = current_time - job.deadline
        deadline_score = max(0.21, 1 - 0.2 * delay)
    reward = (
        0.5 * carbon_score +
        0.3 * cost_score +
        0.2 * deadline_score
    )
    return max(0.21, min(0.79, reward))
