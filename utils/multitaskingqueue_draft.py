import queue
import threading
import time

process_queue = queue.Queue()


# This function will add a procedure to the process_queue. It
def add_to_queue(procedure):
    process_queue.put(procedure)


# Tries to empty all of the current processes within the process_queue
def complete_queue():
    while True:
        try:
            proc = process_queue.get(block=False)
        except process_queue.empty:
            return
        else:
            proc()


class Multithread(threading.Thread):

    def __init__(self, thread_name):
        self.name = thread_name

    def run(self):
        complete_queue()


t1 = Multithread("placeholder")
t1.start()
t1.join()




