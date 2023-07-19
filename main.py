import costos as co
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Costos")
        self.setGeometry(50, 50, 400, 300)

        self.label = QLabel("En espera", self)
        self.label.setGeometry(50, 50, 200, 30)

        self.button = QPushButton("Haz clic", self)
        self.button.setGeometry(50, 100, 100, 30)
        self.button.clicked.connect(self.on_button_click)


    def on_button_click(self):
        # Crear un hilo secundario para ejecutar el cálculo
        calculation_thread = threading.Thread(target=self.run_calculation)
        calculation_thread.start()

    def run_calculation(self):
        co.main_thread()
        self.label.setText("¡Reporte generado!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
