from typing import Dict


class Task:
    def __init__(self, name: str, duration: int, needs: Dict[str, int], priority: int):
        self.name = name
        self.duration = duration
        self.needs = needs
        self.priority = priority
        self.holding: Dict[str, int] = {}
        self.state = 'Ready'
        self.remaining = self.duration
    
    def tick(self):
        if self.state == 'Running' and self.remaining > 0:
            self.remaining -= 1
    
    def set_state(self, state: str):
        assert state in ['Ready', 'Waiting', 'Running', 'Finished']
        self.state = state
    
    def is_done(self):
        return self.remaining == 0

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.__repr__()


class Z(Task):
    def __init__(self, name: str, duration: int):
        super().__init__(name, duration, {'R1': 1, 'R3': 1}, 1)


class Y(Task):
    def __init__(self, name: str, duration: int):
        super().__init__(name, duration, {'R2': 1, 'R3': 1}, 2)


class X(Task):
    def __init__(self, name: str, duration: int):
        super().__init__(name, duration, {'R1': 1, 'R2': 1}, 3)