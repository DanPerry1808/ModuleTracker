
import json

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

# Program entry point
if __name__ == "__main__":
    print("Hello world")
    print("1) Load existing modules")
    print("2) Create new set of modules")
    print("3) Quit")

    choice = -1
    while choice < 1 or choice > 3:
        try:
            choice = int(input("> "))
        except ValueError:
            print("Enter a number between 1 and 3")

    if choice == 1:
        pass
    if choice == 2:
        pass
    if choice == 3:
        print("Goodbye")
        quit()