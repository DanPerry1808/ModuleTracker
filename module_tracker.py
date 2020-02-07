import sys
import os
import file_io
import user_io
import module_set as ms
import module_info as info

# Whether there is a module set currently loaded
loaded = False
# The currently loaded module set
current_set = dict()

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

# Given a percentage out of 100, converts this into a bar of hashes and hyphens
# to form a progress bar
def print_perc_bar(perc):
    length = 20
    conv_rate = length / 100
    num_hashes = round(conv_rate * perc)
    print("[", end="")
    for i in range(length):
        if i < num_hashes:
            print("#", end="")
        else:
            print("-", end="")
    print("]")

# Given the percentage of marks gotten and the percentage of marks lost, outputs
# this into a progres bar of hashes, hyphens and crosses
def print_progress_bar(perc_got, perc_lost):
    length = 20
    conv_rate = length/100
    num_hashes = round(conv_rate * perc_got)
    num_crosses = round(conv_rate * perc_lost)
    print("[", end="")

    for i in range(length):
        if i < num_hashes:
            print("#", end="")
        elif i >= length - num_crosses:
            print("X", end="")
        else:
            print("-", end="")
    print("]")

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
        if assess_complete > 0:
            av_grade = info.get_average_grade(mod)
            print("Average percentage: " + str(av_grade) + "%")
            print("Grade: " + info.perc_to_grade(av_grade))
            print_perc_bar(av_grade)
            print()

            total_grade = info.get_total_perc(mod)
            perc_lost = info.get_perc_lost(mod)
            
            perc_to_pass = round(40 - total_grade, 1)
            if perc_to_pass < 0:
                perc_to_pass = 0
            
            print("Total percentage so far: " + str(total_grade) + "%")
            print("Grade so far: " + info.perc_to_grade(total_grade))
            print_progress_bar(total_grade, perc_lost)
            highest_poss = info.get_uncomplete_perc(mod) + total_grade
            # This figure has to be rounded to prevent floating point rounding error
            print("Highest possible percentage: " + str(round(highest_poss, 1)) + "%")
            print("Highest possible grade: " + info.perc_to_grade(highest_poss))
            print("Total percentage needed from to pass: " + str(perc_to_pass) + "%")
        print()

    print("Credits achieved based on current averages: " + str(info.get_average_credits(current_set)))
    print("Credits achieved based on marks entered so far: " + str(info.get_total_credits(current_set)))

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

# Prints list of possible commands
def help():
    print()
    print("COMMAND LIST")
    print("----------")
    print("create <name> - Creates a new module set with the given name")
    print("editassess - Allows you to edit the details of an assessment")
    print("editmod - Allows you to edit the details of a module")
    print("help - Prints this help dialog")
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
        command_split = command.split()

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
                current_set = ms.edit_module(current_set, selected_mod)
            else:
                print("Cannot edit module. No module set is loaded.")
        # Editassess command allows you to edit attributes of an assessment
        elif command == "editassess":
            if loaded:
                selected_mod = choose_module()
                selected_assess = choose_assessment(selected_mod)
                current_set = ms.edit_assess(current_set, selected_mod, selected_assess)
            else:
                print("Cannot edit assessment. No module set is loaded")
        # Quit command exits the program
        elif command == "quit":
            quit()

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
                    mod_set = ms.create_module_set(command_split[1])
                    file_io.write_json_file(filepath, mod_set)
                else:
                    print("Error: Module set with that name already exists")
            else:
                print("Error: Please provide a file name for the 'create' command")
