import unittest
from src.pipeline import Stage, Pipeline

class TestPipeline(unittest.TestCase):

    def test_stage_working(self):
        """Test that tasks in a stage are completed according to headcount and lead time."""
        L0 = Stage("L0", headcount=5, lead_time=60)  # 1 task per person per hour (60 minutes per task)
        L0.add_tasks(25)

        L0.work_one_hour()  # Simulate one day (6.5 hours)
        self.assertEqual(L0.tasks, 0)
        self.assertEqual(L0.completed_tasks, 25)

    def test_task_movement_between_stages(self):
        """Test task movement from L0 to L1 with a QA rate."""
        L0 = Stage("L0", headcount=5, lead_time=60, qa_rate=0.8)  # 80% QA rate
        L1 = Stage("L1", headcount=2, lead_time=60)
        
        L0.add_tasks(25)

        pipeline = Pipeline([L0, L1])
        pipeline.work_one_day()  # Work one day in the pipeline

        # After L0, only 80% of tasks should move to L1
        self.assertEqual(L0.tasks, 0)
        self.assertEqual(L0.completed_tasks, 25)
        self.assertEqual(L1.tasks, 20)

    def test_remaining_time_estimation(self):
        """Test that the remaining time calculation is correct."""
        L0 = Stage("L0", headcount=10, lead_time=60)  # 10 tasks per day
        L1 = Stage("L1", headcount=5, lead_time=60)
        L2 = Stage("L2", headcount=2, lead_time=60)

        L0.add_tasks(50)  # Total 50 tasks

        pipeline = Pipeline([L0, L1, L2])

        # Work one day
        pipeline.work_one_day()
        remaining_time = pipeline.remaining_time()

        # Check if remaining time is correctly estimated
        self.assertIsInstance(remaining_time, str)
        self.assertTrue(remaining_time.startswith("1d:"))  # Assuming at least 1 day left

    def test_pipeline_completion(self):
        """Test that the pipeline completes all tasks correctly."""
        L0 = Stage("L0", headcount=10, lead_time=30)  # Faster lead time, 30 minutes per task
        L1 = Stage("L1", headcount=5, lead_time=45)
        L2 = Stage("L2", headcount=3, lead_time=60)

        L0.add_tasks(100)  # Total tasks to process

        pipeline = Pipeline([L0, L1, L2])

        # Work until completion
        while not pipeline.is_complete():
            pipeline.work_one_day()

        # Ensure all stages have completed their tasks
        self.assertTrue(pipeline.is_complete())
        for stage in pipeline.stages:
            self.assertEqual(stage.tasks, 0)

    def test_multiple_days(self):
        """Test that the pipeline correctly handles task completion across multiple days."""
        L0 = Stage("L0", headcount=10, lead_time=60)
        L1 = Stage("L1", headcount=5, lead_time=60)
        L2 = Stage("L2", headcount=2, lead_time=60)

        L0.add_tasks(100)  # Large number of tasks

        pipeline = Pipeline([L0, L1, L2])

        # Run the pipeline for several days
        for _ in range(3):  # Simulate 3 days of work
            pipeline.work_one_day()

        # After 3 days, L0 should be mostly completed, and tasks should be moving to L1 and L2
        self.assertGreater(L1.tasks, 0)
        self.assertGreater(L2.tasks, 0)

