
from collections import defaultdict

class Activity:
    def __init__(self, code, duration, predecessors):
        self.code = code
        self.duration = duration
        self.predecessors = predecessors
        self.successors = []
        self.ES = 0
        self.EF = 0
        self.LS = float('inf')
        self.LF = float('inf')

# Dinisikan aktivitas dan durasi disini, serta hubungan antar aktivitas (predecessors)
activities_data = [
    ('A', 3, []),
    ('B', 7, ['A']),
    ('C', 3, []),
    ('D', 6, ['A']),
    ('E', 8, ['D']),
    ('F', 2, ['C']),
    ('G', 3, ['E']),
    ('H', 3, ['F']),
    ('I', 4, ['G', 'H']),
    ('J', 5, ['I'])
]

activities = {code: Activity(code, duration, preds) for code, duration, preds in activities_data}

# Build successors
for act in activities.values():
    for pred in act.predecessors:
        activities[pred].successors.append(act.code)

# Forward pass: hitungan ES, EF
def forward_pass():
    visited = set()
    def visit(node):
        act = activities[node]
        if node in visited:
            return
        for pred in act.predecessors:
            visit(pred)
            act.ES = max(act.ES, activities[pred].EF)
        act.EF = act.ES + act.duration
        visited.add(node)

    for code in activities:
        visit(code)

# Backward pass: kalkulasi LF, LS

def backward_pass(project_duration):
    visited = set()
    def visit(node):
        act = activities[node]
        if node in visited:
            return
        if not act.successors:
            act.LF = project_duration
        else:
            act.LF = min(activities[succ].LS for succ in act.successors)
        act.LS = act.LF - act.duration
        visited.add(node)
        for pred in act.predecessors:
            visit(pred)

    for code in reversed(list(activities.keys())):
        visit(code)

# Run kalkulasi CPM 
forward_pass()
project_duration = max(act.EF for act in activities.values())
backward_pass(project_duration)

# Print hasil
print(f"\n{'Activity':<10}{'ES':<5}{'EF':<5}{'LS':<5}{'LF':<5}{'Slack':<7}{'Critical':<10}")
for code in activities:
    act = activities[code]
    slack = act.LS - act.ES
    critical = 'Yes' if slack == 0 else 'No'
    print(f"{code:<10}{act.ES:<5}{act.EF:<5}{act.LS:<5}{act.LF:<5}{slack:<7}{critical:<10}")

print(f"\nTotal Project Duration: {project_duration} weeks")