import csv
import os
import time
import sqlite3
from PyQt5.QtSql import QSqlQuery


def vaciar_db(borrar_tablas):
    for borrado in borrar_tablas:
        delete_table = QSqlQuery()
        delete_table.exec(borrado)


def crear_tablas(bbdd):
    vaciar_db(borrar_tablas)
    for x in range(len(tablas)):
        create_table = QSqlQuery()
        create_table.exec(tablas[x])
        postureo_procesar_datos()
        print(f'Tabla {x+1} creada.              ', end='\r')
        time.sleep(0.5)
    print("Tablas creadas con éxito.")

    insertar_datos(bbdd)


# atributos = columnas
def preparar_insert(archivo, atributos):
    tablas = ['CAPSULAS', 'CORES', 'LANZAMIENTOS',
              'PLATAFORMA_LANZAMIENTO', 'CARGA', 'COHETES', 'BUQUES']

    insert = (
        f'INSERT INTO {tablas[archivo]} VALUES ({f"?, "*(atributos-1)}?)')
    return insert


def insertar_datos(bbdd):
    connection = sqlite3.connect(bbdd)
    cursor = connection.cursor()

    # Es importante que la carpeta 'csv_data' esté ordenada por nombre ascendente
    ruta = os.path.join('SpaceX', 'csv_data')
    archivos = os.listdir(ruta)
    for archivo in range(len(archivos)):
        file_csv = os.path.join(ruta, archivos[archivo])

        with open(file_csv, 'r') as file:
            # next(file)  # Omite la primera fila (encabezados)
            datos = csv.reader(file, delimiter=',')

            for row in datos:
                atributos = len(row)
                break
            insert = preparar_insert(archivo, atributos)
            cursor.executemany(insert, datos)
            connection.commit()

    postureo_procesar_datos()
    create_trigger(trigger)
    create_view(view)
    print('Datos insertados con éxito en la Base de Datos.')


def create_view(view):
    new_view = QSqlQuery()
    new_view.exec(view)


def create_trigger(trigger):
    for query in trigger:
        new_trigger = QSqlQuery()
        new_trigger.exec(query)


def postureo_procesar_datos():
    for _ in range(3):  # tres repeticiones
        for x in range(4):  # tres puntos
            string = "." * x + "   "
            print(
                f'Procesando datos{string}', end="\r")
            time.sleep(0.2)
    return ('                                                 ')


view = """
    CREATE VIEW IF NOT EXISTS LANZAMIENTOS_EXITOSOS AS
    SELECT 
    PL.full_name AS PLATAFORMA, L.name AS LANZAMIENTO, C.name AS COHETE, 
    C.cost_per_launch AS COSTE, PL.locality AS UBICACION 
    FROM LANZAMIENTOS L
        INNER JOIN COHETES C ON C.rocket_id=L.rocket_id
        INNER JOIN PLATAFORMA_LANZAMIENTO PL ON PL.launchpad_id=L.launchpad_id
        WHERE L.success = "True"
        ORDER BY C.name, L.name
	;
    """

trigger = ["""
    CREATE TABLE IF NOT EXISTS LOG (
								Id_Log INTEGER,
								Fecha date DEFAULT (datetime('now','localtime')),
								Evento TEXT NOT NULL,
								Cohete TEXT NOT NULL,
								PRIMARY KEY (Id_Log AUTOINCREMENT)
								);
    """,
           """							
    CREATE TRIGGER IF NOT EXISTS COHETES_AFTER_INSERT
    AFTER INSERT ON COHETES
    BEGIN
        INSERT INTO LOG (Evento, Cohete)
        VALUES ("Nueva nave", new.name);
    END;
    """,
           """
    CREATE TRIGGER IF NOT EXISTS COHETES_AFTER_DELETE
    AFTER DELETE ON COHETES
    BEGIN
        INSERT INTO LOG (Evento, Cohete)
        VALUES ("Nave destruida", old.name);
    END;
    """,
           "INSERT INTO COHETES (rocket_id, name) VALUES ('5e9d0d96eda699382d09d1eD', 'Estrella de La Muerte');",
           "DELETE FROM COHETES WHERE name = 'Estrella de La Muerte';",
           ]

borrar_tablas = [
    "DROP VIEW IF EXISTS LANZAMIENTOS_EXITOSOS",
    "DROP TRIGGER IF EXISTS COHETES_AFTER_INSERT",
    "DROP TRIGGER IF EXISTS COHETES_AFTER_DELETE",
    "DROP TABLE IF EXISTS LOG",
    "DROP TABLE IF EXISTS LANZAMIENTOS",
    "DROP TABLE IF EXISTS PLATAFORMA_LANZAMIENTO",
    "DROP TABLE IF EXISTS CAPSULAS",
    "DROP TABLE IF EXISTS COHETES",
    "DROP TABLE IF EXISTS BUQUES",
    "DROP TABLE IF EXISTS CARGA",
    "DROP TABLE IF EXISTS CORES"
]

tablas = [
    """
    CREATE TABLE IF NOT EXISTS "PLATAFORMA_LANZAMIENTO" (
	"launchpad_id"	VARCHAR(24) UNIQUE,
	"name"	TEXT,
	"full_name"	TEXT,
	"status"	TEXT,
	"locality"	TEXT,
	"region"	TEXT,
	"timezone"	TEXT,
	"latitude"	NUMERIC,
	"longitude"	NUMERIC,
	PRIMARY KEY("launchpad_id")
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "BUQUES" (
	"ship_id"	VARCHAR(24) UNIQUE,
	"name"	TEXT,
	"type"	TEXT,
	"active"	NUMERIC,
	"model"	TEXT DEFAULT NULL,
	"roles"	TEXT,
	"imo"	REAL DEFAULT NULL,
	"mmsi"	REAL DEFAULT NULL,
	"abs"	REAL DEFAULT NULL,
	"class"	REAL DEFAULT NULL,
	"mass_kg"	REAL DEFAULT NULL,
	"mass_lb"	REAL DEFAULT NULL,
	"year_built"	REAL DEFAULT NULL,
	"home_port"	TEXT,
	PRIMARY KEY("ship_id")
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "CAPSULAS" (
	"capsule_id"	VARCHAR(24) UNIQUE,
	"serial"	VARCHAR(4) UNIQUE,
	"status"	TEXT,
	"reuse_count"	INTEGER,
	"water_landings"	INTEGER,
	"land_landings"	INTEGER,
	PRIMARY KEY("capsule_id")
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "CORES" (
	"core_id"	VARCHAR(24) UNIQUE,
	"serial"	TEXT UNIQUE,
	"status"	TEXT,
	"reuse_count"	INTEGER,
	"block"	REAL DEFAULT NULL,
	"rtls_attempts"	INTEGER,
	"rtls_landings"	INTEGER,
	"asds_attempts"	INTEGER,
	"asds_landings"	INTEGER,
	PRIMARY KEY("core_id")
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "CARGA" (
	"payload_id"	VARCHAR(24) UNIQUE,
	"name"	TEXT UNIQUE,
	"type"	TEXT,
	"reused"	NUMERIC,
	"manufacturers"	TEXT,
	"mass_kg"	REAL DEFAULT NULL,
	"mass_lb"	REAL DEFAULT NULL,
	"orbit"	TEXT DEFAULT NULL,
	"reference_system"	TEXT DEFAULT NULL,
	"regime"	TEXT DEFAULT NULL,
	PRIMARY KEY("payload_id")
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "COHETES" (
	"rocket_id"	VARCHAR(24) UNIQUE,
	"name"	TEXT UNIQUE,
	"type"	TEXT,
	"active"	NUMERIC,
	"country"	TEXT,
	"company"	TEXT,
	"height_mt"	REAL,
	"height_ft"	REAL,
	"diameter_mt"	REAL,
	"diameter_ft"	REAL,
	"mass_kg"	INTEGER,
	"mass_lb"	INTEGER,
	"stages"	INTEGER,
	"boosters"	INTEGER,
	"cost_per_launch"	INTEGER,
	"landing_legs"	TEXT,
	"engines"	TEXT,
	PRIMARY KEY("rocket_id")
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS "LANZAMIENTOS" (
	"launch_id"	VARCHAR(24) UNIQUE,
	"name"	TEXT UNIQUE,
	"date"	datetime UNIQUE,
	"rocket_id"	VARCHAR(24),
	"launchpad_id"	VARCHAR(24),
	"success"	NUMERIC,
	"failures"	TEXT,
	"ships"	TEXT,
	"capsules"	TEXT,
	"payloads"	TEXT UNIQUE,
	"cores"	TEXT UNIQUE,
	"fairings_reused"	TEXT DEFAULT 'None',
	"fairings_recovery_attempts"	TEXT DEFAULT 'None',
	"fairings_recovered"	TEXT DEFAULT 'None',
	PRIMARY KEY("launch_id"),
	FOREIGN KEY("capsules") REFERENCES "CAPSULAS"("capsule_id"),
	FOREIGN KEY("cores") REFERENCES "CORES"("core_id"),
	FOREIGN KEY("ships") REFERENCES "BUQUES"("ship_id"),
	FOREIGN KEY("launchpad_id") REFERENCES "PLATAFORMA_LANZAMIENTO"("launchpad_id"),
	FOREIGN KEY("payloads") REFERENCES "CARGA"("payload_id"),
	FOREIGN KEY("rocket_id") REFERENCES "COHETES"("rocket_id")
    );
    """
]
