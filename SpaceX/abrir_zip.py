import os
from zipfile import ZipFile


def unzip_data():
    ruta_origen = os.path.join('SpaceX', 'archive.zip')
    ruta_destino = os.path.join('SpaceX', 'csv_data')

    with ZipFile(ruta_origen, 'r') as zip_file:
        zip_file.extractall(ruta_destino)
        print(
            '\nSe ha creado una carpeta "csv_data" con los archivos descargados de Kaggle.')
