# Relevant Resources
#   - https://www.tutorialspoint.com/how-to-implement-multithreaded-queue-with-python
#   - https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#   - https://realpython.com/intro-to-python-threading/
# This draft will be primarily based on the second resource

import queue
from threading import Thread

NUMBER_OF_THREADS = 2

process_queue = queue.Queue(maxsize=0)


def add_procedure_request(procedure):
    process_queue.put(procedure)


def complete_procedures(q):
    while True:
        procedure = q.get()
        procedure.complete()
        q.task_done()


def empty_procedure_queue():
    for i in range(NUMBER_OF_THREADS):
        w = Thread(target=complete_procedures, args=(process_queue,))
        w.setDaemon(True)
        w.start()
    process_queue.join()
