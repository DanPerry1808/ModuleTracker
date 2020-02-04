
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
    print("File read successfully")
    return mod_set

def create_json_file(filepath, mod_set):
    with open(filepath, "w") as f:
        f.write(json.dumps(mod_set))
    print("File created successfully")

def list_saves():
    for file in os.listdir("saves/"):
        if file.endswith(".json"):
            print(file[:-5])

def int_input(prompt):
    value = 0
    while True:
        print(prompt)
        try:
            value = int(input("> "))
            break
        except ValueError:
            print("Error: Enter an integer value")
    return value

def float_input(prompt):
    value = 0
    while True:
        print(prompt)
        try:
            value = float(input("> "))
            break
        except ValueError:
            print("Error: Enter a number")
    return value
    

# Prompts the user to enter either Y or N
# Returns True on Y and False on N
def bool_input(prompt):
    choice = "Q"
    while choice not in ("Y", "N"):
        print(prompt)
        choice = input("> ")

    if choice == "Y":
        return True
    else:
        return False

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
        weight1 = int_input("Enter weight fraction numerator:")
        weight2 = int_input("Enter weight fraction denominator:")
    assessment["weight_fraction"] = [weight1, weight2]

    max_mark = -1
    while max_mark < 0:
        max_mark = float_input("Enter the maximum mark for this assessment:")
    assessment["max_mark"] = max_mark

    if bool_input("Has this assessment been completed?"):
        assessment["complete"] = True
        mark = -1
        while mark < 0 or mark > max_mark:
            mark = float_input("Enter the mark achieved in this assessment:")
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
        credits = int_input("Enter the number of credits this module is worth:")
    module["credits"] = credits

    module["assessments"] = []

    while True:
        module["assessments"].append(add_new_assessment())

        if not bool_input("Would you like to add another assessment? (Y/N)"):
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

        if not bool_input("Would you like to add another module/ (Y/N)"):
            break
    
    return module_set

def help():
    print("create <name> - Creates a new module set with the given name")
    print("list - Lists all available module sets")
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
        elif command == "list":
            list_saves()
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
                print("Error: Please provide a file name for the 'load' command")

        if command_split[0] == "create":
            if len(command_split) == 2:
                filepath = os.path.join("saves/" + command_split[1] + ".json")
                if not os.path.isfile(filepath):
                    mod_set = create_module_set(command_split[1])
                    create_json_file(filepath, mod_set)
                else:
                    print("Error: Module set with that name already exists")
            else:
                print("Error: Please provide a file name for the 'create' command")