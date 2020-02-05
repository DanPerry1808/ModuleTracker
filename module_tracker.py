import sys
import os
import file_io
import user_io
import module_info as info

# Whether there is a module set currently loaded
loaded = False
# The currently loaded module set
current_set = dict()

# Checks if the weight fraction for an assessment is valid
def valid_weight(weight1, weight2):
    # Cannot divide by zero
    if weight2 == 0:
        return False
    
    value = weight1 / weight2

    # Cannot be negative
    if value < 0:
        return False
    
    # Cannot be greater than 1 (100%)
    if value > 1:
        return False

    return True

# Creates a new assessment as a dictionary
def add_new_assessment():
    print()
    print("----------")
    print("Adding new assessment")

    assessment = dict()
    name = ""
    while name == "":
        print("Enter assessment title: ")
        name = input("> ")
    assessment["name"] = name

    weight1 = 0
    weight2 = 0

    while not valid_weight(weight1, weight2):
        weight1 = user_io.int_input("Enter weight fraction numerator:")
        weight2 = user_io.int_input("Enter weight fraction denominator:")
    assessment["weight_fraction"] = [weight1, weight2]

    max_mark = -1
    while max_mark < 0:
        max_mark = user_io.float_input("Enter the maximum mark for this assessment:")
    assessment["max_mark"] = max_mark

    if user_io.bool_input("Has this assessment been completed?"):
        assessment["complete"] = True
        mark = -1
        while mark < 0 or mark > max_mark:
            mark = user_io.float_input("Enter the mark achieved in this assessment:")
    else:
        assessment["complete"] = False
        mark = 0
    assessment["mark"] = mark

    return assessment

def add_new_module():
    print()
    print("----------")
    print("Adding new module")

    module = dict()
    name = ""
    while name == "":
        print("Enter module name: ")
        name = input("> ")
    module["name"] = name

    credits = -1
    while credits < 0:
        credits = user_io.int_input("Enter the number of credits this module is worth:")
    module["credits"] = credits

    module["assessments"] = []

    while True:
        module["assessments"].append(add_new_assessment())

        if not user_io.bool_input("Would you like to add another assessment? (Y/N)"):
            break

    return module

def create_module_set(name):
    # Create empty dictionary to store module details
    module_set = dict()
    module_set["name"] = name
    module_set["modules"] = []

    print()
    print("-------------")
    print("Creating new module set called " + name)

    # Keep adding new modules until the users says to stop
    while True:
        module_set["modules"].append(add_new_module())

        if not user_io.bool_input("Would you like to add another module/ (Y/N)"):
            break
    
    return module_set

def load_mod_set(name):
    # Check file actually exists
    filepath = file_io.get_filepath(name)
    if os.path.isfile(filepath):
        global current_set
        global loaded
        current_set = file_io.load_json_file(filepath)
        loaded = True
    else:
        print("Error: Could not find a json file at " + filepath)

# Outputs the following information about each module in the currently loaded set:
# Name, number of assessments completed
def print_module_info():
    print()
    print("Information on modules in set " + current_set["name"])
    for i, mod in enumerate(current_set["modules"], start=1):
        assess_complete = info.get_completed_assess(mod)
        print(str(i) + ") " + mod["name"])
        print(str(assess_complete) + "/" + str(len(mod["assessments"])) + " assessments completed")
        print()

def help():
    print()
    print("COMMAND LIST")
    print("----------")
    print("create <name> - Creates a new module set with the given name")
    print("list - Lists all available module sets")
    print("load <name> - Loads the module set with that name")
    print("loaded - Prints the name of the currently loaded module set")
    print("infomods - Prints information on the modules in the set currently loaded")
    print("unload - Removes the currently loaded module set from memory")
    print("quit - Exits the program")

# Program entry point
if __name__ == "__main__":
    print("Module Viewer V0.1")
    print("-------------------")

    # If user gives name of file to load in arguments, load it
    if(len(sys.argv) == 2):
            load_mod_set(sys.argv[1])

    print("Type 'help' for a command list, or enter a command below:")
    # Continually take in user commands
    while True:
        command = input("> ")

        # Help command displays list of commands
        if command == "help":
            help()
        elif command == "list":
            file_io.list_saves()
        elif command == "loaded":
            print()
            print("Currently loaded module set:")
            if loaded:
                print(current_set["name"])
            else:
                print("No module set loaded")
        # Unload command removes the currently selected module from memory
        elif command == "unload":
            loaded = False
            current_set = dict()
            print()
            print("Unloaded module set.")
        elif command == "infomods":
            if loaded:
                print_module_info()
            else:
                print("No module loaded. No information to show.")
        # Quit command exits the program
        elif command == "quit":
            quit()

        # Commands with arguments need to be split up into a list
        command_split = command.split()

        # Load command loads a module set from a JSON file
        if command_split[0] == "load":
            # Check additonal argument is provided
            if len(command_split) == 2:
                load_mod_set(command_split[1])
            else:
                print("Error: Please provide a file name for the 'load' command")

        # Create command makes a new module set file
        if command_split[0] == "create":
            # Check name argument is provided
            if len(command_split) == 2:
                # Check if file already exists (do not overwrite)
                filepath = file_io.get_filepath(command_split[1])
                if not os.path.isfile(filepath):
                    mod_set = create_module_set(command_split[1])
                    file_io.write_json_file(filepath, mod_set)
                else:
                    print("Error: Module set with that name already exists")
            else:
                print("Error: Please provide a file name for the 'create' command")