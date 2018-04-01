# Chores Assigner
## Overview
In my house, each of the 22 residents does one day of chores a week. This program uses the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) to optimally assign people to a chores team based on their preferences.

Each resident gives each day a preference through a Google form. The options are:
* This day does not work for me at all
* I don't like this day, but can do it as a last resort
* This day is okay for me
* This day is great for me

The CSV results of the Google form is the input to the program. Each preference is translated to a numerical cost, a cost matrix is formed, and then [scipy's implementation](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html) of the Hungarian algorithm is used to find an optimal assignment. Finally, this is written to a CSV file.

## Usage
```
chores_assigner.py <input_file_path> <output_file_path>
```
Where both `input_file_path` and `output_file_path` are paths to CSV files. `output_file_path` doesn't need to exist at runtime; the code will create it if it doesn't exist or otherwise overwrite it.
