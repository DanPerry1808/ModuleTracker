# Returns the number of completed assessments for the module given
def get_completed_assess(mod):
    completed = 0
    for assess in mod["assessments"]:
        if assess["complete"]:
            completed += 1
    return completed
