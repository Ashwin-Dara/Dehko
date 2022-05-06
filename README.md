## Dehcko
Dehko is an NLP smart assistant tool built for your terminal to easily define custom automation macros without worrying about the particular syntax. Type in a description of the task you wish to run, and Dehko will automatically classify natural language to the corresponding intended command. Dehko allows you to eliminate the baggage that comes with the strict precision currently required for many CLI tools. Commands and intents are highly configurable, and can be done by modifying a JSON configuration file. More details are described in **Customization**. 

#### Insert Video Here

## Installation
Dehko was containirzied using Docker for robust and interactibility across different client machines. That being said, downloading Dehko will require the installation of all dependencies. If you do not wish to do this manually, simply choose the appropriate installation executable depending on your operating system. 

Instead, if you wish to develop later on 

## Customization
After downloading Dehko, there should be a modifiable JSON file with the exact name "configurations.JSON." Roughly, the format of the file should look something like the following: 

```python
{
command:"type", 
phrases: ['phrase 1', 'p2', 'phrase-3'],
script: "scripts/command1"
}
```

Modify the JSON file to create the new command type, associated phrases with that command type, and the path of the script that you wish to run whenever that command is called. For the sake of organization, we recommend putting all of your custom scripts within a new directory named `scripts`.

After doing all of this, run the following commands within your terminal. 
```console
foo@bar:~$ dehko train

Cleaning and Reoptimizing Dehko!

PROGRESS: [40%] [##########......................................]
Estimated Time Remaining: 300 ms.
```
d `~$ dehko retrain` so that the program is able to retrain the Neural Net model with the updated data for classification and dumps the model for quick performance. 
 

### Directory Structure

Here is a overview of the structure of this repository.


### Licensing 

Dehko is released under the MIT license. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

---------

#### References 
- https://github.com/openai/gym
- https://github.com/commaai/openpilot
- https://github.com/tensorflow/tensorflow
- https://machinelearningmastery.com/a-gentle-introduction-to-serialization-for-python/
- https://www.deanishe.net/alfred-workflow/guide/serialization.html
- https://hazelcast.com/blog/a-hitchhikers-guide-to-caching-patterns/
