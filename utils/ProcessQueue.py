# Importing relevant modules for multithreaded queue. 
import queue
from threading import Thread

# Max number of threads allowed concurrently
NUMBER_OF_THREADS = 4
RUNNING_QUEUE = False

# Init. process queue.
process_queue = queue.Queue(maxsize=0)

# Adds element to process queue.
def add_procedure_request(procedure):
    process_queue.put(procedure)

# Executes all pending tasks.
def complete_procedures(q):
    while True:
        procedure = q.get()
        procedure.complete()
        q.task_done()

# Helper which is multi-threaded empty.
def empty_procedure_queue():
    global RUNNING_QUEUE
    if not RUNNING_QUEUE:
        RUNNING_QUEUE = True
        for i in range(NUMBER_OF_THREADS):
            w = Thread(target=complete_procedures, args=(process_queue,))
            w.setDaemon(True)
            w.start()
        process_queue.join()
        RUNNING_QUEUE = False

# Relevant Resources
#   - https://www.tutorialspoint.com/how-to-implement-multithreaded-queue-with-python
#   - https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#   - https://realpython.com/intro-to-python-threading/
