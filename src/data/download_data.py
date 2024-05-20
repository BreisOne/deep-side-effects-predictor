import requests
import gzip
import shutil
import json
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

FAERS_API_KEY = os.getenv('FAERS_API_KEY')

def download_sider_data():
    url = 'http://sideeffects.embl.de/media/download/meddra_all_label_se.tsv.gz'
    # Obtener la ruta del directorio actual del script
    script_dir = os.getcwd()
    
    # Construir la ruta relativa al directorio 'data/raw'
    local_filename = os.path.join(script_dir, 'data', 'raw', 'meddra_all_label_se.tsv.gz')
        
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    print("Download and extraction complete from SIDER.")

def unzip_sider_data():
    # Obtener la ruta del directorio actual del script
    script_dir = os.getcwd()
    
    # Construir la ruta relativa al directorio 'data/raw'
    local_filename = os.path.join(script_dir, 'data', 'raw', 'meddra_all_label_se.tsv.gz')
    extracted_filename = os.path.join(script_dir, 'data', 'raw', 'sider_side_effects.tsv')
    
    # Verificar si el archivo sider_side_effects.tsv ya existe
    if not os.path.exists(extracted_filename):
        print("The file side_effects.tsv does not exist. Creating file...")
        # Si no existe, crear el archivo
        with open(extracted_filename, 'w'):
            pass  # Esto crea el archivo vacío
        print("File successfully created.")
        
    else:
        print("The file side_effects.tsv already exists.")
    
    print("Unzipping SIDER file...")
    with gzip.open(local_filename, 'rb') as f_in:
        with open(extracted_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print("Unzipped SIDER file")


def download_openfda_data():
    base_url = 'https://api.fda.gov/drug/event.json'
    params = {
        'api_key': FAERS_API_KEY,
        'limit': 100  # Ajusta el límite según sea necesario
    }
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Obtener la ruta del directorio actual del script
    script_dir = os.getcwd()

    # Construir la ruta relativa al directorio 'data/raw'
    local_filename = os.path.join(script_dir, 'data', 'raw', 'openfda_data.json')
    
    try:
        
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        # Convertir la respuesta a JSON
        data = response.json()
             
        with open(local_filename, 'w') as f:
            json.dump(data, f)
        print("Download of OpenFDA data complete.")
     
    except requests.exceptions.RequestException as e:
        print(f"Error in the API call: {e}")
        
        # Si hay una excepción HTTPError, imprimir la información del error
        if isinstance(e, requests.exceptions.HTTPError):
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    
    if not FAERS_API_KEY:
        print("FAERS_API_KEY not set. Please check your .env file.")
    else:
        download_sider_data()
        unzip_sider_data()
        download_openfda_data()
