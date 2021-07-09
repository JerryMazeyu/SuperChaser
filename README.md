# SuperChaser
追逐动态目标的小游戏，游戏者可以通过操作键盘或socket传命令两种方式对目标人物进行控制，目标是在尽可能高得分情况下抓住目标对象。

![](https://jerrymazeyu.oss-cn-shanghai.aliyuncs.com/2021-07-02-QQ20210702-155327-HD.gif)

## 目录

* [游戏规则](#rule)
* [快速开始](#start)
* [可配置项](#config)
* [服务端并行无图形界面环境](#serv)

### <span id="rule">游戏规则</span>

1. 主角从起点捉住目标对象即为成功，以最终得分为成绩。
2. 在每一次迷宫行走时，最初得分为100分。（）
3. 每走一步扣1分。
4. 尝试向墙壁移动扣2分。
5. 走到炸弹直接判定游戏失败（-1000分），重置游戏。
6. 得分<0时游戏失败，重置游戏。
7. 每回合有随机数量、随机奖励值的一些金币，触碰到可以加一定的分数。
8. 主角可以通过行走不断探索迷宫信息，感知范围是周围4个单位为半径的区域。
9. 在目标对象不在主角的感知范围时，目标每次进行一定规则的随机游走，但会尽量避免走重复的路。
10. 在目标对象属于主角的感知范围时，目标会尽可能的逃离主角。
11. 游戏分为两种难度，其中简单模式下，目标对象有0.2的几率放弃移动，在困难模式下，目标对象和主角的移动频率相同。

### <span id="start">快速开始</span>

```shell
$ git clone git://github.com/JerryMazeyu/SuperChaser.git
$ cd SuperChaser
$ pip install --user ./requirement.txt
$ python main.py # 打开游戏界面
```

运行后会出现游戏主菜单界面，图上有两个🍄，分别选择模式与难度，在动的🍄是可选状态，⬆️⬇️切换选项，按下`Enter`或➡️可以确认选择，⬅️可以重置选择，当两个模式都进行过确认后，则进入游戏主界面。

其中键盘上下左右可以操作主角进行移动，R键可以重置得分和状态，每次移动会点亮周围范围内的部分地图，这些信息在通过socket接受时会作为返回值。

socket传输的案例可以在`client.py`中查看：

```python
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

print("step0: ", sendMove('get'))
# 基础迷宫地图信息（奖励值boom_value、地图信息maze、主角所处的坐标player_cord、当前得分score、状态state（0运行 1成功 -1失败）、目标对象坐标target/target_cord、总用步数total_steps）
# step0:  {'bonus_value': 22, 'maze': [[*]](n*n), 'player_cord': [1, 1], 'score': 100, 'state': 0, 'target': [17, 17], 'target_cord': [17, 17], 'total_steps': 0}
print("step1: ", sendMove('right'))
# 做出移动后的状态
# step1:  {'bonus_value': 46, 'maze': [[*]], 'player_cord': [1, 2], 'score': 99, 'state': 0, 'target': [18, 18], 'target_cord': [17, 17], 'total_steps': 1}
```

其中地图信息为二维列表，其中每一个列表元素代表一行的信息，-9是未探索的部分，0是路，1是墙壁，9是目标，2是金币，-1是炸弹/怪物。

### <span id="conf">可配置项</span>

在`config.py`中可以对迷宫的维度进行配置，其中文件内部有详细的说明。

### <span id="conf">服务端并行无图形界面环境</span>

为了便于并行训练，在`server/server.py`中实现了无图形界面的版本，具体可以参考程序内部的实现。
