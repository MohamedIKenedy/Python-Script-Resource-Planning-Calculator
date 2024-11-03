import openpyxl
from openpyxl import Workbook

class Stage:
    def __init__(self, name, headcount, lead_time, qa_rate=1.0):
        self.name = name
        self.headcount = headcount
        self.lead_time = lead_time  # minutes per task
        self.qa_rate = qa_rate      # QA rate (default: 100% move to next stage)
        self.tasks = 0
        self.completed_tasks = 0

    def work_one_day(self, work_minutes=390):
        tasks_per_worker_per_day = work_minutes / self.lead_time
        total_tasks_completed = min(self.tasks, self.headcount * tasks_per_worker_per_day)
        tasks_for_next_stage = total_tasks_completed * self.qa_rate

        self.tasks -= total_tasks_completed
        self.completed_tasks += total_tasks_completed
        return tasks_for_next_stage

    def add_tasks(self, tasks):
        self.tasks += tasks


class Pipeline:
    def __init__(self, stages):
        self.stages = stages
        self.days_passed = 0
        self.total_work_minutes = 0
        self.daily_data = []

    def work_one_day(self):
        for i in range(len(self.stages)):
            completed_tasks = self.stages[i].work_one_day()
            if i < len(self.stages) - 1:
                self.stages[i + 1].add_tasks(completed_tasks)
        self.days_passed += 1
        self.total_work_minutes += 390  # add daily work minutes (6.5 hours per day)
        self.daily_data.append(self.collect_daily_data())

    def is_complete(self):
        return all(stage.tasks == 0 for stage in self.stages)

    def remaining_time(self):
        total_time_left = 0
        work_minutes_per_day = 390

        for stage in self.stages:
            if stage.tasks > 0:
                tasks_per_worker_per_day = work_minutes_per_day / stage.lead_time
                total_days = stage.tasks / (stage.headcount * tasks_per_worker_per_day)
                total_time_left += total_days

        days = int(total_time_left)
        hours = (total_time_left - days) * 24
        minutes = (hours - int(hours)) * 60
        return f"{days}d:{int(hours)}h:{int(minutes)}m"

    def total_time_taken(self):
        work_minutes_per_day = 390
        total_minutes = self.days_passed * work_minutes_per_day

        days = total_minutes // (24 * 60)
        hours = (total_minutes % (24 * 60)) // 60
        minutes = total_minutes % 60
        return f"{days}d:{hours}h:{minutes}m"

    def total_work_hours_only(self):
        hours = self.total_work_minutes // 60
        minutes = self.total_work_minutes % 60
        return f"{hours}h:{minutes}m"

    def collect_daily_data(self):
        return {
            "day": self.days_passed,
            "tasks_l0": self.stages[0].tasks,
            "completed_l0": self.stages[0].completed_tasks,
            "tasks_l1": self.stages[1].tasks,
            "completed_l1": self.stages[1].completed_tasks,
            "tasks_l2": self.stages[2].tasks,
            "completed_l2": self.stages[2].completed_tasks,
            "remaining_time": self.remaining_time(),
            "total_time_taken": self.total_time_taken()
        }

    def save_to_excel(self, filename="project_progress.xlsx"):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Project Progress"

        # Define the headers based on the format from the image and your provided output
        headers = [
            "Day", "Tasks L0", "Completed L0", "Lead Time L0", "HC L0",
            "Tasks L1", "Completed L1", "Lead Time L1", "HC L1",
            "Tasks L2", "Completed L2", "Lead Time L2", "HC L2",
            "Remaining Tasks", "Remaining Time", "Total Time Taken So Far"
        ]
        sheet.append(headers)

        # Fill in data for each workday
        for data in self.daily_data:
            row_data = [
                data["day"],  # Day number
                f"{data['tasks_l0']:.2f}",  # Tasks remaining in L0
                f"{data['completed_l0']:.2f}",  # Completed tasks in L0
                self.stages[0].lead_time,  # Lead Time for L0
                self.stages[0].headcount,  # Headcount for L0
                f"{data['tasks_l1']:.2f}",  # Tasks remaining in L1
                f"{data['completed_l1']:.2f}",  # Completed tasks in L1
                self.stages[1].lead_time,  # Lead Time for L1
                self.stages[1].headcount,  # Headcount for L1
                f"{data['tasks_l2']:.2f}",  # Tasks remaining in L2
                f"{data['completed_l2']:.2f}",  # Completed tasks in L2
                self.stages[2].lead_time,  # Lead Time for L2
                self.stages[2].headcount,  # Headcount for L2
                f"{data['tasks_l0'] + data['tasks_l1'] + data['tasks_l2']:.2f}",  # Total remaining tasks
                data["remaining_time"],  # Remaining time for the project
                data["total_time_taken"]  # Total time taken so far
            ]

            # Append row to the sheet
            sheet.append(row_data)

        # Add total time taken and total work hours at the end
        sheet.append(["", "", "", "", "", "", "", "", "", "", "", "", "", "Total Time Taken (Days):", self.total_time_taken()])
        sheet.append(["", "", "", "", "", "", "", "", "", "", "", "", "", "Total Work Time (Hours Only):", self.total_work_hours_only()])

        workbook.save(filename)


# Example usage of the classes:
if __name__ == "__main__":
    stage_l0 = Stage(name="L0", headcount=40, lead_time=30, qa_rate=0.8)
    stage_l1 = Stage(name="L1", headcount=10, lead_time=45)
    stage_l2 = Stage(name="L2", headcount=5, lead_time=60)

    stage_l0.add_tasks(100)
    pipeline = Pipeline(stages=[stage_l0, stage_l1, stage_l2])

    while not pipeline.is_complete():
        print(f"--- Day {pipeline.days_passed} ---")
        print(f"L0: {stage_l0.tasks:.2f} tasks remaining, {stage_l0.completed_tasks:.2f} tasks completed")
        print(f"L1: {stage_l1.tasks:.2f} tasks remaining, {stage_l1.completed_tasks:.2f} tasks completed")
        print(f"L2: {stage_l2.tasks:.2f} tasks remaining, {stage_l2.completed_tasks:.2f} tasks completed")
        print(f"Estimated remaining time: {pipeline.remaining_time()}\n")
        pipeline.work_one_day()

    print("All tasks have been completed!")
    print(f"Total Time Taken: {pipeline.total_time_taken()}")
    print(f"Total Work Time (Hours Only): {pipeline.total_work_hours_only()}")
    pipeline.save_to_excel("project1_progress.xlsx")