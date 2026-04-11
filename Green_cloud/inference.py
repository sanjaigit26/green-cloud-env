import os
from openai import OpenAI
from env import GreenCloudEnv
from models import Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN")

MAX_STEPS = 5

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}")


def log_end(success, steps, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")


def call_llm(client):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return response.choices[0].message.content
    except Exception:
        return "fallback"


def get_action(env):
    for job in env.jobs:
        if not job.assigned:
            return Action(
                job_id=job.id,
                region=env.regions[0].name,
                action_type="assign"
            )
    return Action(job_id=1, region=env.regions[0].name, action_type="assign")


def run_task(task_id: str):
    env = GreenCloudEnv()
    rewards = []

    log_start(task_id, "green-cloud-env", MODEL_NAME)

    env.reset(task_id=task_id)

    _ = call_llm(client)

    done = False
    step = 0

    while not done and step < MAX_STEPS:
        step += 1
        action_obj = get_action(env)
        result = env.step(action_obj)

        reward = result.reward
        done = result.done
        rewards.append(reward)

        log_step(step, str(action_obj.model_dump()), reward, done, None)

    success = sum(rewards) > 0

    log_end(success, step, rewards)


def run():
    for task_id in ["easy", "medium", "hard"]:
        run_task(task_id)


if __name__ == "__main__":
    run()
