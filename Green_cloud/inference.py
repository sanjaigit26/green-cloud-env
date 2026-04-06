import os
from openai import OpenAI
from env import GreenCloudEnv
from models import Action

# ✅ REQUIRED ENV VARIABLES (correct format)
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

MAX_STEPS = 5

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}")


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


def get_action(env):
    # simple baseline: assign first unassigned job
    for job in env.jobs:
        if not job.assigned:
            return Action(
                job_id=job.id,
                region=env.regions[0].name,
                action_type="assign"
            )
    return Action(job_id=1, region=env.regions[0].name, action_type="assign")


def run():
    env = GreenCloudEnv()
    rewards = []

    log_start("green-cloud-task", "green-cloud-env", MODEL_NAME)

    env.reset()
    done = False
    step = 0

    while not done and step < MAX_STEPS:
        step += 1

        action_obj = get_action(env)
        result = env.step(action_obj)

        reward = result.reward
        done = result.done

        rewards.append(reward)

        log_step(
            step,
            str(action_obj.model_dump()),
            reward,
            done,
            None
        )

    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = score > 0.3

    log_end(success, step, score, rewards)


if __name__ == "__main__":
    run()
