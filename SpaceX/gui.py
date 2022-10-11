from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from SpaceX.gui_botones import (
    Descargar_Lanzamientos_Exitosos,
    Ver_Lanzamientos_Exitosos,
    Ver_LOG,
    Descargar_LOG
)


class Window(QMainWindow):
    def __init__(self, bbdd, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SpaceX Data (2006 - 2021)")
        self.resize(500, 250)

        # Configuración de los botones
        box = QVBoxLayout()
        self.window1 = Ver_Lanzamientos_Exitosos()
        self.window2 = Descargar_Lanzamientos_Exitosos(bbdd)
        self.window3 = Ver_LOG()
        self.window4 = Descargar_LOG(bbdd)

        # Configuración botón 1
        button1 = QPushButton("Ver tabla de lanzamientos exitosos")
        button1.clicked.connect(
            lambda checked: self.toggle_window(self.window1)
        )
        button1.setFont(QFont('Times', 30))
        box.addWidget(button1)

        # Configuración botón 2. Muestra/oculta la tabla
        button2 = QPushButton("Descargar lanzamientos exitosos en csv")
        button2.clicked.connect(
            lambda checked: self.toggle_window(self.window1)
        )
        button2.setFont(QFont('Times', 30))
        box.addWidget(button2)

        # Configuración botón 3
        button3 = QPushButton("Ver registro de LOG")
        button3.clicked.connect(
            lambda checked: self.toggle_window(self.window3)
        )
        button3.setFont(QFont('Times', 30))
        box.addWidget(button3)

        # Configuración botón 4. Muestra/oculta la tabla
        button4 = QPushButton("Descargar registro de LOG en csv")
        button4.clicked.connect(
            lambda checked: self.toggle_window(self.window3)
        )
        button4.setFont(QFont('Times', 30))
        box.addWidget(button4)

        # Configuración widgets
        widget = QWidget()
        widget.setLayout(box)
        self.setCentralWidget(widget)

        # Configuración estilo de la ventana
        estilo = """
            color: white;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
                                stop: 0 #024b59, stop: 1 #001317);
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: white;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;        
        """
        self.setStyleSheet(estilo)

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            window.show()
