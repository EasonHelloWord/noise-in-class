import os
import sys
import time
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.messagebox import showinfo


def check_for_updates(current_version,url):
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            if latest_version != current_version:
                response_body = response.json()["body"]

                root = tk.Tk()
                root.iconbitmap('./res/function.ico')
                root.title("检测到更新！！！")
                root.geometry("400x280")

                label = tk.Label(root, text=f"最新版本为 {latest_version}，是否下载？", font=(14))
                label.pack(pady=10)
                tk.Label(root, text="更新日志", font=(12)).pack(pady=5)
                scr = scrolledtext.ScrolledText(root, width=50, height=7, wrap=tk.WORD, font=(12))
                scr.insert(tk.INSERT, response_body)
                scr.pack(pady=10)
                scr.tag_configure("center", justify='center')
                scr.tag_add("center", "1.0", "end")
                frame = tk.Frame(root)
                frame.pack()

                def on_yes():
                    root.destroy()
                    download_latest_version(response.json()["assets"][0]["browser_download_url"])

                def on_no():
                    root.destroy()

                yes_button = tk.Button(frame, text='是', width=10, font=(12), command=on_yes)
                yes_button.pack(side=tk.LEFT, padx=10)

                no_button = tk.Button(frame, text='否', width=10, font=(12), command=on_no)
                no_button.pack(side=tk.RIGHT, padx=10)

                root.mainloop()

            else:
                print("当前已是最新版本。")
                return True
        else:
            print("无法获取最新版本信息。")
            return False
    except requests.RequestException as e:
        print(f"发生错误：{e}")
        return False


def download_latest_version(url):
    try:
        response = requests.get(url, stream=True)
        file_name = url.split("/")[-1]
        download_file_name = file_name + ".download"
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        root = tk.Tk()
        root.title("速度慢点没事")
        root.iconbitmap('./res/function.ico')

        progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10)
        progress_label = tk.Label(root, text="")
        progress_label.pack()
        progress = 0
        start_time = time.time()
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        # 拼接保存路径
        for data in response.iter_content(block_size):
            speed = (progress / 1024) / (time.time() - start_time) if time.time() - start_time > 0 else 0
            progress += len(data)
            with open(download_file_name, 'ab') as file:
                file.write(data)
            progress_percent = progress / total_size * 100
            progress_bar["value"] = progress_percent
            progress_label.config(text=f"下载速度: {speed:.2f} KB/s  进度: {progress_percent:.2f}%")
            progress_bar.update()
        file_name = os.path.join(base_path, file_name)
        os.rename(download_file_name, file_name)
        showinfo("更新成功", "最新版本下载完成。")
        root.destroy()

    except requests.RequestException as e:
        print(f"下载错误：{e}")


def check_update(current_version):
    current_version = current_version
    update_info = check_for_updates(current_version,"https://gitee.com/api/v5/repos/EasonJan/noise-in-class/releases/latest")
    if update_info == False:
        update_info = check_for_updates(current_version,"https://api.github.com/repos/EasonHelloWord/noise-in-class/releases/latest")



if __name__ == "__main__":
    check_update("V1.0.0")
