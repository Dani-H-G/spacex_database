import os
import random
import csv
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (
    QTableView,
    QVBoxLayout,
    QWidget,
)


class Ver_Lanzamientos_Exitosos(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración del modelo
        self.model = QSqlTableModel(self)
        self.model.setTable("LANZAMIENTOS_EXITOSOS")
        # Los cambios en la BD se guardan automáticamente con OnFieldChange
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "Plataforma")
        self.model.setHeaderData(1, Qt.Horizontal, "Lanzamiento")
        self.model.setHeaderData(2, Qt.Horizontal, "Cohete")
        self.model.setHeaderData(3, Qt.Horizontal, "Coste")
        self.model.setHeaderData(4, Qt.Horizontal, "Ubicación")
        self.model.select()

        # Configuración de la vista
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

        # Configuriación del botón
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Configuración de la ventana
        self.resize(901, 1000)
        fondo_gui(self)


class Descargar_Lanzamientos_Exitosos(QWidget):
    def __init__(self, bbdd):
        super().__init__()

        connection = sqlite3.connect(bbdd)
        query = "SELECT * FROM LANZAMIENTOS_EXITOSOS"
        result = execute_read_query(connection, query)
        with open(os.path.join('SpaceX', 'csv_data', 'zz_lanzamientos_exitosos.csv'), 'w', newline='') as save_csv:
            write = csv.writer(save_csv)
            for row in result:
                write.writerow(row)


class Ver_LOG(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración del modelo
        self.model = QSqlTableModel(self)
        self.model.setTable("LOG")
        self.model.select()

        # Configuración de la vista
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

        # Configuriación del botón
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Configuración de la ventana
        self.resize(393, 250)
        fondo_gui(self)


class Descargar_LOG(QWidget):
    def __init__(self, bbdd):
        super().__init__()

        connection = sqlite3.connect(bbdd)
        query = "SELECT * FROM LOG"
        result = execute_read_query(connection, query)
        with open(os.path.join('SpaceX', 'csv_data', 'zz_log.csv'), 'w', newline='') as save_csv:
            write = csv.writer(save_csv)
            for row in result:
                write.writerow(row)


def fondo_gui(self):
    ruta_fondos = os.path.join('SpaceX', 'fondos')
    fondo = random.choice(os.listdir(ruta_fondos))
    ruta = os.path.join(ruta_fondos, fondo).replace("\\", '/')
    estilo = (
        f"color: darkgrey; border-image: url({ruta}); background-repeat: no-repeat; background-position: center; background-attachment: fixed;")
    self.setStyleSheet(estilo)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    column_name = [description[0] for description in cursor.description]

    result = cursor.fetchall()  # Obtiene una lista
    result.insert(0, tuple(column_name))
    return result
