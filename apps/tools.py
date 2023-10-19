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
        current_time = self.get_time()
        if current_time not in self.db:
            self.db[current_time] = [db]
        else:
            self.db[current_time].append(db)
        if datetime.datetime.now().strftime("%S") == "0":
            self.calculate_averages()
            self.averages = {}
    def reserve_alarm(self):
        self.alarm.append(self.get_time())

    def get_time(self):
        current_time = datetime.datetime.now()
        return current_time.strftime("%H:%M")

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
        fig = plt.figure()
        fig.canvas.manager.set_window_title('好看的统计信息')
        fig.canvas.manager.window.setWindowIcon(QtGui.QIcon("./res/function.ico"))
        plt.plot(x_data, y_data)

        for time in self.alarm:
            if time in x_labels:
                index = x_labels.index(time)
                plt.scatter(index, data[time], color='red')  # 标记红色

        plt.xticks(x_data, x_labels, rotation=45)
        plt.xlabel('时间')
        plt.ylabel('分贝')
        plt.title('看看今天的统计数据叭')
        current_time = datetime.datetime.now().strftime("%Y-%m_%d-%H-%M")
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
    import time,random
    counter = Count()
    for x in range(50):
        counter.reserve_db(random.uniform(-70, 0))
        time.sleep(0.1)
    for x in range(50):
        counter.reserve_db(random.uniform(-70, 0))
        time.sleep(0.1)
        # 假设alarm是在特定时间触发
        counter.reserve_alarm()
    counter.plot_graph()
