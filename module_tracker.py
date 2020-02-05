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
    print("----------")
    for i, mod in enumerate(current_set["modules"], start=1):
        assess_complete = info.get_completed_assess(mod)
        print(str(i) + ") " + mod["name"])
        print(str(mod["credits"]) + " credits")
        print(str(assess_complete) + "/" + str(len(mod["assessments"])) + " assessments completed")
        print()

# Allows the user to choose one of the modules from the currently loaded set
# Returns the index of the chosen module in the current_set["modules"] list
def choose_module():
    print()
    print("Enter the number of the module you want to select")
    for i, mod in enumerate(current_set["modules"], start=1):
        print(str(i) + ") " + mod["name"])
    choice = -1
    num_mods = len(current_set["modules"])
    while choice < 1 or choice > num_mods:
        choice = user_io.int_input()
    return choice - 1

# Allows the user to choose one of the assessment from the module with the
# given index in current_set
# Returns the index of the chosen assessment in the module["assessment"] list
def choose_assessment(mod_index):
    print()
    print("Enter the number of the assessment you want to select")
    for i, assess in enumerate(current_set["modules"][mod_index]["assessments"], start=1):
        print(str(i) + ") " + assess["name"])
    choice = -1
    num_assess = len(current_set["modules"][mod_index]["assessments"])
    while choice < 1 or choice > num_assess:
        choice = user_io.int_input()
    return choice - 1

# Allows the user to change the details of a module then rewrites that to the file
def edit_module(index):
    print()
    print("Currently editing: " + current_set["modules"][index]["name"])
    print("Please enter the number of the option you want: ")
    print("1) Edit module name")
    print("2) Edit number of credits")
    
    # Allow user to choose which attribute to change
    choice = -1
    while choice < 1 or choice > 2:
        choice = user_io.int_input()
    
    # Name changing
    if choice == 1:
        new_name = ""
        while new_name == "":
            print("Enter the new module name:")
            new_name = input("> ")
        
        current_set["modules"][index]["name"] = new_name
    else:
        # Credit amount changing
        new_creds = -1
        while new_creds < 0:
            new_creds = user_io.int_input("Enter the new number of credits")
            current_set["modules"][index]["credits"] = new_creds

    # Rewrites file
    filepath = file_io.get_filepath(current_set["name"])
    file_io.write_json_file(filepath, current_set)

# Allows the user to edit an attribute of one assessment
def edit_assess(mod_index, assess_index):
    current_mod = current_set["modules"][mod_index]
    current_assess = current_mod["assessments"][assess_index]
    print()
    print("Currently editing " + current_mod["assessments"][assess_index]["name"] + " in " + current_mod["name"])
    print("Please enter the number of the option you want:")
    print("1) Edit assessment name")
    print("2) Edit assessment weight")
    
    if current_assess["complete"]:
        print("3) Edit mark")
    else:
        print("3) Set mark")

    print("4) Edit maximum mark")

    if current_assess["complete"]:
        print("5) Reset as incomplete")

    max_choice = -1
    if current_assess["complete"]:
        max_choice = 5
    else:
        max_choice = 4
    
    choice = -1
    while choice < 1 or choice > max_choice:
        choice = user_io.int_input()
    
    if choice == 1:
        new_name = ""
        while new_name == "":
            print()
            print("Enter new module name:")
            new_name = input("> ")
        
        current_set["modules"][mod_index]["assessments"][assess_index]["name"] = new_name
    elif choice == 2:
        weight1 = 0
        weight2 = 0

        while not valid_weight(weight1, weight2):
            weight1 = user_io.int_input("Enter weight fraction numerator:")
            weight2 = user_io.int_input("Enter weight fraction denominator:")
        current_set["modules"][mod_index]["assessments"][assess_index]["weight_fraction"] = [weight1, weight2]
    elif choice == 3:
        mark = -1
        while mark < 0 or mark > current_assess["max_mark"]:
            mark = user_io.float_input("Enter the mark for this assessment:")
        current_set["modules"][mod_index]["assessments"][assess_index]["mark"] = mark
        current_set["modules"][mod_index]["assessments"][assess_index]["complete"] = True
    elif choice == 4:
        max_mark = -1
        while max_mark < 0:
            max_mark = user_io.float_input("Enter the maximum mark for this assessment:")
        current_set["modules"][mod_index]["assessments"][assess_index]["max_mark"] = max_mark
    elif choice == 5:
        # Resetting the assessment as incomplete will set complete to false and mark to 0
        current_set["modules"][mod_index]["assessments"][assess_index]["mark"] = 0
        current_set["modules"][mod_index]["assessments"][assess_index]["complete"] = False
    
    # Rewrites file
    filepath = file_io.get_filepath(current_set["name"])
    file_io.write_json_file(filepath, current_set)


# Prints list of possible commands
def help():
    print()
    print("COMMAND LIST")
    print("----------")
    print("create <name> - Creates a new module set with the given name")
    print("editassess - Allows you to edit the details of an assessment")
    print("editmod - Allows you to edit the details of a module")
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

    # Continually take in user commands
    while True:
        print()
        print("Type 'help' for a command list, or enter a command below:")
        command = input("> ")

        # Help command displays list of commands
        if command == "help":
            help()
        # List command displays all module sets in the saves folder
        elif command == "list":
            file_io.list_saves()
        # Displays the name of the currently loaded module set
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
        # Infomods command prints out info about currently loaded modules
        elif command == "infomods":
            if loaded:
                print_module_info()
            else:
                print("No module loaded. No information to show.")
        # Editmod command allows you to edit attributes of a module
        elif command == "editmod":
            if loaded:
                selected_mod = choose_module()
                edit_module(selected_mod)
            else:
                print("Cannot edit module. No module set is loaded.")
        # Editassess command allows you to edit attributes of an assessment
        elif command == "editassess":
            if loaded:
                selected_mod = choose_module()
                selected_assess = choose_assessment(selected_mod)
                edit_assess(selected_mod, selected_assess)
            else:
                print("Cannot edit assessment. No module set is loaded")
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
