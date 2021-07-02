import time
import socket
import json



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 6999))
def send_move(move):
    client.send(move.encode('utf-8'))
    time.sleep(0.1)
    try:
        receiveData = client.recv(204800)
        return json.loads(receiveData)
    except:
        return {}



print("step0: ", send_move('get'))
print("step1: ", send_move('right'))
print("step2: ", send_move('left'))
print("step3: ", send_move('down'))
print("step4: ", send_move('up'))
print("step5: ", send_move('reset'))
print("step6: ", send_move('otherxxxxx'))