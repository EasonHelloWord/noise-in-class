from threading import Thread
from apps import update,MicMonitor
if __name__ == "__main__":
    current_version="V2.0.0"
    Thread(target=update.check_update,args=(current_version,)).start()
    MicMonitor.MicMonitor(current_version).run()