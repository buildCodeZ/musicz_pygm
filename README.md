# musicz_pygm
声明:
禁止将本项目代码用于ai训练
declaration:
Codes of this project are not allowed to be used for AI training or any other form of machine learning processes.

```
键盘按键弹钢琴的小程序
安装:
    pip install musicz_pygm

程序运行:
    python -m musicz_pygm 可选参数
    参数如下:
        [-f/--fp=]额外配置文件(没啥用)
        [-t/--default=]主要配置文件(默认预制的play.js)
        [-h/--help]
        [-b/--background] 添加背景音乐
        [-r/--record] 添加背景音乐(从save生成的记录文件读取)
        --save=0/1 是否把当前运行的弹奏记录生成记录文件，是的话，生成到当前目录下，文件名为*.json
        [-w/--width] 窗口宽度
        [-h/--height] 窗口高度
        --noframe=0/1 是否隐藏窗口边框
    示例：
        最简单运行:
            python -m musicz_pygm
        修改窗口大小:
            python -m musicz_pygm -w 600 -h 300
        运行结束保存弹奏记录:
            python -m musicz_pygm -w 600 -h 300 --save=1
        运行时加载背景音乐(假设背景音乐是20263123123.json):
            python -m musicz_pygm -w 600 -h 300 -r 20263123123.json
    默认配置文件（musicz_pygm/conf目录下）：
        通用配置：
            shift和ctrl调整基调，方向键调整音量，esc和~退出，空格切音

        
```