import user_io
import file_io

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

        if not user_io.bool_input("Would you like to add another module? (Y/N)"):
            break
    
    return module_set

# Allows the user to change the details of a module then rewrites that to the file
def edit_module(current_set, index):
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
    return current_set

# Allows the user to edit an attribute of one assessment
def edit_assess(current_set, mod_index, assess_index):
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
    return current_set
