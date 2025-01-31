# Copyright (C) [2025] [Blondel Aymeric ATTOP project]
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License, version 3, along with this program. If not, see <https://www.gnu.org/licenses/>.


import os
import shutil
import argparse
import re

import configparser

# Create a ConfigParser object and read the INI file
config = configparser.ConfigParser()
config.read('../config.ini')

# Get the values of DIR_RAW_DATA and DIR_PROCESSED_DATA from the configuration data
DIR_RAW_DATA = config['Directories']['RawData']
DIR_PROCESSED_DATA = config['Directories']['ProcessedData']
DIR_RESULT_DATA = config['Directories']['ResultData']


#DIR_PROCESSED_DATA = "../data/processed_data/molcas_test"
#DIR_RAW_DATA ="../data/raw_data/molcas_test"

def openmolcas_create_directories(jobs, directory_name):
    """Create directories for jobs.

    Args:
        jobs (list of int): A list of integers representing the number of jobs to be created.
        directory_name (str): The name of the main directory where all job directories will be created.
        --openmolcas : type of benchio
    Returns:
        None
    """
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)  # Create main directory if it doesn't exist

    for i in jobs:
        job_folder = f"{directory_name}/job_{i}"
        if not os.path.exists(job_folder):
            os.mkdir(job_folder)  # Create job directory if it doesn't exist

        for j in range(1, i + 1):
            geom_folder = f"{job_folder}/geom_{j}"
            # Check if geom directory already exists
            if not os.path.exists(geom_folder):
                os.mkdir(geom_folder)
                openmolcas_copy_files_into_directory(geom_folder)
            else:
                print(f"Directory '{geom_folder}' already exists.")
                return


def openmolcas_copy_files_into_directory(geom_folder):
    # List of file names to be copied
    files = [DIR_RAW_DATA + "/geometry_1.xyz", DIR_RAW_DATA + "/mol_input_1.input", DIR_RAW_DATA + "/start.RasOrb"]

    for file in files:
        # Check if the file exists before trying to copy it
        if os.path.exists(file):
            shutil.copy(file, geom_folder)
        else:
            print(f"File '{file}' does not exist.")


def get_job_numbers(directory):
    """Get a list of job numbers from directory names in the given directory.

    Args:
        directory (str): The path to the directory containing the job directories.

    Returns:
        A list of integers representing the job numbers extracted from the directory names.
    """

    # Get all subdirectories in the given directory
    subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    # Extract job numbers from directory names using regular expressions
    job_numbers = []
    pattern = r'job_(\d+)'
    for subdir in subdirs:
        match = re.search(pattern, subdir)
        if match:
            job_number = int(match.group(1))
            job_numbers.append(job_number)

    return job_numbers


def openmolcas_replace_njob_in_slurm(input_filename, directory_name, number):
    """Replace all occurrences of {REMPLACE_NJOB} in an input file with a number and write the result to an output file.

    Args:
        input_filename (str): The path to the input file.
        output_filename (str): The path to the output file.
        number (int or str): The number to replace the placeholders with. Must not be equal to 1.
    """
    print(f"Processing job {number}...")
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)  # Create main directory if it doesn't exist
    # Check that the number is not equal to 1
    if number == 1:
        print(f"Processing job {number}...")

        #raise ValueError("Number must not be equal to 1")

    # Read the contents of the input file into a string
    with open(input_filename, 'r') as f:
        content = f.read()

    # Replace all occurrences of {REMPLACE_NJOB} in the string with the given number (converted to a string)
    new_content = content.replace("{REMPLACE_NJOB}", str(number))
    #print(new_content)
    basename = os.path.basename(input_filename)
    dirname = os.path.dirname(input_filename)
    new_basename = basename.replace('njob', str(number)).replace('.tpl', '.sh')
    output_filepath = os.path.join(directory_name, new_basename)
    #print(output_filepath)
    # Write the updated contents to the output file
    with open(output_filepath, 'w') as f:
        f.write(new_content)


#create_directories([1,10],DIR_PROCESSED_DATA+"/toto")def main():
if __name__ == "__main__":
    """Parse command-line arguments and create directories for specified jobs.

    Args:
        None (arguments are parsed from the command line)

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Create directories for specified jobs.")
    parser.add_argument("--jobs", nargs='+', type=int,
                        help="List of integers representing the number of jobs to be created.")
    parser.add_argument("--dir", type=str,
                        help="The name of the main directory where all job directories will be created.")
    parser.add_argument('--openmolcas', action='store_true', help='Generate openmolcas benchio files')
    parser.add_argument('--slurm', action='store_true', help='generate slurm file')
    args = parser.parse_args()
    if args.jobs is not None and args.slurm and args.openmolcas and args.dir:
        job_numbers = get_job_numbers(DIR_PROCESSED_DATA + "/" + args.dir)
        #print(job_numbers)
        for number in job_numbers:
            if number == 1:
                tpl_file = "sub_molcas_nautilus_1job.tpl"
            else:
                tpl_file = "sub_molcas_nautilus_njob.tpl"
            openmolcas_replace_njob_in_slurm(DIR_RAW_DATA + "/sub_molcas_nautilus_njob.tpl",
                                             DIR_PROCESSED_DATA + "/" + args.dir, number)
    if args.jobs is not None and args.dir and args.openmolcas:
        openmolcas_create_directories(args.jobs, DIR_PROCESSED_DATA + "/" + args.dir)
    else:
        print("Please provide both --openmolcas --jobs and --dir arguments and/or --slurm.")
