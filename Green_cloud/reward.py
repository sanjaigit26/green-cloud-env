def calculate_reward(job, region, energy_sources, current_time):
    carbon = 0
    cost = 0

    # 🔹 Compute weighted carbon & cost
    for source, ratio in region.energy_mix.items():
        energy = energy_sources[source]
        carbon += energy.carbon_intensity * ratio
        cost += energy.cost * ratio

    # 🔹 Normalize values
    carbon_score = 1 - carbon          # lower carbon = better
    cost_score = 1 - (cost / 3)        # normalize cost

    # 🔹 Deadline score
    if current_time <= job.deadline:
        deadline_score = 1.0
    else:
        delay = current_time - job.deadline
        deadline_score = max(0, 1 - 0.2 * delay)

    # 🔹 Final weighted reward
    reward = (
        0.5 * carbon_score +
        0.3 * cost_score +
        0.2 * deadline_score
    )

    return max(min(reward, 1.0), 0.0)