from Task import *
from typing import List, Dict


class Scheduler:
    def __init__(self, resources):
        assert resources['R1']
        assert resources['R2']
        assert resources['R3']
        self.resources: Dict[str, int] = resources
        self.ready: List[Task] = []
        self.waiting: List[Task] = []
        self.running: Task = None
    
    def check_resources_satisfied(self, task: Task):
        for resource_type, amount in task.needs.keys():
            if self.resources[resource_type] < amount:
                return False
        return True

    def add_task(self, task: Task):
        self.ready.insert(0, task)
    
    def check_running_task(self):
        if self.running is None:
            return
        if self.running.is_done():
            # Free CPU
            # Release resources
            pass
    
    def sjf(self):
        while self.running or self.ready or self.waiting:
            pass
    

