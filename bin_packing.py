from z3 import *
import random
import csv
import time
import sys


TIMEOUT = 600000
BIN_CAPACITY = 100
MIN_ITEM_SIZE = 1
MAX_ITEM_SIZE = 100

def write_to_file(data):
    file_path = "results4.csv"
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print(f"An error occurred while writing to the CSV file '{file_path}': {e}")

def generate_random_problem(num_vals):
    items = []
    for i in range(num_vals):
        items.append(random.randint(MIN_ITEM_SIZE, MAX_ITEM_SIZE))
    return items

def solve(items, seed):
    start_time = time.time()
    num_bins = len(items)

    solver = Solver()
    solver.set("timeout", TIMEOUT)

    x = [[Bool(f"x_{i}_{j}") for j in range(num_bins)] for i in range(len(items))]  
    b = [Bool(f"b_{j}") for j in range(num_bins)]                                   

    for i in range(len(items)):
        solver.add(Or([x[i][j] for j in range(num_bins)]))  
        for j1 in range(num_bins):
            for j2 in range(j1 + 1, num_bins):
                solver.add(Or(Not(x[i][j1]), Not(x[i][j2])))  

    for j in range(num_bins):
        solver.add(Sum([If(x[i][j], items[i], 0) for i in range(len(items))]) <= BIN_CAPACITY)

    for j in range(num_bins):
        solver.add(Or([x[i][j] for i in range(len(items))]) == b[j]) 
        for i in range(len(items)):
            solver.add(Or(Not(x[i][j]), b[j]))  

    objective = Sum([If(b[j], 1, 0) for j in range(num_bins)])
    opt = Optimize()
    opt.add(solver.assertions())
    opt.set("timeout", TIMEOUT)
    opt.minimize(objective)
    if opt.check() == sat:
        model = opt.model()
        bins = [[] for _ in range(num_bins)]
        for i in range(len(items)):
            for j in range(num_bins):
                if model.evaluate(x[i][j]):
                    bins[j].append(items[i])
        used_bins = [bin for bin in bins if bin]
        end_time = time.time()
        total_time = end_time - start_time
        if sys.argv[1] == "test":
            data = [seed, len(items), total_time, len(used_bins), BIN_CAPACITY]
            write_to_file(data)
        print(f"Minimum number of bins used: {len(used_bins)}")
        for idx, bin in enumerate(used_bins):
            print(f"Bin {idx + 1}: {bin}")
    else:
        end_time = time.time()
        total_time = end_time - start_time
        if sys.argv[1] == "test":
            data = [seed, len(items), total_time, "No solution", items]
            write_to_file(data)
        print("No solution found")

def main():
    #print(generate_random_problem())
    if len(sys.argv) < 2:
        print("Usage: python3 bin_packing.py <test/number_of_values> ...")
        print("python3 bin_packing.py test <number_of_values> <seed> <capacity(default 100)>")
        print("python3 bin_packing.py <number_of_values> list of items wieghts <capacity> <timeout>")
        return 1

    global BIN_CAPACITY
    global TIMEOUT
    if sys.argv[1] == "test":
        seed = int(sys.argv[3])
        num_vals = int(sys.argv[2])
        if len(sys.argv) == 5:
            BIN_CAPACITY = int(sys.argv[4])
        random.seed(seed)
        items = generate_random_problem(num_vals)
        print(items)
        solve(items, seed)
    else:
        num_vals = int(sys.argv[1])
        items = []
        for i in range(num_vals):
            items.append(int(sys.argv[1+i]))
        BIN_CAPACITY = int(sys.argv[-2])
        TIMEOUT = int(sys.argv[-1])
        solve(items, -1)
    return 0


main()