from src.pipeline import Stage, Pipeline

def get_user_input():
    stages = []
    num_stages = int(input("Enter the number of stages: "))

    for i in range(num_stages):
        name = input(f"Enter the name for stage {i+1}: ")
        headcount = int(input(f"Enter the headcount for stage {i+1}: "))
        lead_time = float(input(f"Enter the lead time (minutes per task) for stage {i+1}: "))
        qa_rate = float(input(f"Enter the QA rate for stage {i+1} (default is 1.0): ") or 1.0)
        stage = Stage(name=name, headcount=headcount, lead_time=lead_time, qa_rate=qa_rate)
        stages.append(stage)

    initial_tasks = int(input("Enter the initial number of tasks for the first stage: "))
    stages[0].add_tasks(initial_tasks)

    return stages

def main():
    stages = get_user_input()
    pipeline = Pipeline(stages=stages)

    while not pipeline.is_complete():
        print(f"--- Day {pipeline.days_passed} ---")
        for i, stage in enumerate(pipeline.stages):
            print(f"{stage.name}: {stage.tasks:.2f} tasks remaining, {stage.completed_tasks:.2f} tasks completed")
        print(f"Estimated remaining time: {pipeline.remaining_time()}\n")
        pipeline.work_one_day()

    print("All tasks have been completed!")
    print(f"Total Time Taken: {pipeline.total_time_taken()}")
    print(f"Total Work Time (Hours Only): {pipeline.total_work_hours_only()}")
    pipeline.save_to_excel("project_progress.xlsx")

if __name__ == "__main__":
    main()