import sounddevice as sd
import numpy as np
import tkinter as tk
from threading import Thread
import time
import sys
import winsound
from . import tools

class MicMonitor:
    def __init__(self,ver):
        self.count = tools.Count()
        self.db_threshold = -25
        self.alarm_enabled = False
        self.warning_shown = True
        self.db_down_count = 0
        self.warning_start = 0
        self.current_indata = None
        self.ver = ver
        self.root = tk.Tk()
        self.root.title("你有点大声awa")
        self.root.attributes('-topmost', True)
        self.root.geometry("180x165")
        self.root.iconbitmap("./res/function.ico")

        self.setup_ui()

    def setup_ui(self):
        db_threshold_label = tk.Label(self.root, text="分贝阈值", font=("", 9))
        db_threshold_label.pack()

        db_threshold_slider = tk.Scale(self.root, from_=-90, to=0, orient="horizontal",
                                    command=lambda x: self.set_threshold(int(x)), length=300)
        db_threshold_slider.set(self.db_threshold)
        db_threshold_slider.config(font=("", 9))
        db_threshold_slider.pack()

        self.db_label = tk.Label(self.root, text="分贝：0", font=("", 12))
        self.db_label.pack()

        me_label = tk.Label(self.root, text=f"制作：Eason_J  {self.ver}", font=("", 9))
        me_label.pack()

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        alarm_checkbox = tk.Checkbutton(
            main_frame, text="启用警报", command=self.toggle_alarm, font=("", 10))
        alarm_checkbox.pack()

        self.warning_label = tk.Label(self.root, text="你有点大声", bg="red",
                                    fg="white", font=("", 15), width=20, height=2)
        self.warning_label.pack(side="bottom", fill="x")
        self.warning_label.pack_forget()

    def calculate_db(self, indata):
        rms = np.sqrt(np.mean(indata**2))
        db = 20 * np.log10(rms)
        self.count.reserve_db(db)
        return db

    def callback(self, indata, frames, time1, status):
        self.current_indata = indata
        if status:
            print(status, file=sys.stderr)
        db = self.calculate_db(indata)
        self.db_label.config(text=f"分贝: {db:.2f} dB", font=("", 12))

        if db >= self.db_threshold:
            self.db_down_count = 0
            self.start_warning(self.warning_label)
            self.warning_shown = True
            if self.alarm_enabled:
                if self.warning_shown and time.time()-self.warning_start > 2:
                    Thread(target=self.play_alarm).start()
        elif db < self.db_threshold:
            self.warning_shown = False
            self.hide_warning(self.warning_label)

    def hide_warning(self, label):
        self.db_down_count += 1
        if self.db_down_count > 20:
            label.pack_forget()
            self.warning_shown = False
            self.db_down_count = 0

    def start_warning(self, label):
        label.pack()
        self.warning_shown = True

    def play_alarm(self):
        self.warning_start = time.time()+1
        yes = 0
        no = 0
        for x in range(30):
            db = self.calculate_db(self.current_indata)
            if db >= self.db_threshold:
                yes += 1
            else:no += 1
            time.sleep(0.1)
        if self.alarm_enabled and yes/(yes+no) >= 0.3:
            self.count.reserve_alarm()
            winsound.PlaySound("./res/mic/保持安静.wav", winsound.SND_FILENAME)

    def set_threshold(self, value):
        self.db_threshold = value

    def toggle_alarm(self):
        self.alarm_enabled = not self.alarm_enabled

    def run(self):
        with sd.InputStream(callback=self.callback, channels=1, samplerate=44100, device=None):
            self.root.mainloop()
        self.count.plot_graph()

if __name__ == "__main__":
    monitor = MicMonitor('V1.2.4')
    monitor.run()
    monitor.count()
