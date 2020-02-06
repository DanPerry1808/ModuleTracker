# Returns the number of completed assessments for the module given
def get_completed_assess(mod):
    completed = 0
    for assess in mod["assessments"]:
        if assess["complete"]:
            completed += 1
    return completed

# Returns the percentage from the marks gotten for a given assessment
def get_assess_percentage(assess):
    return (assess["mark"] * 100) / assess["max_mark"]

# Converts a percentage into the equivalent uni grade
def perc_to_grade(perc):
    if perc >= 70:
        return "1"
    elif perc >= 60:
        return "2:1"
    elif perc >= 50:
        return "2:2"
    elif perc >= 40:
        return "3"
    else:
        return "Fail"

# Calculates the average grade of all completed assessments in a module
# If no assessments complete, returns None to avoid divide by zero error
def get_average_grade(mod):
    grade = 0
    num_assess = 0
    for assess in mod["assessments"]:
        if assess["complete"]:
            num_assess += 1
            grade += get_assess_percentage(assess)

    if num_assess > 0:
        return round(grade / num_assess, 1)
    else:
        return None

# Gets the total grade so far based on complete assessments
def get_total_perc(mod):
    grade = 0
    for assess in mod["assessments"]:
        weight_list = assess["weight_fraction"]
        weight = weight_list[0] / weight_list[1]
        grade += get_assess_percentage(assess) * weight
    return round(grade, 1)

def get_perc_lost(mod):
    perc = 0
    for assess in mod["assessments"]:
        if assess["complete"]:
            weight_list = assess["weight_fraction"]
            weight = weight_list[0] / weight_list[1]
            perc += (100 - get_assess_percentage(assess)) * weight
    return round(perc, 1)

# Gets the percentage of the module made up of uncompleted assessments
def get_uncomplete_perc(mod):
    perc = 0
    for assess in mod["assessments"]:
        if not assess["complete"]:
            weight_list = assess["weight_fraction"]
            weight = weight_list[0] / weight_list[1]
            perc += weight * 100
    return round(perc, 1)
