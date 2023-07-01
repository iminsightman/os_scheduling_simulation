from Task import *
from Scheduler import *

r1, r2, r3 = tuple(map(int, input().split(' ')))
n_tasks = int(input())
tasks = []
for _ in range(n_tasks):
    name, task_type, duration = input().split(' ')
    task = eval("{}('{}', {})".format(task_type, name, duration))
    tasks.append(task)

# fcfs = FCFS({'R1': r1, 'R2': r2, 'R3': r3})
# for task in tasks:
#     fcfs.add_task(task)
# fcfs.run()

# sjf = SJF({'R1': r1, 'R2': r2, 'R3': r3})
# for task in tasks:
#     sjf.add_task(task)
# sjf.run()

# rr = RR({'R1': r1, 'R2': r2, 'R3': r3}, 2)
# for task in tasks:
#     rr.add_task(task)
# rr.run()

hrrn = HRRN({'R1': r1, 'R2': r2, 'R3': r3})
for task in tasks:
    hrrn.add_task(task)
hrrn.run()