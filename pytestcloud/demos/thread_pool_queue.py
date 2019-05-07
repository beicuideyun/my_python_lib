import queue
import threading
import socket

class ThreadPoolManager():
    def __init__(self, thread_num):
        self.work_queue = queue.Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        for i in range(thread_num):
            thread = ThreadManager(self.work_queue)
            thread.start()

    def add_jobs(self, func, *args):
        self.work_queue.put((func, args))

class ThreadManager(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            target, args = self.work_queue.get()
            target(*args)
            self.work_queue.task_done()

thread_pool = ThreadPoolManager(4)

def handle_request(conn_sockt):
    recv_data = conn_sockt.recv(1024)
    reply = 'HTPP/1.1 200 OK \r\n\r\n'
    reply += "hello world"
    print("thread %s is running" % threading.current_thread().name)
    conn_sockt.send(reply)
    conn_sockt.close()

host = ""
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    conn_socket, addr = s.accept()
    thread_pool.add_jobs(handle_request, *(conn_socket, ))

s.close()