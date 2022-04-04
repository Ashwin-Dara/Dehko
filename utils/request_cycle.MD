# Message (Request) Cycle
## High-Level Overview 
Everytime a user types a message into any one of the channels, we employ the same following procedure in order ensure that every single message is classified accurately, parsed consistently, and the corresponding requested routine is efficiently executed. There are four stages within this cycle: 
1. Message Parsing and Classification
2. Process Construction
3. Process Assignment and Balancing
4. Execution

### Message Parsing and Classification

Every time a message is received, it will be matched for the tag `@bot_name` in the very beginning of the message where the `bot_name` stands for the name of the bot. This will be to confirm where the sent messaged was directed to. 

### Process Construction

### Process Assignment and Balancing 

### Execution
