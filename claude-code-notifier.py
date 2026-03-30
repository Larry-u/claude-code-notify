#  conda activate claude-notify
# pyinstaller -F -w --add-data "claude.ico;." claude-code-notifier.py

import threading
import os
import sys
from flask import Flask, request
from win11toast import toast
import pystray
from PIL import Image, ImageDraw

# 初始化 Flask 应用
app = Flask(__name__)

@app.route('/send', methods=['GET', 'POST'])
def receive_message():
    """接收消息的接口"""
    msg = "收到一条新消息！" # 默认消息
    
    if request.method == 'POST':
        # 支持 JSON 格式 {"msg": "你的消息"}
        data = request.get_json(silent=True)
        if data and 'msg' in data:
            msg = data['msg']
        # 支持表单格式
        elif request.form.get('msg'):
            msg = request.form.get('msg')
    else:
        # 支持 GET 请求的 URL 参数 ?msg=你的消息
        if request.args.get('msg'):
            msg = request.args.get('msg')

    # # 触发 Windows 11 弹窗通知
    # # 可以在这里自定义通知的图标、点击操作等
    # toast('局域网通知助手', msg)
    
    # return {"status": "success", "message": "通知已发送"}, 200
    
    # 新增：定义一个专门用来发通知的小函数
    def show_toast(message):
        # 这个操作会在新线程里阻塞，但不影响 Flask 主线程
        # toast('局域网通知助手', message, scenario='reminder')
        toast('局域网通知助手', message, scenario='reminder', button='关闭')

    # 关键修改：启动一个独立的守护线程来发送弹窗
    # target 指向弹窗函数，args 传递消息参数
    threading.Thread(target=show_toast, args=(msg,), daemon=True).start()
    
    # 因为弹窗被扔到了别的线程，这里会立刻执行并返回给调用方！
    return {"status": "success", "message": "通知已发送"}, 200

def run_server():
    """在后台线程运行 Flask 服务"""
    # host='0.0.0.0' 允许局域网内其他机器访问
    # 禁用 debug 和 reloader 以防在多线程/打包后出现问题
    app.run(host='0.0.0.0', port=8888, debug=False, use_reloader=False)

def resource_path(relative_path):
    """
    获取资源的绝对路径。
    兼容开发环境（直接运行脚本）和 PyInstaller 打包后的环境（从临时目录运行）。
    """
    if hasattr(sys, '_MEIPASS'):
        # 如果是被 PyInstaller 打包的 EXE 运行，它会有一个 _MEIPASS 属性，指向解压的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 如果是直接运行 Python 脚本，就返回当前目录
    return os.path.join(os.path.abspath("."), relative_path)

def create_icon_image():
    """读取本地图片作为托盘图标"""
    # 将这里的 'my_icon.png' 替换为你本地图片的实际路径
    # 建议将图片放在和 notifier.py 同一个文件夹下，支持 .png 或 .ico 格式
    icon_path = resource_path('claude.ico')
    
    try:
        # 尝试打开本地图片
        image = Image.open(icon_path)
        return image
    except Exception as e:
        # 如果找不到图片或加载失败，使用之前的代码生成一个默认图标兜底
        print(f"无法加载本地图标 ({e})，将使用默认图标。")
        image = Image.new('RGB', (64, 64), (0, 120, 215))
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill=(255, 255, 255))
        return image

def quit_action(icon, item):
    """退出程序的逻辑"""
    icon.stop()
    os._exit(0) # 强制关闭包括 Flask 后台在内的整个进程

def setup_tray():
    """设置系统托盘"""
    image = create_icon_image()
    # 右键菜单
    menu = pystray.Menu(pystray.MenuItem('退出', quit_action))
    # 创建托盘图标
    icon = pystray.Icon("NetNotifier", image, "局域网通知服务", menu)
    icon.run()

if __name__ == '__main__':
    # 1. 启动 HTTP 监听服务（作为守护线程运行，不阻塞主线程）
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # 2. 启动系统托盘图标（必须运行在主线程，会阻塞直到用户点击退出）
    setup_tray()