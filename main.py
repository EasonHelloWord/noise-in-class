import sounddevice as sd
import numpy as np
import tkinter as tk
from threading import Thread
import time
import sys
import os
import winsound
ver = "v1.2.1"
# 资源文件目录访问


def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath("./res")
    return os.path.join(base_path, relative_path)


# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('')
os.chdir(cd)
# 麦克风设置
mic_device = None  # 根据需要设置麦克风设备
sample_rate = 44100  # 根据需要调整采样率

# 分贝阈值和警报开关
db_threshold = -40  # 初始阈值
alarm_enabled = False  # 警报开关

# 创建图形用户界面
root = tk.Tk()
root.title("你有点大声awa")
root.attributes('-topmost', True)  # 将窗口置顶
root.geometry("255x210")  # 设置窗口宽度为400像素，高度为400像素
root.iconbitmap("./下载.ico")
# 创建滑块用于设置分贝阈值
db_threshold_label = tk.Label(root, text="分贝阈值", font=("", 16))  # 修改标签字体
db_threshold_label.pack()

# 修改滑块的长度和字体
db_threshold_slider = tk.Scale(root, from_=-90, to=0, orient="horizontal",
                               command=lambda x: set_threshold(int(x)), length=300)
db_threshold_slider.set(db_threshold)
db_threshold_slider.config(font=("", 12))
db_threshold_slider.pack()
# 创建分贝显示标签
db_label = tk.Label(root, text="分贝：0", font=("", 18))  # 修改标签字体
db_label.pack()
# 创建个人显示标签
me_label = tk.Label(root, text=f"制作：Eason_J  {ver}", font=("", 10))  # 修改标签字体
me_label.pack()
# 创建一个主框架并使用pack布局
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)
# 创建复选框用于启用/禁用警报
def toggle_alarm():
    global alarm_enabled
    alarm_enabled = not alarm_enabled


alarm_checkbox = tk.Checkbutton(
    main_frame, text="启用警报", command=toggle_alarm, font=("", 14))  # 修改复选框字体
alarm_checkbox.pack()
# 创建警告显示标签
warning_label = tk.Label(root, text="你有点大声", bg="red",
                         fg="white", font=("", 20), width=20, height=2)
warning_label.pack(side="bottom", fill="x")  # 底部对齐，水平平铺
warning_label.pack_forget()
# 在全局范围内创建一个变量，用于跟踪警告消息的状态
warning_shown = True
db_down_count = 0
warning_start = 0

# 分贝检测函数
def calculate_db(indata):
    rms = np.sqrt(np.mean(indata**2))
    db = 20 * np.log10(rms)
    return db

# 麦克风录音回调函数
def callback(indata, frames, time, status):
    global warning_shown
    if status:
        print(status, file=sys.stderr)
    db = calculate_db(indata)
    db_label.config(text=f"分贝: {db:.2f} dB")

    if db >= db_threshold:
        global db_down_count
        db_down_count = 0
        # 创建警告消息标签
        start_warning(warning_label)
        warning_shown = True
        if alarm_enabled:
            Thread(target=play_alarm).start()
    elif db < db_threshold:
        warning_shown = False
        hide_warning(warning_label)


# 隐藏警告消息
def hide_warning(label):
    global db_down_count
    db_down_count += 1

    if db_down_count > 20:
        label.pack_forget()
        global warning_shown
        warning_shown = False
        db_down_count = 0


# 显示警告消息
def start_warning(label):
    label.pack()
    global warning_shown
    warning_shown = True


# 播放警报声音
def play_alarm():
    global warning_start
    if warning_shown and time.time()-warning_start > 3:
        time.sleep(3)
        if warning_shown and time.time()-warning_start > 3:
            warning_start = time.time()
            winsound.PlaySound("保持安静.wav", winsound.SND_FILENAME)


# 设置分贝阈值
def set_threshold(value):
    global db_threshold
    db_threshold = value

# 切换警报开关
def toggle_alarm():
    global alarm_enabled
    alarm_enabled = not alarm_enabled


# 启动麦克风录音
with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, device=mic_device):
    root.mainloop()
