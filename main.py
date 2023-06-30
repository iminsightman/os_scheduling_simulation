from Task import *
from Scheduler import *

fcfs = FCFS({'R1': 2, 'R2': 1, 'R3': 1})
fcfs.add_task(Z('T1', 2))
fcfs.add_task(X('T2', 3))
fcfs.add_task(Y('T3', 4))
fcfs.add_task(Y('T4', 4))
fcfs.run()