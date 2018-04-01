import sys
import csv
from datetime import datetime

from scipy.optimize import linear_sum_assignment
import numpy as np

DAY_NAMES = ["monday", "tuesday", "wednesday",
             "thursday", "friday", "saturday"]
MAX_PEOPLE_PER_DAY = 5


def main():
    if len(sys.argv) < 3:
        raise IndexError(
            "No arguments provided.\nUsage: chores_assigner.py <input_file_path> <output_file_path>")

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    people = _get_people(input_file_path)

    # Create a cost matrix
    # Each row represents a person
    # Each column represents a slot on that day's team
    cost_matrix = np.zeros([len(people), MAX_PEOPLE_PER_DAY*len(DAY_NAMES)])

    # Populate the cost matrix
    for i, person in enumerate(people):
        for j, day in enumerate(person.costs):
            day_start = j*MAX_PEOPLE_PER_DAY
            day_end = j*MAX_PEOPLE_PER_DAY+MAX_PEOPLE_PER_DAY
            cost_matrix[i, day_start:day_end] = person.costs[day]

    # Use the Hungarian algorithm to solve the assignment
    optimal_assignments = linear_sum_assignment(cost_matrix)

    # Find total cost
    cost = cost_matrix[optimal_assignments[0], optimal_assignments[1]].sum()

    # Interpret assignments
    optimal_assignments = zip(optimal_assignments[0], optimal_assignments[1])

    with open(output_file_path, "w+") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Name", "Assignment", "Cost"])
        for person_index, day_index in optimal_assignments:
            person = people[person_index]
            day = DAY_NAMES[int(day_index / 5)]
            csvwriter.writerow([person.name, day, person.costs[day]])


def _get_people(file_path):
    people = []
    with open(file_path) as f:
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

    return people


def _preference_cost(pref):
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
