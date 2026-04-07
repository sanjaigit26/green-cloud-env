from fastapi import FastAPI
from env import GreenCloudEnv
from models import Action
import uvicorn

app = FastAPI()
env = GreenCloudEnv()


# ✅ Homepage
@app.get("/")
def home():
    return {"status": "ok"}


# 🔁 Reset Endpoint (FIXED: supports GET + POST)
@app.get("/reset")
@app.post("/reset")
def reset():
    obs = env.reset()
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


# 🚀 Main Entry
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# 🔥 Entry Point
if __name__ == "__main__":
    main()
