from queue import Queue
from threading import Thread
import threading
import time

# 创建队列实例，用于存储任务
queue = Queue()

def do_job():
    while True:
        i = queue.get()
        time.sleep(1)
        print("index %s. current: %s" % (i, threading.current_thread()))
        queue.task_done()


if __name__ == '__main__':
    #创建包含三个线程的线程池
    for i in range(3):
        t = Thread(target = do_job)
        #t.daemon = True
        t.start()


    time.sleep(3)
    for i in range(10):
        queue.put(i)

    queue.join()