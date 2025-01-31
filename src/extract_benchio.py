# Copyright (C) [2025] [Blondel Aymeric ATTOP project]
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License, version 3, along with this program. If not, see <https://www.gnu.org/licenses/>.


# coding: utf-8
# !/usr/bin/python
import argparse
from openmolcas import bench_openmolcas as bo

import configparser

# Create a ConfigParser object and read the INI file
config = configparser.ConfigParser()
config.read('../config.ini')

DIR_RESULT_DATA = config['Directories']['ResultData']



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Open a file and print its contents.')
    #parser.add_argument('file_path', type=str, help='Path to the file to open.')
    parser.add_argument('-f', help='path to input file')
    parser.add_argument('-d', help='path  to directory of input files')
    parser.add_argument('-o', help='csv output file')
    parser.add_argument('-b', help='Bench directory')
    # pour l'instant que openmolcas
    parser.add_argument('-t', help='Benchmark type')
    parser.add_argument('-a', help='Benchmark directory')
    args = parser.parse_args()

    #output_file = 'chemin/vers/votre/fichier.csv'
    #file_path = args.file_path
    #output_file = './extract.csv'
    output_file= DIR_RESULT_DATA+"/extract.csv"
    if args.f:
        line_with_wall = bo.extract_line_with_wall(args.f)
        value = bo.extract_value_from_wall_line(line_with_wall)
        if value:
            print(f"La valeur de 'WALL=' est {value}.")
        else:
            print("Aucune ligne avec 'WALL=' n'a été trouvée.")
        if value:
            bo.save_line_to_csv(value, output_file)
            print(f"The WallTime value was extracted and stored in {output_file}.")
        else:
            print("No line with 'Timing: Wall' was found.")
    if args.d:
        bo.openmolcas_extract_wall_values_from_directory(args.d, args.o)
    if args.b:
        bench_dict=bo.openmolcas_extract_wall_values_from_bench(args.b,output_file)
        bo.openmolcas_display_bench_as_bar_chart(bench_dict)
        #print(bench_dict)

    if (args.t == "Bench_Hz"):
        # This function is still under development and not tested.
        print("Benchmarking host frequencies with OpenMolcas")
        dict_values_host_hz = bo.openmolcas_analyse_value_host_hz(args.a, output_file)
        bo.openmolcas_analyse_value_host_hz(dict_values_host_hz)

