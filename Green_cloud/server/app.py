from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import GreenCloudEnv
from models import Action
from grader import GRADERS
import uvicorn

app = FastAPI()
env = GreenCloudEnv()

EPS = 1e-4

def clamp(value: float) -> float:
    return max(EPS, min(1.0 - EPS, float(value)))

def run_and_grade(task_name: str) -> float:
    env.reset(task_id=task_name)
    for job in env.jobs:
        best_region = min(
            env.regions,
            key=lambda r: sum(
                env.energy_sources[s].carbon_intensity * ratio
                for s, ratio in r.energy_mix.items()
            )
        )
        env.step(Action(job_id=job.id, region=best_region.name, action_type="assign"))
    return clamp(GRADERS[task_name](env))

class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/reset")
def reset_get(task_id: str = "easy"):
    obs = env.reset(task_id=task_id)
    return obs.model_dump()

@app.post("/reset")
def reset_post(body: ResetRequest = None):
    task_id = body.task_id if body else "easy"
    obs = env.reset(task_id=task_id)
    return obs.model_dump()

@app.post("/step")
def step(action: dict):
    act = Action(**action)
    result = env.step(act)
    return {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }

@app.get("/grade")
@app.post("/grade")
def grade():
    return {
        "easy":   run_and_grade("easy"),
        "medium": run_and_grade("medium"),
        "hard":   run_and_grade("hard")
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
