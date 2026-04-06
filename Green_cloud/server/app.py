from fastapi import FastAPI
from env import GreenCloudEnv
from models import Action
import uvicorn

app = FastAPI()
env = GreenCloudEnv()


# ✅ Homepage (NEW)
@app.get("/")
def home():
    return {"status": "Green Cloud Env Running "}


# 🔁 Reset Endpoint
@app.get("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


# ⚙️ Step Endpoint
@app.post("/step")
def step(action: dict):
    act = Action(**action)
    result = env.step(act)
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }


# 🚀 Main Entry (REQUIRED)
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


# 🔥 Entry Point
if __name__ == "__main__":
    main()