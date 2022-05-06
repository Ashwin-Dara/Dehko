## Dehcko
Dehko is an NLP smart assistant tool built for your terminal to easily define custom automation macros without worrying about the particular syntax. Type in a description of the task you wish to run, and Dehko will automatically classify natural language to the corresponding intended command. Dehko allows you to eliminate the baggage that comes with the strict precision currently required for many CLI tools. Commands and intents are highly configurable, and can be done by modifying a JSON configuration file. More details are described in ** Customization **. 

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

[PROGRESS] #########----------------
Status: 40%. Estimated Time: 300 ms.
```
d `~$ dehko retrain` so that the program is able to retrain the Neural Net model with the updated data for classification and dumps the model for quick performance. 
 


### Installation

To add Dehcko to your server without the intent of modifying the project, please go to the Dehcko landing page and follow the installation procedure. Installation is as simple as clicking the directed button and allowing Dehko admin privledges for the intended Discord community.

To use Dehcko requires no additional configuration other than installation. Just install and add the bot to the appropriate server. However, commands will require 

### Directory Overview

### Customization

To contribute to this project, 

### Development

### Testing and Reporting Feedback 

With Dehcko comes an organized dashboard to represent key information abo

### Licensing 

Dehko is released under the MIT license. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#### References 

https://github.com/openai/gym
https://github.com/commaai/openpilot
https://github.com/tensorflow/tensorflow
 









### Utils - Design Features 
- Will be able to play music from YouTube
- Example commands. `please play music ~link` `play music ~link` `could you please tune a jam ~link`
- It will be inconveniant in terms of user design if they cant play music without the link 

FEATURE: play music based on the song. Will need to play the top result from the name. This is low priority. 
FEATURE: curate playlists from YouTube API. Alongside a recommendation system, this would be very good. 
FEATURE: Will send nice dashboard of the current song that is playing (maybe try to retrieve more information from spotify? Need to figure out how to send a nicely formatting image that retrieves the thumbnail and everything) 

#### Weather 
- Example commands `what is the temperature` 
- Output: should give a nice visual dashboard depending on the area that you are in. It will give day's forecast by default. 

#### Radio 
- curate the playlist 

#### Reminders
- make this an exact command. Should not be something left to NLP/Classification.
`~remind 1hr "tell me to check this"`
`~remind 1:30hr "Check the forecast"`


## Serialization and Caching

Since the program is mainly event driven and to prevent resources from being lost in the background once we are done with a particular task, serialization is carefully employed to store core information. In particular, after the classification model is trained and optimized, we serialize the model for convenient accessibility once the program ends. Moreover, important mappings that were recovered through the formatting is recovered as well. No time is ever wasted doing time-consuming tasks that have already been once done before! We use the "pickle" python library in order to serialize. 

### Relevant Readings
- https://machinelearningmastery.com/a-gentle-introduction-to-serialization-for-python/
- https://www.deanishe.net/alfred-workflow/guide/serialization.html
- https://hazelcast.com/blog/a-hitchhikers-guide-to-caching-patterns/
