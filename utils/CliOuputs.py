# To enable multi-line formatting and avoid clutter, relevant statements and information 
# about the CLI (such as the help message and the training status) were grouped into this file. 

no_arguments_input = '''Dehko (1.02)

There were not enough arguments for Dehko to understand! Please type in a description of the script you wish to run. 
For a more detailed description, please type `dehko -h`'''

training_output = '''Dehko (1.02)

Retraining Dehko to reflect updates made in settings.json & enhance classification accuracy!\n'''

help_output = '''Dehko (1.02) is an open-source program to simplify the management and execution of automation scripts. Here's a quick overview of the usage to help you get started: 

Usages:
	dehko "<Description of Script Phrases>" :
		Will execute the script corresponding to the description you provide. Must be enclosed in quotes. 
	
	dehko --train :
		Will retrain the neural net to reflect any changes in the settings.json file. 

	dehko --help : 
		Opens the help prompt providing general information about the usage of dehko. 

	dehko -h: 
		Concise usage of the --help command, which opens the informational panel. 

To learn more about customization, contributions, and modifying Dehko, please visit our GitHub: https://github.com/Ashwin-Dara/Dehko.\n'''