import os
import sys
from threading import Thread
from apps import update,db_control
if __name__ == "__main__":
    current_version="V2.1.0"
    # 资源文件目录访问


    def source_path(relative_path):
        # 是否Bundle Resource
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    # 修改当前工作目录，使得资源文件可以被正确访问
    cd = source_path('')
    os.chdir(cd)
    # Thread(target=update.check_update,args=(current_version,)).start()
    db_control.MicMonitor(current_version).run()