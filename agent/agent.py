"""
Example agent.
"""

import random

class Agent():
    def __init__(self, batch=1):
        self.batch = batch

    def move(self, env):
        res = []
        for i in range(self.batch):
            res.append(random.choice(['up', 'down', 'left', 'right']))
        return res


