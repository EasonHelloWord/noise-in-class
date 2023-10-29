import datetime
import os
import sys

import matplotlib.pyplot as plt
from PyQt5 import QtGui


class Count:
    def __init__(self):
        self.averages = {}
        self.db = {}
        self.alarm = []
        # 获取文件所在的目录
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        # 拼接保存路径
        filename = os.path.join(base_path, "reports")
        if not os.path.exists(filename):  # 如果目录不存在则创建
            os.mkdir(filename)

    def reserve_db(self, db):
        if datetime.datetime.now().strftime("%S") == "0":
            self.calculate_averages()
            self.averages = {}
        current_time = self.get_time()
        if current_time not in self.db:
            self.db[current_time] = [db]
        else:
            self.db[current_time].append(db)

    def reserve_alarm(self):
        self.alarm.append(self.get_time())

    @staticmethod
    def get_time():
        current_time = datetime.datetime.now()
        current_second = current_time.second
        if current_second < 30:
            current_time = current_time.replace(second=0)
        else:
            current_time = current_time.replace(second=30)
        return current_time.strftime("%H:%M:%S")

    @staticmethod
    def get_weekday():
        weekday_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日'
        }

        date_object = datetime.date.today()
        weekday = date_object.weekday()
        return weekday_dict[weekday]

    def calculate_averages(self):
        for key in self.db:
            self.averages[key] = sum(self.db[key]) / len(self.db[key])
        return self.averages

    def plot_graph(self):
        data = self.calculate_averages()
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        x_data = list(range(len(data)))
        y_data = list(data.values())
        x_labels = list(data.keys())

        save_x = 30
        new_list = x_labels

        fig = plt.figure(figsize=(12, 6))
        fig.canvas.manager.set_window_title('好看的统计信息')
        fig.canvas.manager.window.setWindowIcon(QtGui.QIcon("./res/function.ico"))
        # 初始化 alarm_pot
        alarm_pot = None
        for alarm_time in self.alarm:
            if alarm_time in x_labels:
                index = x_labels.index(alarm_time)
                alarm_pot = plt.scatter(index, data[alarm_time], color='red')  # 标记红色
        if len(x_labels) > save_x:
            new_list = [''] * len(x_labels)
            change_item = list(range(0, len(x_labels), len(x_labels) // save_x))
            for i in change_item:
                if i < len(x_labels):
                    new_list[i] = x_labels[i]
        x_labels = new_list
        db_line, = plt.plot(x_data, y_data, color='blue')  # 分贝图
        average_line, = plt.plot(x_data, [sum(y_data) / len(y_data) for _ in range(len(x_data))], color='orange')  # 平均值
        if alarm_pot:
            plt.legend(handles=[db_line, average_line, alarm_pot], labels=["响度值", "平均值", "报警时间点"],
                       loc="lower right")
        else:
            plt.legend(handles=[db_line, average_line], labels=["响度值", "平均值"], loc="lower right")
        plt.xticks(x_data, x_labels, rotation=45)
        plt.xlabel('时间')
        plt.ylabel('分贝')
        current_date_month = datetime.datetime.now().strftime("%m")
        current_date_day = datetime.datetime.now().strftime("%d")
        plt.title(f'看看{current_date_month}月{current_date_day}日({self.get_weekday()})的统计数据叭')
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        plt.tight_layout(pad=2.0, w_pad=0.5, h_pad=1.0, rect=(0, 0, 1, 0.95))
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        # 拼接保存路径
        filename = os.path.join(base_path, "reports")
        save_path = os.path.join(filename, f"{current_time}.png")
        plt.savefig(save_path)
        plt.show()


if __name__ == "__main__":
    import time
    import random

    counter = Count()
    for x in range(3600):
        counter.reserve_db(random.uniform(-70, 0))
        time.sleep(0.01)
    for x in range(50):
        counter.reserve_db(random.uniform(-70, 0))
        time.sleep(0.01)
        # 假设alarm是在特定时间触发
        counter.reserve_alarm()
    counter.plot_graph()
