import threading
import time
from typing import SupportsFloat


class Timer(threading.Thread):

    def __init__(self):
        super().__init__()
        self._pause = threading.Event()  # 用于暂停线程的标识
        self._pause.set()  # 设置为True
        self._stop = threading.Event()  # 用于停止线程的标识
        self._stop.set()  # 将running设置为True

        self.num = 0

    def run(self):
        while self._stop.isSet():
            self._pause.wait()  # 为True时立即返回, 为False时阻塞直到self.__flag为True后返回
            self.running()
            time.sleep(1)

    def running(self):
        self.num += 1
        print("NUM:", self.num)

    def pause(self):
        self._pause.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self._pause.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self._pause.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self._stop.clear()  # 设置为False


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    time.sleep(3)
    print("暂停")
    timer.pause()
    time.sleep(3)
    print("继续")
    timer.resume()
    time.sleep(2)
    print("停止")
    timer.stop()
