from Task import *
from typing import List, Dict
from abc import ABC, abstractmethod


class Scheduler(ABC):
    def __init__(self, resources):
        assert 'R1' in resources.keys()
        assert 'R2' in resources.keys()
        assert 'R3' in resources.keys()
        self.resources: Dict[str, int] = resources
        self.ready: List[Task] = []
        self.waiting: List[Task] = []
        self.running: Task = None
    
    def check_resources_satisfied(self, task: Task):
        for resource_type, amount in task.needs.items():
            if self.resources[resource_type] < amount:
                return False
        return True
    
    def assign_resources(self, task: Task):
        for resource_type, amount in task.needs.items():
            self.resources[resource_type] -= amount
            task.holding[resource_type] = amount

    def release_resources(self, task: Task):
        for resource_type, amount in task.holding.items():
            self.resources[resource_type] += amount
    
    def add_task(self, task: Task):
        self.ready.insert(0, task)
    
    """ State transition methods """

    # releasing of resources is not done here, just the transition
    def move_from_running_to_finished(self):
        assert self.running is not None
        self.running.set_state('Finished')
        self.running = None
    
    # releasing of resources is not done here, just the transition
    def move_from_running_to_ready(self):
        assert self.running is not None
        self.ready.insert(0, self.running)
        self.running.set_state('Ready')
        self.running = None
    
    def move_from_ready_to_waiting(self, task: Task):
        assert task in self.ready
        self.ready.remove(task)
        self.waiting.insert(0, task)
        task.set_state('Waiting')
    
    # resource satisfaction check and allocation is not done here, just the transition
    def move_from_ready_to_running(self, task: Task):
        assert task in self.ready
        assert self.running is None
        self.ready.remove(task)
        self.running = task
        self.running.set_state('Running')
    
    def move_from_waiting_to_ready(self, task: Task, position: int):
        assert task in self.waiting
        self.waiting.remove(task)
        self.ready.insert(position, task)
        task.set_state('Ready')
    
    # A naive simulation of CPU
    def cpu_tick(self):
        for task in self.ready:
            task.tick()
        for task in self.waiting:
            task.tick()
        if self.running is None:
            return
        self.running.tick()
        if self.running.is_done():
            self.release_resources(self.running)
            self.move_from_running_to_finished()
    
    def check_waiting(self):
        # This strategy does not affect SJF and HRRN
        to_be_moved = [task for task in self.waiting if self.check_resources_satisfied(task)]
        to_be_moved = sorted(to_be_moved, key=lambda x: x.priority) # highest priority is at first
        for task in to_be_moved:
            self.move_from_waiting_to_ready(task, 0)
    
    def run(self):
        while self.running or self.waiting or self.ready:
            print(self)
            self.cpu_tick()
            # schedule
            self.check_waiting()
            self.schedule()

    @abstractmethod
    def schedule(self):
        pass

    def __repr__(self) -> str:
        repr = "\t".join(["{}:{}".format(key, value) for key, value in self.resources.items()])+"\n"
        repr += "Ready Queue: ["+",".join(list(map(str, self.ready)))+"]\n"
        repr += "Waiting Queue: ["+",".join(list(map(str, self.waiting)))+"]\n"
        repr += "Running: "+str(self.running)+"\n"+"-"*50
        return repr
    

class FCFS(Scheduler):
    def __init__(self, resources):
        super().__init__(resources)
    
    def schedule(self):
        if self.running is not None:
            # CPU is occupied
            return
        while self.ready:
            # Find and dispatch a task
            task = self.ready[-1]
            if self.check_resources_satisfied(task):
                self.assign_resources(task)
                self.move_from_ready_to_running(task)
                break
            else:
                self.move_from_ready_to_waiting(task)


class SJF(Scheduler):
    def __init__(self, resources):
        super().__init__(resources)
    
    def schedule(self):
        if self.running is not None:
            # CPU is occupied
            return
        while self.ready:
            # Find and dispatch a task
            task = min(self.ready, key=lambda x: x.duration)
            if self.check_resources_satisfied(task):
                self.assign_resources(task)
                self.move_from_ready_to_running(task)
                break
            else:
                self.move_from_ready_to_waiting(task)


class RR(Scheduler):
    def __init__(self, resources, quantum):
        super().__init__(resources)
        self.q = quantum
        self.t = 0
    
    def schedule(self):
        if self.t % self.q == 0 or self.running is None:
            # preempt if needed
            if self.running is not None:
                self.move_from_running_to_ready()
            else:
                # reset time counter, a task has finished faster than quantum
                self.t = 0
            while self.ready:
                # Find and dispatch a task
                task = self.ready[-1]
                if task.holding:
                    self.move_from_ready_to_running(task)
                    break
                elif self.check_resources_satisfied(task):
                    self.assign_resources(task)
                    self.move_from_ready_to_running(task)
                    break
                else:
                    self.move_from_ready_to_waiting(task)
        self.t += 1


class HRRN(Scheduler):
    def __init__(self, resources):
        super().__init__(resources)
    
    def schedule(self):
        if self.running is not None:
            # CPU is occupied
            return
        while self.ready:
            # Find and dispatch a task
            task = max(self.ready, key=lambda x: x.get_response_ratio())
            if self.check_resources_satisfied(task):
                self.assign_resources(task)
                self.move_from_ready_to_running(task)
                break
            else:
                self.move_from_ready_to_waiting(task)