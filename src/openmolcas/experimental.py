# Copyright (C) [2025] [Blondel Aymeric ATTOP project]
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License, version 3, along with this program. If not, see <https://www.gnu.org/licenses/>.



import os
import csv
import pandas
import matplotlib.pyplot as plt
from collections import defaultdict

from src.openmolcas.bench_openmolcas import openmolcas_extract_value_from_wall_line


# This function is still under development and not tested.
def openmolcas_extract_wall_host_hz_values_from_directory(directory, output_file):
    """
    This function extracts wall time values and host Hz values from all openmolcas output files in a specified directory.
    It writes these values into a csv file, and it also prints out a sorted dictionary of the extracted values.

    Args:
        directory (str): The path to the directory containing the openmolcas output files.
        output_file (str): The path to the csv file where the extracted wall time values will be written.

    Returns:
        dict: A sorted dictionary of all the extracted values, with the keys being strings representing numbers,
              and the values being lists containing the corresponding wall time value(s) and host Hz value(s).

    Raises:
        FileNotFoundError: If the specified directory or output file does not exist.
        Exception: For any other errors that might occur while reading or writing files.
    """
    import re, os
    from collections import defaultdict
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #values_host_hz= defaultdict(lambda: None)
        values_host_hz = {}
        list_host_hz_value = []
        number = None
        values = []
        subdirectories = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                #directory = os.path.dirname(file)

                #print(f"Le répertoire contenant le fichier est : {file}")
                #directory_name = os.path.dirname(file_path)
                if file.endswith('.output'):
                    file_path = os.path.join(root, file)
                    directory_name = os.path.dirname(file_path)
                    #file_path2 = os.path.join(dirs, file)

                    number = directory_name[-5:].split('_')[1]
                    key = str(number)
                    with open(file_path, 'r') as file:
                        for line in file:
                            openmolcas_extract_value_from_wall_line(line)
                        if key not in values_host_hz:
                            values_host_hz[key] = []

                        values_host_hz[key].append(values)
                        writer.writerow([values])
                if file == "for_debug.txt":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as file:
                        content = file.read()

                        # Utiliser des expressions régulières pour extraire les informations
                        node_match = re.search(r'node\d+', content)
                        frequency_match = re.search(r'current CPU frequency: (\d+)', content)

                        if node_match and frequency_match:
                            node = node_match.group(0)
                            frequency = frequency_match.group(1)
                            #print(f'Node: {node}')
                            values_host_hz[key].append(node)
                            #print(f'CPU Frequency: {frequency}')
                            values_host_hz[key].append(frequency)
                        else:
                            print('The necessary information was not found in the file.')

    values_host_hz = {int(k): v for k, v in values_host_hz.items()}
    sorted_values_host_hz = dict(sorted(values_host_hz.items()))
    sorted_values_host_hz = {str(k): v for k, v in sorted_values_host_hz.items()}
    print(sorted_values_host_hz)
    return sorted_values_host_hz


def openmolcas_analyse_value_host_hz(dict_values_host_hz):
    """
    Experimental function.

    This function is still under development and may contain bugs or unexpected behavior.
    """
    """
    This function takes a dictionary containing walltime values, hostname values, and Hz values as input,
    and it writes these values to an Excel file. The function also prints out the 'Hz' column of the resulting DataFrame.

    Args:
        dict_values_host_hz (dict): A dictionary where each key-value pair represents a set of walltime value(s), hostname value(s), and Hz value(s).
                                   The keys should be strings representing numbers, and the values should be lists containing the corresponding walltime value(s), hostname value(s), and Hz value(s).

    Raises:
        Exception: For any errors that might occur while writing to the Excel file.
    """
    from pandas import ExcelWriter

    from IPython.display import HTML
    df = (pd.DataFrame(dict_values_host_hz).transpose())
    #.transpose())
    df.columns = ['Walltime', 'Hostname', 'Hz']
    #df["feature1"] = df["feature1"].astype(str)
    print(df["Hz"])
    #df.columns = ['feature1', 'feature2', 'feature3','feature4']
    #df[['column1', 'column2', 'column3']]=df.apply(pd.Series)
    #df = df.drop('testjob', axis=1)
    # Apply the function to your DataFrame and display it
    #styled_df = df.style.apply(highlight_Walltime, axis=1)
    #styled_df.to_html('mon_fichier.html', index=False)
    #styled_df.to_excel('mon_fichier.xlsx', engine='openpyxl', index=False)
    #display(styled_df)
    #df_html = styled_df.to_html()
    writer = ExcelWriter('mon_fichier.xlsx')
    df.to_excel(writer, index=False)
    writer.save()
    #result = styled_df.to_html()
    #print(result)
