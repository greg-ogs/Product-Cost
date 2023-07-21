# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
Aqui no usamos self porque somos medio masoqyistas

Y tambien esta el porque no es bueno trabajar en empresas pequeñas donde el dueño se siente un sabelotodo y
no quiere comprar medidores asi que aqui me tienen haciendo adivinanzas para aproximar el consumo
"""

import costos as co
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import threading
import csv
import pandas as pd


class Back:

    @staticmethod
    def main_thread():
        nlcad, nlcd = Back.load_data()
        folio_db = Back.order_by_folio(nlcad, nlcd)
        Back.call_and_print_all_times(folio_db, nlcad)

    @staticmethod
    def load_data():
        compilado_data = pd.read_csv('compilado.csv',
                                     encoding='latin1')  # Lee el archivo de compilado de produccion "procesos"
        shape_a = compilado_data.shape  # Dimencion de la base de datos

        list_compilado_data = compilado_data.values.tolist()  # pasa de dataframe a lista
        # Eliminar valores nan
        nlcd = []
        # Recorre la lista en busca de valores nan
        for i in range(shape_a[0]):
            if str(list_compilado_data[i][1]) != "nan":
                nlcd.append(list_compilado_data[:][i])  # Si cumple la condicion los agrega a una lista vacia

        calidad_data = pd.read_csv('calidad.csv', encoding='latin1')  # repite lo anterior pero con la lista de revisado
        shape_b = calidad_data.shape

        list_calidad_data = calidad_data.values.tolist()
        nlcad = []
        for i in range(shape_b[0]):
            if str(list_calidad_data[i][0]) != "nan":
                nlcad.append(list_calidad_data[:][i])
        return nlcad, nlcd

    @staticmethod
    def order_by_folio(nlcad, nlcd):
        # Replica la funcion folio_data pero para todos los folios
        folio_db = []
        len_a = len(nlcad)  # Largo de la base de datos de revisado
        for i in range(len_a):
            to_search_a = str(nlcad[i][0])  # Folio a ser comparado
            to_search_a = to_search_a[0:5]
            len_b = len(nlcd)  # Largo de la base de datos del compilado de produccion
            folio_data = []
            for j in range(len_b):
                to_search_b = str(nlcd[j][1])  # Folio a ser comparado
                to_search_b = to_search_b[0:5]
                if to_search_a == to_search_b:  # Comparacion
                    # print("==============" + str(NLCD[i][:]) + "==============")
                    folio_data.append(nlcd[j][:])
            folio_db.append(folio_data)  # Crea una matriz de 3D donde:
            # La primera dim es para cada folio diferente
            # La segunda dim es para cada registro de ese folio
            # La tercera es para cada dato de ese registro
        return folio_db

    @staticmethod
    def call_and_print_all_times(folio_db, nlcad):  # Funcion que recolecta el resultado de varias
        # toma la base de datos tridimencional y busca en cada folio (primera dim)
        # En cada una manda a llamar la funcion de tiempo total por folio
        # para asi dar el tiempo total de maquina para cada folio
        len_c = len(folio_db)  # Largo de la primera dim equivalente al numero de folios revisados
        # ask for cost
        # cost_l = float(input("Cual es el precio de la luz?"))
        # cost_w = float(input("Cual es el precio de el agua?"))
        # cost_g = float(input("Cuales el precio del gas?"))
        cost_l = 3.1012
        cost_w = 0
        cost_g = 8.65
        times = []
        n_times = co.net_times(folio_db, nlcad)  # Calculo del tiempo general y por maquina
        net_general = co.general()  # Money per week
        general_p_min = net_general / n_times  # Per minute

        for i in range(len_c):  # Para cada folio
            folio_to_calc = folio_db[i][:][:]  # Toma la info de cada folio
            if len(folio_db[i][:][:]) > 0:
                no_folio = str(folio_db[i][0][1])  # Toma el folio
                no_folio = no_folio[0:5]
                no_folio = int(no_folio)
                metros_r = co.metros_re(nlcad, i)  # Metros totales recibidos en almacen
                # se envia el folio al que se desa calcular el tiempode cada maquina
                tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama = co.time_p_folio(
                    folio_to_calc)
                # Se toman los tiempos que devolvieron y se calcula la velocidad de produccion por maquina
                vel_atm, vel_jet, vel_com, vel_ht, vel_stork, vel_rama = co.time_per_meter(metros_r, tiempo_atm,
                                                                                           tiempo_jet,
                                                                                           tiempo_combi,
                                                                                           tiempo_ht, tiempo_stork,
                                                                                           tiempo_rama)  # Tiempo de maquina
                # por metro
                # se guarda en una lista
                machine_times = [no_folio, tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama,
                                 metros_r, vel_atm, vel_jet, vel_com, vel_ht, vel_stork, vel_rama]
                # Var to incert into csv
                # Call cost function
                cost_atm, cost_jet, cost_com, cost_ht, cost_stork, cost_rama = co.cost_maquina(machine_times, cost_l,
                                                                                               cost_w,
                                                                                               cost_g, general_p_min)
                # Add cost per machine
                machine_cost = [no_folio, tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama,
                                metros_r, cost_atm, cost_jet, cost_com, cost_ht, cost_stork, cost_rama, vel_atm,
                                vel_jet,
                                vel_com,
                                vel_ht, vel_stork, vel_rama]
                # Se agrega a una matriz con la forma folio-tiempos-velocidades
                times.append(machine_cost)
        # al terminar de recorrer todos los folios se imprime en un archivo delimitados por comas

        with open('Cost.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(times)
            file.close()


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
        Back.main_thread()
        self.label.setText("¡Reporte generado!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
