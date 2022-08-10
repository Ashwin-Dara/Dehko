# Contains a mapping of the action defined within settings.JSON to the appropriate function that needs to be executed. 
# The mapping format is the following: key is the name of the action while the value is the function that will be executed. 
# The current functions (lambda x : 0) are place holders to be re-defined with the user. All actions can be written in 
# this file and then added to the mapping accordingly. 

command_to_func_mapping = \
    {"web-workflow" : (lambda x: 0),
    "weather": (lambda x: 0),
    "music": (lambda x: 0)}
