import datetime
import numpy as np
from collections import defaultdict
#===================================================================================================================================

# distance between monkeys
def euc_d(x1,y1, x2,y2):
  return np.sqrt(np.sum((x1 - x2)**2 + (y1 - y2)**2))
#===================================================================================================================================


# read and process the file
def read_monkey_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines in the file

    # Extract the first row as headers
    headers = lines[0].strip().split(',')

    # Initialize a list to hold the data
    monkey_data = []

    # Process each line after the header
    for line in lines[1:]:
        values = line.strip().split(',')
        monkey_record = dict(zip(headers, values))
        monkey_data.append(monkey_record)

    return monkey_data
#===================================================================================================================================

# # of digits wanna keep, (Monkey[''], 3) the 3 indicates # of digits
def truncate_coordinates(data):
    for monkey in data:
        monkey['x'] = round(float(monkey['x']), 3)
        monkey['y'] = round(float(monkey['y']), 3)
#===================================================================================================================================

# check if monkey is in the box, subfunction of find_pairs
def is_within_box(x, y, box):
    """Check if the point (x, y) is within the defined box."""
    (x_min, y_min), (x_max, y_max) = box
    return x_min <= x <= x_max and y_min <= y <= y_max
#===================================================================================================================================

# find pairs _ bad time complexity -> use the optimized version
def find_pairs_within_box(data, box):
    pairs = []
    time_format = "%d-%b-%Y %H:%M:%S"

    # Convert all times in data to datetime objects for easier comparison
    for monkey in data:
        monkey['time'] = datetime.datetime.strptime(monkey['time'], time_format)

    # Compare each monkey with every other monkey
    for i, monkey1 in enumerate(data):
        for monkey2 in data[i+1:]:
            if monkey1['time'] == monkey2['time']:  # Check if they were recorded at the same time
                x1, y1 = float(monkey1['x']), float(monkey1['y'])
                x2, y2 = float(monkey2['x']), float(monkey2['y'])

                # Check if both monkeys are within the box
                if is_within_box(x1, y1, box) and is_within_box(x2, y2, box):
                    pairs.append((monkey1['name'], monkey2['name']))

    return pairs
#===================================================================================================================================

# group pairs of monkeys presence at the same time: n -> n^2 
def group_monkeys_by_time(data):
    groups = defaultdict(list)
    for monkey in data:
        groups[monkey['time']].append(monkey)
    return list(groups.values())
#===================================================================================================================================

# process all pairs to find pairs in the box, running time optimized 
def find_pairs_within_box_optimized(data, box):
    pairs = []
    time_format = "%d-%b-%Y %H:%M:%S"
    for monkey in data:
        monkey['time'] = datetime.datetime.strptime(monkey['time'], time_format)
    
    # Group data by time
    time_groups = group_monkeys_by_time(data)
    
    # Process each time group
    for group in time_groups:
        for i, monkey1 in enumerate(group):
            for monkey2 in group[i+1:]:  # Ensures monkey2 is always different from monkey1
                # Skip comparing a monkey with itself
                if monkey1['name'] == monkey2['name']:
                    continue
                
                x1, y1 = float(monkey1['x']), float(monkey1['y'])
                x2, y2 = float(monkey2['x']), float(monkey2['y'])
                
                # Check if both monkeys are within the box
                if is_within_box(x1, y1, box) and is_within_box(x2, y2, box):
                    # Append pair with time information
                    pairs.append((monkey1['name'], monkey2['name'], monkey1['time'].strftime(time_format), x1, y1, x2, y2))

    return pairs
#===================================================================================================================================

def main():
    #===================================================================================================================================
    #========================================             Set Up                ========================================================
    #===================================================================================================================================
    # Path to your data file
    file_path = 'C:\\Users\\tfeng24\\Desktop\\Sam_MonkeyTracking\\Cleaned_Data\\Cleaned_Data-2021-10-24.txt'
    
    # Read the data from the file
    data = read_monkey_data(file_path)

    # shrink digits after .
    truncate_coordinates(data)
    
    # box coordinates (bottom-left and top-right corners) = area wanna be searched
    #box = ((5, 7), (8, 11))         # left bottom
    #box = ((5, 16), (9, 19))        # left middle
    #box = ((5, 26), (8, 25))        # left top
    #box = ((12, 6), (15, 9))        # middle bottom
    #box = ((11, 13), (15, 16))      # middle middle 1
    #box = ((15, 16), (18, 19))      # middle middle 2
    #box = ((14, 21), (17, 23))      # middle top
    #box = ((21, 21.5), (26, 24))    # right bottom
    box = ((22, 16), (27, 18))      # right middle
    #box = ((20, 3), (23, 6))        # right top

    #===================================================================================================================================
    #========================================             Find Pairs                ====================================================
    #===================================================================================================================================
    # Find pairs of monkeys within the box at the same time
    pairs = find_pairs_within_box_optimized(data, box)
    # Print the results for FIND_PAIRS>>>
    if pairs:
        print("Pairs of monkeys within the specified box at the same time:")
        for name1, name2, time, x1, y1, x2, y2 in pairs:
            print(f"Pair ({name1} at {x1,y1}, {name2} at {x2,y2}), Time: {time}, distance:{euc_d(x1,y1,x2,y2)}")
    else:
        print("No pairs of monkeys were found within the specified box at the same time.")
    #===================================================================================================================================
    #===================================================================================================================================



if __name__ == "__main__":
    main()