# Importing relevant project libraries. 
from math import fabs
from MessageParser import MessageParser
from ProcessQueue import *
from Procedure import Procedure

# Importing relevant queue modules.
import queue
from threading import Thread

# Queue class with dynamic load balancing depending on how long each script is taking to execute. 
# Designed to ensure minimal blockage, especially whenever executing a particular script has large 
# overhead. 
class QueueLoad:
    # Defining minimum and maximum load allowed
    min_load = 0.1
    max_load = 3
    RUNNING = False

    # Constructor. Inits number of bins, total entries, and processes.
    def __init__(self):
        self.num_bins = 5
        self.num_entries = 0
        self.processQ = queue.Queue(maxsize=0)
        for i in range(0, self.num_bins):
            self.queues = ProcessQueue()

    # Returns load factor
    def get_load(self):
        return self.num_entries / self.num_bins

    # Completes the pending processes stored within the queue.
    def complete(self):
        if not QueueLoad.RUNNING:
            QueueLoad.RUNNING = true
            for i in range(4):
                w = Thread(target=complete_procedures, args=(process_queue,))
                w.setDaemon(True)
                w.start()
            self.processQ.join()
            QueueLoad.RUNNING = False

    # If the load factor hits some critical mass, we will expand the number of
    # possible concurrent queues for program efficiency.
    def expand_queues(self):
        i = 0
        temp = self.num_bins
        while i < temp:
            self.queues.add(ProcessQueue())
            self.num_bins += 1
            i += 1

    # Adds to the current queue.
    def queue_process(self, process):
        pr_id = process.get_process_id()

        if self.get_load() > QueueLoad.max_load:
            self.expand_queues()

        assigned_queue = pr_id % self.num_bins
        self.queues[assigned_queue].add(process)
        self.num_entries += 1


# Creates a queue for the requested processes with a load limit that is pre-defined. 
# Insertions into the queue require constant time.
class ProcessQueue:
    # Constructor: defining the appropriate pointers and size. 
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Adding to the process queue linked list.
    def add(self, obj):
        if self.head is None and self.tail is None:
            self.head = obj
            self.tail = obj
            self.size += 1
        else:
            self.tail.next = obj
            self.tail = obj
            self.size += 1

    # FIFO pop structure.
    def pop(self):
        if self.size == 0:
            return None
        if self.size == 1:
            first = self.head
            self.head = None
            self.tail = None
            self.size -= 1
            first.complete()
            return first
        else:
            first = self.head
            self.head = self.head.next
            first.next = None
            self.size -= 1
            first.complete()
            return first

    def size(self):
        return self.size

    # Returns information about the first item within the queue.
    # Used for debugging and returning relevant meta data.
    def peek(self):
        if self.head is None:
            return "ProcessQueue is empty"
        else:
            return "Head Process in Queue:  " + \
                   self.head.to_string()


class MsgClient:
    def __init__(self, nn_model):
        # Setting the NLP model from the dumps folder we serialized the trained model in.
        # Everytime we re-train the model or add additional things to the model, WE MUST RE-RUN MAIN.
        self.nlp_model = nn_model
        self.command_model = self.nlp_model.get_command_model()

        # Taking the contents of the message and creating an object of the "MessageParser"
        # It will parse through the message that we just send and tell us key information about
        # the arguments, type, and etc.
        parsed_msg = MessageParser(message.content, self.nlp_model, self.command_model)
        if parsed_msg.is_command_ping():
            # Create a procedure of the "type" that we parsed the message
            # Extract the relevant arguments and pass them into the procedure
            # Push the procedure object onto the "Process Queue."
            procedure = Procedure(parsed_msg.get_command_type(), parsed_msg.get_argument())
            add_procedure_request(procedure)
            empty_procedure_queue()

    # Mirror function without server support.
    def process_message(self, text):
        parsed_msg = MessageParser(text, self.nlp_model, self.command_model)
        procedure = Procedure(parsed_msg.get_command_type(), parsed_msg.get_argument())
        parsed_msg.print_data()
        print(procedure.to_string())
        add_procedure_request(procedure)
        empty_procedure_queue()
