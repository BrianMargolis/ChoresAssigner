from scipy.optimize import linear_sum_assignment
import numpy as np

class ChoresAssigner:
    def __init__(self, day_names, max_people_per_day):
        self.day_names = day_names
        self.max_people_per_day = max_people_per_day

    def hungarian(self, people):
        # Create a cost matrix
        # Each row represents a person
        # Each column represents a slot on that day's team
        cost_matrix = np.zeros([len(people), self.max_people_per_day*len(self.day_names)])

        # Populate the cost matrix
        for i, person in enumerate(people):
            for j, day in enumerate(person.costs):
                day_start = j*self.max_people_per_day
                day_end = (j+1)*self.max_people_per_day
                cost_matrix[i, day_start:day_end] = person.costs[day]

        # Use the Hungarian algorithm to solve the assignment
        optimal_assignments = linear_sum_assignment(cost_matrix)

        # Find total cost, not currently used for anything
        cost = cost_matrix[optimal_assignments[0], optimal_assignments[1]].sum()

        # Provide a more reasonable structure:
        # list of (person index, assigned day index)
        optimal_assignments = zip(optimal_assignments[0], optimal_assignments[1])
        return optimal_assignments, cost


    def ford_fulkerson(self, people):
        pass