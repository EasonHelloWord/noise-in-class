import datetime
import random
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon

class Count:
    def __init__(self):
        self.db = {}
        self.alarm = []

    def reserve_db(self, db):
        current_time = self.get_time()
        if current_time not in self.db:
            self.db[current_time] = [db]
        else:
            self.db[current_time].append(db)

    def reserve_alarm(self):
        self.alarm.append(self.get_time())

    def get_time(self):
        current_time = datetime.datetime.now()
        return current_time.strftime("%H:%M")

    def calculate_averages(self):
        averages = {}
        for key in self.db:
            averages[key] = sum(self.db[key]) / len(self.db[key])
        return averages

    def plot_graph(self):
        data = self.calculate_averages()
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        x_data = list(range(len(data)))
        y_data = list(data.values())
        x_labels = list(data.keys())

        plt.plot(x_data, y_data)

        for time in self.alarm:
            if time in x_labels:
                index = x_labels.index(time)
                plt.scatter(index, data[time], color='red')  # 标记红色

        plt.xticks(x_data, x_labels, rotation=45)
        plt.xlabel('时间')
        plt.ylabel('分贝')
        plt.title('看看今天的统计数据叭')
        current_time = datetime.datetime.now().strftime("%H.%M.%S")
        plt.savefig(f'{current_time}.png')
        plt.show()


if __name__ == "__main__":
    import time
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