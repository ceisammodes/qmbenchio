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
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from openmolcas import bench_openmolcas as bo


def extract_line_with_wall(file_path):
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


def save_line_to_csv(line, output_file):
    '''
    Args:
        line:
        output_file:

    Returns:
    '''
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([line])





def display_bench_as_bar_chart2(bench_dict):
    #print(bench_dict['10job'])
    # Extract the values from the dictionaries
    #print(bench_dict['10job'])
    float_values = {}
    float_values = defaultdict(list)
    fig, ax = plt.subplots(len(bench_dict.keys()))
    fig.suptitle('benchio openmolcas flow /scratch/waves 1000job 25sept')
    for i, type_bench in enumerate(bench_dict.keys()):
        #print(type_bench)
        for value in bench_dict[type_bench]:
            #float_values[type_bench]=(float(value))
            float_values[type_bench].append(float(value))
        print(float_values["10job"])

        # Plot the values
        #plt.plot(X, y, color='r', label='sin')
        ax[i].plot(range(len(float_values[type_bench])), float_values[type_bench], 'tab:blue')
        #ax.set_title(bench_dict[type_bench])
        # Add labels and a title to the plot
        ax[i].set_xlabel('nb job')
        ax[i].set_ylabel('Walltime')

    # Show the plot
    plt.show()


def display_bench_as_bar_chart3(bench_dict):
    #print(bench_dict['10job'])
    # Extract the values from the dictionaries
    #print(bench_dict['10job'])
    float_values = {}
    float_values = defaultdict(list)
    fig, ax = plt.subplots(len(bench_dict.keys()))
    fig.suptitle('benchio openmolcas flow /scratch/waves cnode327,703,704 ')
    for i, type_bench in enumerate(bench_dict.keys()):
        #print(type_bench)
        for value in bench_dict[type_bench]:
            #float_values[type_bench]=(float(value))
            float_values[type_bench].append(float(value))
        print(float_values["10job"])

        # Plot the values
        #plt.plot(X, y, color='r', label='sin')
        ax[i].plot(range(len(float_values[type_bench])), float_values[type_bench], 'tab:blue')
        #ax.set_title(bench_dict[type_bench])
        # Add labels and a title to the plot
        ax[i].set_xlabel('nb job')
        ax[i].set_ylabel('Walltime')

    # Show the plot
    plt.show()


def display_bench_as_bar_chart(bench_dict):
    # Récupérer les clés et les valeurs du dictionnaire
    #keys = list(bench_dict.keys())
    #print(keys)
    df = pd.DataFrame()
    df['job'] = bench_dict.keys()
    df['wall'] = bench_dict.values()
    print(df)

    processed_rows = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Iterate over each list value in the 'list_column'
        for value in row['wall']:
            # Create a new row with the processed value
            processed_row = row.copy()
            processed_row['wall'] = value

            # Append the processed row to the list
            processed_rows.append(processed_row)

    # Create a new DataFrame from the processed rows
    processed_df = pd.DataFrame(processed_rows)

    # Print the processed DataFrame
    print(processed_df)
    # Create a new figure
    fig, ax = plt.subplots()

    # Plot the values
    ax.plot(processed_df['wall'])

    # Add labels and a title to the plot
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.set_title('Plot of Values')

    # Show the plot
    plt.figure()
    print(processed_df['wall'])
    processed_df['wall'] = pd.to_numeric(processed_df['wall'])
    print(processed_df['wall'].dtypes)
    processed_df['wall'].plot(kind='line')
    #df['wall']=pd.to_numeric(df['wall'],errors='coerce')
    #print(df.dtypes)
    #print(df)
    #df.plot.line(processed_df)
    plt.show()
    #print(df)

    #for i,key in enumerate(keys):
    #    i=i+1
    #    print(key)
    #for j,value in enumerate(values):
    #    j=j+1
    #    print(value)
    #    plt.plot(bench_dict[key])
    # Créer le graphique à barres
    #plt.bar(i, value)

    # Ajouter des étiquettes aux axes
    #plt.xlabel('walltime')
    #plt.ylabel('nb job')
    # Ajouter un titre au graphique
    #plt.title('benchmarkio_openmolcasflow')

    # Afficher le graphique
    #plt.show()


def extract_subdirectories(directory):
    subdirectories = []
    for root, dirs, files in os.walk(directory):
        # Vérifiez si le répertoire actuel est directement sous le répertoire racine
        subdirs = extract_subdirectories(directory)
        print("Sous-répertoires immédiats :", subdirs)
    return subdirectories


def highlight_Walltime(s):
    s['Walltime'] = pd.to_numeric(s['Walltime'], errors='coerce')
    return ['background-color: red' if v > 300 else '' for v in s['Walltime']]


# Apply the function to your DataFrame and display it


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Open a file and print its contents.')
    #parser.add_argument('file_path', type=str, help='Path to the file to open.')
    parser.add_argument('-f', help='chemin du fichier à lire')
    parser.add_argument('-d', help='chemin du répertoire à parcourir')
    parser.add_argument('-o', help='fichier csv de sortie')
    parser.add_argument('-b', help='Bench directory')
    # pour l'instant que openmolcas
    parser.add_argument('-t', help='Type Benchmark')
    parser.add_argument('-a', help='Bench directory')
    args = parser.parse_args()

    #output_file = 'chemin/vers/votre/fichier.csv'
    #file_path = args.file_path
    output_file = './extract.csv'
    if args.f:
        line_with_wall = extract_line_with_wall(args.f)
        value = bo.extract_value_from_wall_line(line_with_wall)
        if value:
            print(f"La valeur de 'WALL=' est {value}.")
        else:
            print("Aucune ligne avec 'WALL=' n'a été trouvée.")
        if value:
            save_line_to_csv(value, output_file)
            print(f"La valeur Wall a été extraite et stockée dans {output_file}.")
        else:
            print("Aucune ligne avec valeur 'Timing: Wall' n'a été trouvée.")
    if args.d:
        bo.openmolcas_extract_wall_values_from_directory(args.d, args.o)
    if args.b:
        bench_dict=bo.openmolcas_extract_wall_values_from_bench(args.b,output_file)
        display_bench_as_bar_chart2(bench_dict)
        #bo.openmolcas_extract_wall_values_from_bench(args.d, output_file)
        #bench_dict = bo.openmolcas_extract_wall_values_from_bench_to_analyse_with_host_and_hz(args.b, output_file)
        print(bench_dict)
        #display_bench_as_bar_chart2(bench_dict)
    if (args.t == "Bench_Hz"):
        print("Bench pour alanyser la frequence des hosts avec benchmark openmolcas")
        dict_values_host_hz = bo.openmolcas_analyse_value_host_hz(args.a, output_file)
        bo.openmolcas_analyse_value_host_hz(dict_values_host_hz)
        #print(bench_dict)
        ## analyse
        #display_bench_as_bar_chart3(bench_dict)
