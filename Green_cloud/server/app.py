from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import GreenCloudEnv
from models import Action
from grader import GRADERS
import uvicorn

app = FastAPI()
env = GreenCloudEnv()

class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"

# ✅ Homepage
@app.get("/")
def home():
    return {"status": "ok"}

# 🔁 Reset - supports GET (query param) and POST (JSON body)
@app.get("/reset")
def reset_get(task_id: str = "easy"):
    obs = env.reset(task_id=task_id)
    return obs.model_dump()

@app.post("/reset")
def reset_post(body: ResetRequest = None):
    task_id = body.task_id if body else "easy"
    obs = env.reset(task_id=task_id)
    return obs.model_dump()

# ⚙️ Step Endpoint
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

# 📊 Grade Endpoint
@app.get("/grade")
@app.post("/grade")
def grade():
    scores = {}
    for task_name, grader_fn in GRADERS.items():
        # Reset env for this task
        env.reset(task_id=task_name)

        # ✅ Auto-assign all jobs to lowest-carbon region before grading
        for job in env.jobs:
            best_region = min(
                env.regions,
                key=lambda r: sum(
                    env.energy_sources[s].carbon_intensity * ratio
                    for s, ratio in r.energy_mix.items()
                )
            )
            env.step(Action(
                job_id=job.id,
                region=best_region.name,
                action_type="assign"
            ))

        scores[task_name] = grader_fn(env)

    return scores

# 🚀 Main Entry
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
