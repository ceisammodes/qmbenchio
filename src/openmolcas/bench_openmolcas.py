# Copyright (C) [2025] [Blondel Aymeric ATTOP project]
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License, version 3, along with this program. If not, see <https://www.gnu.org/licenses/>.



import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
def openmolcas_extract_line_with_wall(file_path):
    """
    Args:
        file_path: The path to the file to be read.

    Returns: str or None: The line containing 'Timing: Wall' if found, otherwise None.

    Example:
    file_path = 'path/to/your/file.txt'
    result = extract_line_with_wall(file_path)
    if result:
        print(f"Found the line: {result}")
    else:
        print("No 'Timing: Wall' found.")
    """
    with open(file_path, 'r') as file:
        for line in file:
            if 'Timing: Wall' in line:
                return line
    return None


def openmolcas_save_line_to_csv(line, output_file):
    '''
    Args:
        line:
        output_file:

    Returns:
    '''
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([line])

def openmolcas_extract_subdirectories(directory):
    subdirectories = []
    for root, dirs, files in os.walk(directory):
        "Check if the current directory is at the top-level."
        subdirs = openmolcas_extract_subdirectories(directory)
        print("Immediate child directories :", subdirs)
    return subdirectories


def openmolcas_highlight_Walltime(s):
    s['Walltime'] = pd.to_numeric(s['Walltime'], errors='coerce')
    return ['background-color: red' if v > 300 else '' for v in s['Walltime']]


# Apply the function to your DataFrame and display it


def openmolcas_extract_wall_values_from_bench(directory, output_file):
    """
    Extracts walltime values from benchmark subdirectories.

    This function traverses the specified directory to find subdirectories
    ending with 'job'. It extracts wall time values from each subdirectory
    using the `openmolcas_extract_wall_values_from_directory` function and
    stores them in a dictionary.

    Args:
        directory (str): The path to the main directory containing benchmark subdirectories.
        output_file (str): The path to the output file where extracted values will be written.

    Returns:
        dict: A dictionary where keys are subdirectory names and values are lists of extracted walltime values.
    """
    keys=[]
    values=[]
    subdirectories = []
    bench_dict = {}
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.endswith('job'):
                subdirectories.append(os.path.join(root, dir))
    for subdirectory in subdirectories:

        values=openmolcas_extract_wall_values_from_directory(subdirectory, output_file)
        subdirectory=os.path.basename(subdirectory)

        bench_dict[subdirectory]=values

    return(bench_dict)

def openmolcas_extract_wall_values_from_directory(directory,output_file):
    """
    This function extracts walltime values from all Molcas output files in a specified directory
    and writes them into a csv file.

    Args:
        directory (str): The path to the directory containing the Molcas output files.
        output_file (str): The path to the csv file where the extracted wall time values will be written.

    Returns:
        list: A list of all the extracted wall time values.

    Raises:
        FileNotFoundError: If the specified directory or output file does not exist.
        Exception: For any other errors that might occur while reading or writing files.
    """
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        values=[]
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.output'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as file:
                        for line in file:
                            value = openmolcas_extract_value_from_wall_line(line)
                            if value:
                                values.append(value)
                                writer.writerow([value])
    return values


def openmolcas_extract_value_from_wall_line(line):
    """
    This function extracts the wall time value from a given line in a openmolcas output file, if it exists.

    Args:
        line (str): The line from which to extract the wall time value.

    Returns:
        str or None: The extracted wall time value as a string, or None if no value was found in the line.
    """
    if 'Wall=' in line:
        start_index = line.index('Wall=') + len('Wall=')
        end_index = line.find(' ', start_index)
        if end_index == -1:
            end_index = len(line)
        value = line[start_index:end_index]
        return value.strip()
    return None


def openmolcas_extract_wall_values_from_bench_to_analyse_with_host_and_hz(directory, output_file):
    """
        Extracts wall time values from benchmark directories for analysis with host and Hz information.

        This function traverses the specified directory to find subdirectories ending with 'job'.
        It extracts wall time values from each subdirectory using the
        `openmolcas_extract_wall_values_from_directory` function and stores them in a dictionary.

        Args:
            directory (str): The path to the main directory containing benchmark subdirectories.
            output_file (str): The path to the output file where extracted values will be written.

        Returns:
            dict: A dictionary where keys are subdirectory names and values are lists of extracted walltime values.
    """
    keys = []
    values = []
    subdirectories = []
    bench_dict = {}
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.endswith('job'):
                subdirectories.append(os.path.join(root, dir))
    for subdirectory in subdirectories:

        values=openmolcas_extract_wall_values_from_directory(subdirectory, output_file)
        subdirectory = os.path.basename(subdirectory)
        #print(values)
        bench_dict = values

    return (bench_dict)



def openmolcas_display_bench_as_bar_chart(bench_dict):
    """
    This function takes a dictionary containing benchmarking data as input, and it displays this data as a bar chart using Matplotlib. The dictionary should have keys that represent different types of benchmarks, and values that are lists of string representations of floating-point numbers.

    Args:
        bench_dict (dict): A dictionary where each key-value pair represents a set of walltime value(s) for a specific type of benchmark. The keys should be strings representing the type of benchmark, and the values should be lists containing the corresponding walltime value(s) as string representations of floating-point numbers.

    Raises:
        ValueError: If any of the string representations of floating-point numbers cannot be converted to a float.
    """
    #print(bench_dict['10job'])
    # Extract the values from the dictionaries
    #print(bench_dict['10job'])
    float_values = {}
    float_values = defaultdict(list)
    fig, ax = plt.subplots(len(bench_dict.keys()))
    fig.suptitle('benchio openmolcas')
    for i, type_bench in enumerate(bench_dict.keys()):
        #print(type_bench)
        for value in bench_dict[type_bench]:
            #float_values[type_bench]=(float(value))
            float_values[type_bench].append(float(value))
        #print(float_values["10job"])

        # Plot the values
        #plt.plot(X, y, color='r', label='sin')
        ax[i].plot(range(len(float_values[type_bench])), float_values[type_bench], 'tab:blue')
        #ax.set_title(bench_dict[type_bench])
        # Add labels and a title to the plot
        ax[i].set_xlabel('nb job')
        ax[i].set_ylabel('Walltime')

    # Show the plot
    plt.show()


