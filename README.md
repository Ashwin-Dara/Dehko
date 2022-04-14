# Dehcko - Overview 

References: 
https://github.com/openai/gym


## Table of Contents 
- What is Dehcko?
- Discord Channel Installation and Examples
- Open Source and Contribution 
- Testing and Reporting Feedback
- Directory Structure
- Licensing

### What is Dehcko?

Dehcko is an NLP smart assistant built for discord that is able to take in natural language in the form of textual expressions and efficiently parse, detect, and classify the corresponding appropriate command the user intends to complete. Currently, core functionality of Dehcko includes being able to play music, give weather forecasts, set reminders, curate radio playlists, etc. Much more can be done by modifying the appropriate JSON command "settings" file and creating a corresponding "action" function. More details are described in ** Open Source and Contribution **. 

#### Video Overview


--------------- 


### Discord Channel Installation and Examples

To add Dehcko to your server without the intent of modifying the project, please go to the Dehcko landing page and follow the installation procedure. Installation is as simple as clicking the directed button and allowing Dehko admin privledges for the intended Discord community.

To use Dehcko requires no additional configuration other than installation. Just install and add the bot to the appropriate server. However, commands will require 

### Open Source and Contribution 

To contribute to this project, 

### Testing and Reporting Feedback 

With Dehcko comes an organized dashboard to represent key information abo

### Directory Structure 

### Licensing 

#### References 

https://github.com/openai/gym
https://github.com/commaai/openpilot
https://github.com/tensorflow/tensorflow
 









## Utils - Design Features 
- Will be able to play music from YouTube
- Example commands. `please play music ~link` `play music ~link` `could you please tune a jam ~link`
- It will be inconveniant in terms of user design if they cant play music without the link 

FEATURE: play music based on the song. Will need to play the top result from the name. This is low priority. 
FEATURE: curate playlists from YouTube API. Alongside a recommendation system, this would be very good. 
FEATURE: Will send nice dashboard of the current song that is playing (maybe try to retrieve more information from spotify? Need to figure out how to send a nicely formatting image that retrieves the thumbnail and everything) 

## Weather 
- Example commands `what is the temperature` 
- Output: should give a nice visual dashboard depending on the area that you are in. It will give day's forecast by default. 

## Radio 
- curate the playlist 

## Reminders
- make this an exact command. Should not be something left to NLP/Classification.
`~remind 1hr "tell me to check this"`
`~remind 1:30hr "Check the forecast"`
