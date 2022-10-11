import sys
import os
from PyQt5.QtWidgets import QApplication

from SpaceX.abrir_zip import unzip_data
from SpaceX.crear_conexion import crear_conexion
from SpaceX.crear_db import crear_tablas
from SpaceX.gui import Window


def main():
    # Obtener ficheros
    unzip_data()

    # Conectar con la base de datos
    bbdd = 'SpaceX.db'
    if crear_conexion(bbdd) == False:
        sys.exit()

    # Insertar datos en la base de datos
    crear_tablas(bbdd)

    # Crear la aplicación
    app = QApplication(sys.argv)

    # Crear la ventana principal
    win = Window(bbdd)
    win.show()

    # Ejecutar el bucle de eventos
    sys.exit(app.exec())
