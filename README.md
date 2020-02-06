# Module Tracker
A CLI to track progress in university modules.

## Installation and running the program
1) Ensure you have Python 3 installed
2) Download the zip file and extract it
3) Open the terminal/command line on your computer and get python to run the `module_tracker.py` script. (Eg. on Linux `python3 module_tracker.py`)
3a) As an optional step, you can specify a module set to load from the command line by specifying the name of the module set after the file name (Eg. `python3 module_tracker.py first_year`)
4) On first start-up, you will probably want to either run the `help` command or create a module using the `create <name>` command.

## Command List
- `create <name>` - Creates a new module set with the given name
- `editassess` - Allows you to edit the details of an assessment
- `editmod` - Allows you to edit the details of a module
- `help` - Prints this help dialog
- `list` - Lists all available module sets
- `load <name>` - Loads the module set with that name
- `loaded` - Prints the name of the currently loaded module set
- `infomods` - Prints information on the modules in the set currently loaded
- `unload` - Removes the currently loaded module set from memory
- `quit` - Exits the program

## Tutorial: How to create a module set
1) `create set` will create a module_set called 'set'
2) You will now create the first module in the set, the program will ask you for a name and number of credits it is worth
3) Now you will need to add the individual assessments for that module. You will need to enter a name, it's weight towards the module's marking (this will need to be given as a fraction, with the top part entered first, then the bottom one), and the maximum mark. The program will ask if this assessment has been completed. If it has, you can enter the mark you got for it.
4) You can now add as many additional assessments to the module as you want
5) After finishing that module, you can then add as many other modules as you want to the module set
6) When you are done, the module set will be saved to a file. You can then load this module set using the `load` command.