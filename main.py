from Task import *
from Scheduler import *

# fcfs = FCFS({'R1': 2, 'R2': 1, 'R3': 1})
# fcfs.add_task(Z('T1', 3))
# fcfs.add_task(X('T2', 1))
# fcfs.add_task(Y('T3', 2))
# fcfs.run()

# sjf = SJF({'R1': 2, 'R2': 1, 'R3': 1})
# sjf.add_task(Z('T1', 3))
# sjf.add_task(X('T2', 1))
# sjf.add_task(Y('T3', 2))
# sjf.run()

rr = RR({'R1': 2, 'R2': 1, 'R3': 1}, 2)
rr.add_task(Z('T1', 3))
rr.add_task(X('T2', 1))
rr.add_task(Y('T3', 2))
rr.run()