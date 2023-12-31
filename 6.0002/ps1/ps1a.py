###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    with open(filename, "r") as f:
        lines = f.readlines()
    cows = {}
    for line in lines:
        line = line.strip().split(',')
        name = line[0]
        weight = int(line[1])
        cows[name] = weight
    return cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_dict = dict(cows)
    cows_list = [(name, cows_dict[name]) for name in sorted(cows_dict, key=cows_dict.get, reverse=True)]
    trips = []
    while cows_list:
        trip = []
        space = limit
        new_cows = []
        for cow in cows_list:
            if cow[1] <= space:
                space -= cow[1]
                trip.append(cow[0])           
            else:
                new_cows.append(cow)
        trips.append(trip)
        cows_list = new_cows[:]
    return trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Generate combination of all trips
    cow_partitions = get_partitions(cows)
    # Iterate over all partitions
    for partition in cow_partitions:
        weight_checks = []
        for trip in partition:
            # Get the weight of each trip and store the check with the limit in a list
            trip_weight = sum([cows[name] for name in trip])
            weight_checks.append(trip_weight <= limit)
        # If all the checks are true -> all trips below the weight limit, found solution
        if all(weight_checks):
            return partition
     
# Problem 4
def compare_cow_transport_algorithms(filename):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows(filename)
    print(f'Loaded {filename}')

    # Greedy algorithm timing 
    start = time.time()
    print('----- Greedy Algorithm -----')
    greedy_result = greedy_cow_transport(cows, 10)
    end = time.time()
    print(f'Greedy Trips: {len(greedy_result)}')
    print(f'Greedy Time: {(end - start):.2f} s')

    # Brute force algorithm timing
    start = time.time()
    print('----- Brute Force Algorithm -----')
    brute_force_result = brute_force_cow_transport(cows, 10)
    end = time.time()
    print(f'Brute Force Trips: {len(brute_force_result)}')
    print(f'Brute Force Time: {(end - start):.2f} s')

if __name__ == '__main__':
    compare_cow_transport_algorithms("ps1_cow_data.txt")
    print('\n\n')
    compare_cow_transport_algorithms("ps1_cow_data_2.txt")