'''This script was used to run the test cases'''

import subprocess
import csv
import sys

SEEDS = [7, 12, 33, 79, 123, 673, 839, 1283, 4291, 9046]
NUM_VALS_LIST = [3, 5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31, 32]
CAPACITY_LIST=[100, 200, 300, 400, 500,600,700, 800,900, 1000, 1100]

def write_to_file(data):
    file_path = "results4.csv"
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print(f"An error occurred while writing to the CSV file '{file_path}': {e}")

def run_command(command):
    try:
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = result.communicate()
        if result.returncode == 0:
            return stdout.strip().split("\n")
        else:
            print("Error:", stderr.strip())
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def main():
    write_to_file(["Seed", "Number of Values", "Time", "Number of Bins", "Bins", "Capacity"])
    initial_command = "python3 bin_packing.py test "
    if sys.argv[1] == "1":
        for i in range(len(NUM_VALS_LIST)):
            num_vals = str(NUM_VALS_LIST[i])
            for j in range(len(SEEDS)):
                command = initial_command + num_vals + " " + str(SEEDS[j])
                print(run_command(command))
    elif sys.argv[1] == "2":
        initial_command += "11 "
        for i in range(len(CAPACITY_LIST)):
            capacity = str(CAPACITY_LIST[i])
            for j in range(len(SEEDS)):
                command = initial_command + str(SEEDS[j]) + " " + capacity
                print(run_command(command))
    else:
        initial_command += "50 "
        for i in range(len(SEEDS)):
            command = initial_command + str(SEEDS[i]) + " 1000"
            print(run_command(command))


main()