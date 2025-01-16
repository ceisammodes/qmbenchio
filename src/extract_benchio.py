# coding: utf-8
# !/usr/bin/python
import argparse
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def extract_line_with_wall(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if 'Timing: Wall' in line:
                return line
    return None

def extract_value_from_wall_line(line):
    if 'Wall=' in line:
        start_index = line.index('Wall=') + len('Wall=')
        end_index = line.find(' ', start_index)
        if end_index == -1:
            end_index = len(line)
        value = line[start_index:end_index]
        return value.strip()
    return None

def save_line_to_csv(line, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([line])

def extract_wall_values_from_bench(directory, output_file):
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
        values=extract_wall_values_from_directory(subdirectory, output_file)
        subdirectory=os.path.basename(subdirectory)
            #print(values)
        bench_dict[subdirectory]=values
            #my_dict[subdirectory] = []
        #print(subdirectory)

    #my_dict = dict(zip(keys, values))
    #print(bench_dict)
    return(bench_dict)
    #print(my_dict['100job'])


def extract_wall_values_from_bench_to_analyse_with_host_and_hz(directory, output_file):
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
        values=extract_wall_host_hz_values_from_directory(directory, output_file)
        #values=extract_wall_values_from_directory(subdirectory, output_file)
        subdirectory=os.path.basename(subdirectory)
            #print(values)
        bench_dict=values
            #my_dict[subdirectory] = []
        #print(subdirectory)

    #my_dict = dict(zip(keys, values))
    #print(bench_dict)
    return(bench_dict)
    #print(my_dict['100job'])

def display_bench_as_bar_chart2(bench_dict):
    #print(bench_dict['10job'])
    # Extract the values from the dictionaries
    #print(bench_dict['10job'])
    float_values = {}
    float_values = defaultdict(list)
    fig, ax = plt.subplots(len(bench_dict.keys()))
    fig.suptitle('benchio openmolcas flow /scratch/waves 1000job 25sept')
    for i,type_bench in enumerate(bench_dict.keys()):
        #print(type_bench)
        for value in bench_dict[type_bench]:
            #float_values[type_bench]=(float(value))
            float_values[type_bench].append(float(value))
        print(float_values["10job"])

    # Plot the values
    #plt.plot(X, y, color='r', label='sin')
        ax[i].plot(range(len(float_values[type_bench])),float_values[type_bench],'tab:blue')
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
    for i,type_bench in enumerate(bench_dict.keys()):
        #print(type_bench)
        for value in bench_dict[type_bench]:
            #float_values[type_bench]=(float(value))
            float_values[type_bench].append(float(value))
        print(float_values["10job"])

    # Plot the values
    #plt.plot(X, y, color='r', label='sin')
        ax[i].plot(range(len(float_values[type_bench])),float_values[type_bench],'tab:blue')
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
    df=pd.DataFrame()
    df['job']=bench_dict.keys()
    df['wall']=bench_dict.values()
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
    processed_df['wall']=pd.to_numeric(processed_df['wall'])
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


def extract_wall_values_from_directory(directory,output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        values=[]
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.output'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as file:
                        for line in file:
                            value = extract_value_from_wall_line(line)
                            if value:
                                values.append(value)
                                writer.writerow([value])
    return values

def extract_subdirectories(directory):
    subdirectories = []
    for root, dirs, files in os.walk(directory):
        # Vérifiez si le répertoire actuel est directement sous le répertoire racine
        subdirs = extract_subdirectories(directory)
        print("Sous-répertoires immédiats :", subdirs)
    return subdirectories
def extract_wall_host_hz_values_from_directory(directory,output_file):
    import re,os
    from collections import defaultdict
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #values_host_hz= defaultdict(lambda: None)
        values_host_hz = {}
        list_host_hz_value=[]
        number=None
        values=[]
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
                            value = extract_value_from_wall_line(line)
                        if key not in values_host_hz:
                            values_host_hz[key] = []

                        values_host_hz[key].append(value)
                        writer.writerow([value])
                if file=="for_debug.txt":
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




def analyse_value_host_hz(dict_values_host_hz):
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
    parser.add_argument('-b', help='repertoire du bench')
    parser.add_argument('-a', help='repertoire du bench')
    args = parser.parse_args()

    #output_file = 'chemin/vers/votre/fichier.csv'
    #file_path = args.file_path
    output_file = './extract.csv'
    if args.f:
      line_with_wall = extract_line_with_wall(args.f)
      value = extract_value_from_wall_line(line_with_wall)
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
        extract_wall_values_from_directory(args.d,args.o)
    if args.b:
        bench_dict=extract_wall_values_from_bench(args.b,output_file)
        display_bench_as_bar_chart2(bench_dict)
    if args.a:
        dict_values_host_hz=extract_wall_values_from_bench_to_analyse_with_host_and_hz(args.a,output_file)
        analyse_value_host_hz(dict_values_host_hz)
        #print(bench_dict)
        ## analyse
        #display_bench_as_bar_chart3(bench_dict)
