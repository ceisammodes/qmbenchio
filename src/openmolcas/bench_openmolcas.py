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

def openmolcas_extract_wall_values_from_bench(directory, output_file):
    keys=[]
    values=[]
    subdirectories = []
    bench_dict = {}
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.endswith('job'):
                subdirectories.append(os.path.join(root, dir))
    for subdirectory in subdirectories:
        # Faites quelque chose avec chaque sous-répertoire
        values=openmolcas_extract_wall_values_from_directory(subdirectory, output_file)
        subdirectory=os.path.basename(subdirectory)
            #print(values)
        bench_dict[subdirectory]=values
            #my_dict[subdirectory] = []
        #print(subdirectory)

    #my_dict = dict(zip(keys, values))
    #print(bench_dict)
    return(bench_dict)
    #print(my_dict['100job'])


def openmolcas_extract_wall_values_from_directory(directory,output_file):
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
    if 'Wall=' in line:
        start_index = line.index('Wall=') + len('Wall=')
        end_index = line.find(' ', start_index)
        if end_index == -1:
            end_index = len(line)
        value = line[start_index:end_index]
        return value.strip()
    return None

def openmolcas_extract_wall_host_hz_values_from_directory(directory, output_file):
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

            #subdirs = extract_subdirectories(dirs)
            #print("Sous-répertoires immédiats :", subdirs)
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
                    #
                    # Vérifiez si la clé existe dans le dictionnaire

                    #values_host_hz[key]=list_host_hz_value
                    #print(number)  # Output: 7 1
                    #print(f"Le répertoire contenant le fichier  {file} est : {number}")
                    with open(file_path, 'r') as file:
                        for line in file:
                            value = openmolcas_extract_value_from_wall_line(line)
                        if key not in values_host_hz:
                            values_host_hz[key] = []

                        values_host_hz[key].append(value)
                        writer.writerow([value])
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
                            print('Les informations nécessaires n\'ont pas été trouvées dans le fichier.')

    values_host_hz = {int(k): v for k, v in values_host_hz.items()}
    sorted_values_host_hz = dict(sorted(values_host_hz.items()))
    sorted_values_host_hz = {str(k): v for k, v in sorted_values_host_hz.items()}
    print(sorted_values_host_hz)
    return sorted_values_host_hz


def openmolcas_analyse_value_host_hz(dict_values_host_hz):
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


def openmolcas_extract_wall_values_from_bench_to_analyse_with_host_and_hz(directory, output_file):
    '''
    Args:
        directory:
        output_file:

    Returns:

    '''
    keys = []
    values = []
    subdirectories = []
    bench_dict = {}
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.endswith('job'):
                subdirectories.append(os.path.join(root, dir))
    for subdirectory in subdirectories:
        # Faites quelque chose avec chaque sous-répertoire
        #values = extract_wall_host_hz_values_from_directory(directory, output_file)
        values=openmolcas_extract_wall_values_from_directory(subdirectory, output_file)
        subdirectory = os.path.basename(subdirectory)
        #print(values)
        bench_dict = values
        #my_dict[subdirectory] = []
        #print(subdirectory)

    #my_dict = dict(zip(keys, values))
    #print(bench_dict)
    return (bench_dict)
    #print(my_dict['100job'])


def openmolcas_display_bench_as_bar_chart2(bench_dict):
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


