# Prints the prompt and gets input from the user
# Only accepts an integer
def int_input(prompt=None):
    value = 0
    while True:
        if prompt != None:
            print(prompt)
        try:
            value = int(input("> "))
            break
        except ValueError:
            print("Error: Enter an integer value")
    return value

# Prints the prompt and gets input from the user
# Only accepts a float
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
