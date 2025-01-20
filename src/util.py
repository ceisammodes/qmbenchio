import os
import requests
from tqdm import tqdm
import zipfile

def download_and_extract_zip(url, raw_folder='data/raw', extract_folder='data/extracted'):
    """
    Downloads a .zip file from a URL, saves it in the `raw_folder` directory,
    and extracts its contents into the `extract_folder` directory, displaying a progress bar.

    Args:
        url (str): The URL of the .zip file to download.
        raw_folder (str, optional): The directory to save the downloaded .zip file. Defaults to 'data/raw'.
        extract_folder (str, optional): The directory to extract the contents of the .zip file. Defaults to 'data/extracted'.

    """
    # Création des dossiers si nécessaire
    os.makedirs(raw_folder, exist_ok=True)
    os.makedirs(extract_folder, exist_ok=True)

    # Nom du fichier zip dans le dossier de destination
    zip_filename = os.path.join(raw_folder, 'datafile.zip')

    # Télécharger le fichier zip
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Total de la taille du fichier (si disponible)
        total_size = int(response.headers.get('content-length', 0))

        # Téléchargement du fichier avec une barre de progression
        with open(zip_filename, 'wb') as file, tqdm(
            desc=zip_filename,
            total=total_size,
            unit='B', unit_scale=True
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):  # Taille des morceaux
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))  # Mettre à jour la barre de progression

        print(f"Le fichier zip a été téléchargé avec succès dans {zip_filename}")

        # Décompresser le fichier zip
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
            print(f"Les fichiers ont été extraits dans {extract_folder}")
    else:
        print(f"Erreur de téléchargement : {response.status_code}")
