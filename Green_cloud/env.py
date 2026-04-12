from typing import Dict
from models import Observation, Action, StepResult, Job, Region, EnergySource
from reward import calculate_reward
from tasks import TASKS

def clamp(value: float) -> float:
    return max(0.1, min(0.9, float(value)))

class GreenCloudEnv:
    def __init__(self):
        self.time = 0
        self.max_time = 10
        self.jobs = []
        self.regions = []
        self.energy_sources: Dict[str, EnergySource] = {}
        self.current_task_id = "easy"
        self.current_task = TASKS["easy"]

    def reset(self, task_id: str = "easy") -> Observation:
        self.time = 0
        if task_id not in TASKS:
            task_id = "easy"
        self.current_task_id = task_id
        self.current_task = TASKS[task_id]

        self.energy_sources = {
            "solar": EnergySource(name="solar", carbon_intensity=0.1, cost=2.0, availability=0.8),
            "wind":  EnergySource(name="wind",  carbon_intensity=0.2, cost=1.5, availability=0.7),
            "coal":  EnergySource(name="coal",  carbon_intensity=0.9, cost=1.0, availability=1.0),
        }
        self.regions = [
            Region(name="us-east",    capacity=100, energy_mix={"solar": 0.5, "coal": 0.5}),
            Region(name="eu-west",    capacity=80,  energy_mix={"wind": 0.6, "coal": 0.4}),
            Region(name="asia-south", capacity=120, energy_mix={"solar": 0.3, "wind": 0.3, "coal": 0.4}),
        ]
        self.jobs = [
            Job(id=1, compute_required=30, deadline=5),
            Job(id=2, compute_required=40, deadline=7),
            Job(id=3, compute_required=20, deadline=4),
        ]
        return self._get_observation(reward=0.5, done=False)

    def step(self, action: Action) -> StepResult:
        reward = 0.5
        done = False

        job    = next((j for j in self.jobs    if j.id   == action.job_id), None)
        region = next((r for r in self.regions if r.name == action.region),  None)

        if job and region and action.action_type == "assign" and not job.assigned:
            job.assigned = True
            job.assigned_region = region.name
            reward = clamp(calculate_reward(job, region, self.energy_sources, self.time))

        self.time += 1

        if self.time >= self.max_time or all(j.assigned for j in self.jobs):
            done = True

        if done:
            reward = clamp(self.current_task["grader"](self))

        return StepResult(
            observation=self._get_observation(reward=reward, done=done),
            reward=reward,
            done=done,
            info={"task_id": self.current_task_id}
        )

    def state(self):
        return {
            "time": self.time,
            "task_id": self.current_task_id,
            "jobs": [j.dict() for j in self.jobs],
        }

    def _get_observation(self, reward: float = 0.5, done: bool = False) -> Observation:
        return Observation(
            time=self.time,
            jobs=self.jobs,
            regions=self.regions,
            energy_sources=self.energy_sources,
            reward=reward,
            done=done
        )
