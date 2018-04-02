import sys
import csv

from assigners import ChoresAssigner

def main():
    if len(sys.argv) < 3:
        raise IndexError(
            "No arguments provided.\nUsage: chores_assigner.py <input_file_path> <output_file_path>")

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    MAX_PEOPLE_PER_DAY = 4
    
    # Read in input file and get a list of people and their preferences
    people = []
    with open(input_file_path) as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            name = row[1]
            pref_list = row[2:8]
            costs = {}
            for i, pref in enumerate(pref_list):
                costs[DAY_NAMES[i]] = _preference_cost(pref)
            person = Person(name, costs)
            people.append(person)

    assigner = ChoresAssigner(DAY_NAMES, MAX_PEOPLE_PER_DAY)
    optimal_assignments, cost = assigner.hungarian(people)

    teams = {}
    # Output assignments to CSV
    with open(output_file_path, "w+") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Name", "Assignment", "Cost"])
        for person_index, day_index in optimal_assignments:
            person = people[person_index]
            day = DAY_NAMES[int(day_index / MAX_PEOPLE_PER_DAY)]
            if day in teams:
                teams[day].append(person.name)
            else:
                teams[day] = [person.name]
            csvwriter.writerow([person.name, day, person.costs[day]])

    for day in DAY_NAMES:
        print("{0}:".format(day))
        for person in teams[day]:
            print("\t{0}".format(person))

def _preference_cost(pref):
    '''
    Translate a survey response (text) into a numerical cost. This is the subjective part of the assignment.

    As far as I can tell, scipy's implementation of the Hungarian algorithm doesn't require the costs to be positive. However, it's a good choice to have your most minimally optimal response set at 0 so that your "goal" (minimal optimality * number of people) doesn't scale with number of people. One less thing to think about.

    Future versions of this function should read in from a CSV file to expose an interface for setting the responses and values.
    '''
    if pref == "I don't like this day, but can do it as a last resort.":
        return 100
    elif pref == "This day is okay for me.":
        return 20
    elif pref == "This day is great for me!":
        return 0
    elif pref == "This day does not work for me at all. PLEASE ONLY USE THIS FOR LEGITIMATE REASONS":
        return 1000
    else:
        raise ValueError("Found invalid preference text: {0}".format(pref))

class Person:
    name = ""
    costs = {}

    def __init__(self, name, costs):
        self.name = name
        self.costs = costs

    def __str__(self):
        return self.name


if __name__ == "__main__":
    main()
