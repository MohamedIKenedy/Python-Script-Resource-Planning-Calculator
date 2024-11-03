import time
import random

def dynamic_task_arrival(pipeline, interval=3, max_tasks=20):
    """Dynamically add tasks to L0 at random intervals."""
    while not pipeline.is_complete():
        num_tasks = random.randint(1, max_tasks)
        print(f"New tasks arriving: {num_tasks} tasks added to L0.")
        pipeline.stages[0].add_tasks(num_tasks)
        time.sleep(interval)
