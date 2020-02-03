
import json
import os

class ModuleList:

    def __init__(self, name, mods):
        """
        name: String - identifier for this list of modules
        mods: Module[] - the list of modules
        """
        self.name = name
        self.modules = mods

class Module:

    def __init__(self, name, credits, assessments):
        """
        name: String - Name of this module
        credits: Int - Number of credits the module is worth
        assessments: Assessment[] - The marked assessments in this module
        """
        self.name = name
        self.credits = credits
        self.assessments = assessments

class Assessment:

    def __init__(self, name, weight, max_marks, marks = 0, complete = False):
        """
        name: String - Name of this assessment
        weight: Int - The percentage this assessment is worth to the module
        max_marks: Int - The maximum number of marks you can get
        marks: Int - The actual number of marks achieved
        complete: Boolean - Whether this assessment has been completed yet
        """
        self.name = name
        self.weight = weight
        self.max_marks = max_marks
        self.marks = marks
        self.complete = complete

def load_json_file(filepath):
    with open(filepath, "r") as f:
        mod_set = json.loads(f.read())
    return mod_set

def help():
    print("list - Lists all available module sets")
    print("create <name> - Creates a new module set with the given name")
    print("load <name> - Loads the module set with that name")
    print("quit - Exits the program")

# Program entry point
if __name__ == "__main__":
    print("Module Viewer V0.1")
    print("-------------------")
    print("Type 'help' for a command list, or enter a command below:")
    # Continually take in user commands
    while True:
        command = input("> ")

        # Help command displays list of commands
        if command == "help":
            help()
        # Quit command exits the program
        elif command == "quit":
            quit()

        # Commands with arguments need to be split up into a list
        command_split = command.split()

        # Load command loads a module set from a JSON file
        if command_split[0] == "load":
            # Check additonal argument is provided
            if len(command_split) == 2:
                # Check file actually exists
                filepath = os.path.join("saves/" + command_split[1] + ".json")
                if os.path.isfile(filepath):
                    load_json_file(filepath)
                else:
                    print("Error: Could not find a json file at " + filepath)
            else:
                print("Error: Please provide a name for the load command")