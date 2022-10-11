from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase


def crear_conexion(nombre_bd):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(nombre_bd)
    print('Base de Datos creada y conectada.')

    if not connection.open():
        QMessageBox.warning(
            None,
            "Error de conexión.",
            f"DB Error: {connection.lastError().text()}",
        )
        return False
    return True
