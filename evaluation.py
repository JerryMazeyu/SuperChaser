"""
Automatically evaluate script.
"""


from agent import agent_ins
from server.server import Server
import time
import json


print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()) )
server = Server(1)
round_ = 0
result = []
print("Start Evaluation...")
while round_ < 10:
    while True:
        initState = server.step(['get'])
        move = agent_ins.move(initState)
        reward = server.step(move)[0]
        state = reward['state']
        # print(f"Round {round_}: ; Reward: {reward}")
        if state != 0:
            print(f"Round {round_+1} is over, state is {state}, final score is {max(0, reward['score'])}.")
            print("="*66)
            result.append(max(0, reward['score']))
            round_ += 1
            break
print("Evaluation is OK! Saving to Json.")
now_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
with open('finalscore.json', 'w') as file:
    json.dump({'detail': result, 'score': sum(result)/len(result)}, file)




