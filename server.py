from fastapi import FastAPI
import random
import time

app = FastAPI()

# Configurable random delay time for server to complete a job
delay_time = random.randint(5, 20)  # in seconds
start_time = time.time()


@app.get("/status")
async def get_status():
    """
    Simulates a server endpoint that returns the status of a video translation job.

    Returns:
        dict: A dictionary containing the status of the job, which can be "pending", "completed", or "error".
    """
    elapsed_time = time.time() - start_time
    if elapsed_time < delay_time:
        return {"result": "pending"}
    elif random.random() < 0.1:  # 10% chance of error
        return {"result": "error"}
    else:
        return {"result": "completed"}
