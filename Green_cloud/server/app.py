from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import GreenCloudEnv
from models import Action
from grader import GRADERS
import uvicorn

app = FastAPI()
env = GreenCloudEnv()

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
    score = GRADERS[task_name](env)
    return max(0.001, min(0.999, float(score)))

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
    obs = result.observation.model_dump()
    obs["reward"] = result.reward
    obs["done"] = result.done
    return {
        "observation": obs,
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }

@app.get("/grade")
@app.post("/grade")
def grade():
    scores = {
        "easy":   run_and_grade("easy"),
        "medium": run_and_grade("medium"),
        "hard":   run_and_grade("hard")
    }
    return {k: max(0.001, min(0.999, float(v))) for k, v in scores.items()}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
