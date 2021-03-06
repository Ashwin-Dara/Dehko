# Message (Request) Cycle
## High-Level Overview 
Everytime a user types a message into any one of the channels, we employ the same following procedure in order ensure that every single message is classified accurately, parsed consistently, and the corresponding requested routine is efficiently executed. There are four stages within this cycle: 
1. Message Parsing and Classification
2. Process Construction
3. Process Assignment and Balancing
4. Execution

### Message Parsing and Classification

Every time a message is received, it will be matched for the tag `@bot_name` in the very beginning of the message where the `bot_name` stands for the name of the bot. This will be to confirm where the most recently sent messaged was directed to.

Here is a valid message structure which would parsed and be deconstructed into a process object.

#### INSERT DIAGRAM*** HAVE A DIAGRAM SIMILAR TO THE COMMUNICATION PROCOTOLS

The "heading" ping indicates the message needs to be parsed. Finally, the argument, which takes the structure `~argument~` or `~argument` (either will work) will be extracted and removed from the message. The only text remaining within the message will what the client naturally sends, which will be classified using an RNN and mapped to a corresponding valid command.

### Process Construction

After breaking the message into its three components and removing the head and the tail component, the "body" is classified and converted into a process object. Here is an overview of the `Process` class.

```{python}
Process

    @Members
    
    @Functions 
```

### Process Assignment and Load Balancing  

To efficiently handle all requests, employed is a model analogous to load balancing. Here's an overview of how requests are handled and efficiently processed:
1. Client messages/commands are converted to Processes.
   1. Processes have a consistent associated process ID.
   2. The ID is based on the (1) sender's user id (2) the type of request the user is making.


2. Processes are assigned to various `ProcessQueues`. Requests follow a FIFO mechanism.
   1. The system begins with 5 `ProcessQueues` in parallel.
   2. All queues are multi-tasking with completetion as the end whole.
   3. If the load factor is below a certain amount, the number of concurrent `ProcessQueues` will double.


### Efficient Execution

## Dependencies
### APIs

### Libraries

### Installation