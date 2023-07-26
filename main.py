# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
Aqui casi no usamos self porque somos medio masoqyistas

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
    def time_p_folio(folio_data):  # Calcula el tiempo de cada maquina para un folio
        # El argumento es la informacion de un folio, es decir, los procesos de cada folio dentro de la fabrica
        # ADD TO MACHINE
        # Rama
        tiempo_rama = 0
        len_fd = len(folio_data)  # tamaño de la lista con la informacion del folio
        for i in range(len_fd):  # corre en el largo de la lista con la informacion del folio
            if folio_data[i][5] == "Rama Bruckner" or folio_data[i][5] == "Rama bruckner":  # compara la cadena para
                # determinar si es de una maquina u otra
                tiempo_rama = tiempo_rama + int(folio_data[i][11])  # Suma los tiempos si concide la maquina
        # Stork
        tiempo_stork = 0
        len_fd = len(folio_data)
        for i in range(len_fd):
            if folio_data[i][5] == "Estampadora" or folio_data[i][5] == "Estampadora Storck":
                tiempo_stork = tiempo_stork + int(folio_data[i][11])
        # Jigger HT
        tiempo_ht = 0
        len_fd = len(folio_data)
        for i in range(len_fd):
            if folio_data[i][5] == "Jigger HT":
                tiempo_ht = tiempo_ht + int(folio_data[i][11])
        # Jigger Combi
        tiempo_combi = 0
        len_fd = len(folio_data)
        for i in range(len_fd):
            if folio_data[i][5] == "Jigger Combi" or folio_data[i][5] == "Jigger combi":
                tiempo_combi = tiempo_combi + int(folio_data[i][11])
        # Jigger ATM
        tiempo_atm = 0
        len_fd = len(folio_data)
        for i in range(len_fd):
            if folio_data[i][5] == "Jigger ATM":
                tiempo_atm = tiempo_atm + int(folio_data[i][11])
        # Jet
        tiempo_jet = 0
        len_fd = len(folio_data)
        for i in range(len_fd):
            if folio_data[i][5] == "Jet 1" or folio_data[i][5] == "Jet 2":
                tiempo_jet = tiempo_jet + int(folio_data[i][11])
        return tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama

    @staticmethod
    def metros_re(nlcad, i):
        metros_r = nlcad[i][3]
        return metros_r

    @staticmethod
    def cost_maquina(machine_times, cost_l, cost_w, cost_g, general_p_min, nom_p_min_jig, nom_p_min_stork,
                     nom_p_min_rama):
        # noFolio, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama
        cost_p_min_atm, cost_p_min_jet, cost_p_min_com, cost_p_min_ht, cost_p_min_stork, cost_p_min_rama = \
            Back.consumos_maquina(cost_w, cost_l, cost_g)
        # costElitex = machineTimes[][]
        cost_atm = machine_times[1] * cost_p_min_atm + machine_times[1] * general_p_min + machine_times[
            1] * nom_p_min_jig
        cost_jet = machine_times[2] * cost_p_min_jet + machine_times[2] * general_p_min + machine_times[
            2] * nom_p_min_jig
        cost_com = machine_times[3] * cost_p_min_com + machine_times[3] * general_p_min + machine_times[
            3] * nom_p_min_jig
        cost_ht = machine_times[4] * cost_p_min_ht + machine_times[4] * general_p_min + machine_times[4] * nom_p_min_jig
        cost_stork = machine_times[5] * cost_p_min_stork + machine_times[5] * general_p_min + machine_times[
            5] * nom_p_min_stork
        cost_rama = machine_times[6] * cost_p_min_rama + machine_times[6] * general_p_min + machine_times[
            6] * nom_p_min_rama
        return cost_atm, cost_jet, cost_com, cost_ht, cost_stork, cost_rama

    @staticmethod
    def read_gastos_csv():
        gastos_data = pd.read_csv('Gastos.csv',
                                  encoding='latin1')  # Lee el archivo de gastos generales
        list_gastos_data = gastos_data.values.tolist()
        return list_gastos_data

    @staticmethod
    def general():
        list_gastos_data = Back.read_gastos_csv()
        net_general = list_gastos_data[0][16]
        #   print(net_general)
        net_general = net_general.replace("'", "")
        net_general = net_general.replace(",", "")
        net_general = float(net_general)
        return net_general

    @staticmethod
    def nom():
        list_gastos_data = Back.read_gastos_csv()
        nom_jiggers = list_gastos_data[0][7]
        nom_stork = list_gastos_data[0][17]
        nom_rama = list_gastos_data[0][6]
        return nom_jiggers, nom_stork, nom_rama

    @staticmethod
    def nom_p_min(ne_times):
        nom_jiggers, nom_stork, nom_rama = Back.nom()
        jigger_times = ne_times[0] + ne_times[1] + ne_times[2] + ne_times[3]
        nom_p_min_jig = nom_jiggers / jigger_times
        nom_p_min_stork = nom_stork / ne_times[4]
        nom_p_min_rama = nom_rama / ne_times[5]
        return nom_p_min_jig, nom_p_min_stork, nom_p_min_rama

    @staticmethod
    def net_times(folio_db, nlcad):
        machine_times = []
        len_c = len(folio_db)  # Largo de la primera dim equivalente al numero de folios revisados
        for i in range(len_c):  # Para cada folio
            folio_to_calc = folio_db[i][:][:]  # Toma la info de cada folio
            if len(folio_db[i][:][:]) > 0:
                no_folio = str(folio_db[i][0][1])  # Toma el folio
                no_folio = no_folio[0:5]
                no_folio = int(no_folio)
                metros_r = Back.metros_re(nlcad, i)  # Metros totales recibidos en almacen
                # se envia el folio al que se desa calcular el tiempode cada maquina
                tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama = Back.time_p_folio(folio_to_calc)
                times_p_machine = [tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama]
                machine_times.append(times_p_machine)
        len_a = len(machine_times)
        total_atm = 0
        total_jet = 0
        total_combi = 0
        total_ht = 0
        total_stork = 0
        total_rama = 0
        for i in range(len_a):
            total_atm = total_atm + machine_times[i][0]
            total_jet = total_jet + machine_times[i][1]
            total_combi = total_combi + machine_times[i][2]
            total_ht = total_ht + machine_times[i][3]
            total_stork = total_stork + machine_times[i][4]
            total_rama = total_rama + machine_times[i][5]
        ne_times = [total_atm, total_jet, total_combi, total_ht, total_stork, total_rama]
        n_times = sum(ne_times)
        return n_times, ne_times

    @staticmethod
    def consumos_maquina(cost_w, cost_l, cost_g):
        cost_p_min_atm = (0.0453334 * 1.478 * cost_l) + (0 * cost_w) + (0.1605555555555556 * cost_g)  #
        cost_p_min_jet = (0.3956667 * 1.478 * cost_l) + (0 * cost_w) + (0.1805555555555556 * cost_g)  #
        cost_p_min_com = (0.3483334 * 1.478 * cost_l) + (0 * cost_w) + (0.40625 * cost_g)  #
        cost_p_min_ht = (0.156667 * 1.478 * cost_l) + (0 * cost_w) + (0.3159722222222222 * cost_g)  #
        cost_p_min_stork = (0.62 * 1.478 * cost_l) + (0 * cost_w) + (2.03125 * cost_g)  #
        cost_p_min_rama = (0.870066855668766 * 1.478 * cost_l) + (0 * cost_w) + (0.7899305555555556 * cost_g)  #
        return cost_p_min_atm, cost_p_min_jet, cost_p_min_com, cost_p_min_ht, cost_p_min_stork, cost_p_min_rama

    @staticmethod
    def time_per_meter(metros_r, tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama):
        if tiempo_atm > 0:
            vel_atm = metros_r / tiempo_atm
        else:
            vel_atm = 0
        if tiempo_jet > 0:
            vel_jet = metros_r / tiempo_jet
        else:
            vel_jet = 0
        if tiempo_combi > 0:
            vel_com = metros_r / tiempo_combi
        else:
            vel_com = 0
        if tiempo_ht > 0:
            vel_ht = metros_r / tiempo_ht
        else:
            vel_ht = 0
        if tiempo_stork > 0:
            vel_stork = metros_r / tiempo_stork
        else:
            vel_stork = 0
        if tiempo_rama > 0:
            vel_rama = metros_r / tiempo_rama
        else:
            vel_rama = 0
        return vel_atm, vel_jet, vel_com, vel_ht, vel_stork, vel_rama

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
        title = ["no_folio", "tiempo_atm", "tiempo_jet", "tiempo_combi", "tiempo_ht", "tiempo_stork", "tiempo_rama",
                 "metros_en_almacen", "costo_atm", "costo_jet", "costo_com", "costo_ht", "costo_stork", "costo_rama",
                 "vel_atm", "vel_jet", "vel_com", "vel_ht", "vel_stork", "vel_rama"]
        times = [title]
        n_times, ne_times = Back.net_times(folio_db, nlcad)  # Calculo del tiempo general y por maquina
        net_general = Back.general()  # Money per week
        general_p_min = net_general / n_times  # Per minute
        nom_p_min_jig, nom_p_min_stork, nom_p_min_rama = Back.nom_p_min(ne_times)
        for i in range(len_c):  # Para cada folio
            folio_to_calc = folio_db[i][:][:]  # Toma la info de cada folio
            if len(folio_db[i][:][:]) > 0:
                no_folio = str(folio_db[i][0][1])  # Toma el folio
                no_folio = no_folio[0:5]
                no_folio = int(no_folio)
                metros_r = Back.metros_re(nlcad, i)  # Metros totales recibidos en almacen
                # se envia el folio al que se desa calcular el tiempode cada maquina
                tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama = Back.time_p_folio(
                    folio_to_calc)
                # Se toman los tiempos que devolvieron y se calcula la velocidad de produccion por maquina
                vel_atm, vel_jet, vel_com, vel_ht, vel_stork, vel_rama = Back.time_per_meter(metros_r, tiempo_atm,
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
                cost_atm, cost_jet, cost_com, cost_ht, cost_stork, cost_rama = Back.cost_maquina(machine_times, cost_l,
                                                                                               cost_w,
                                                                                               cost_g, general_p_min,
                                                                                               nom_p_min_jig,
                                                                                               nom_p_min_stork,
                                                                                               nom_p_min_rama)
                # Add cost per machine
                machine_cost = [no_folio, tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama,
                                metros_r, cost_atm, cost_jet, cost_com, cost_ht, cost_stork, cost_rama, vel_atm,
                                vel_jet,
                                vel_com,
                                vel_ht, vel_stork, vel_rama]
                # Se agrega a una matriz con la forma folio-tiempos-velocidades
                times.append(machine_cost)
        # al terminar de recorrer todos los folios se imprime en un archivo delimitados por comas

        with open('Costos.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(times)
            file.close()

    @staticmethod
    def main_thread():
        nlcad, nlcd = Back.load_data()
        folio_db = Back.order_by_folio(nlcad, nlcd)
        Back.call_and_print_all_times(folio_db, nlcad)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Estimacion de costos")
        self.setGeometry(50, 50, 400, 300)

        self.label = QLabel("En espera...", self)
        self.label.setGeometry(155, 70, 300, 30)

        self.button = QPushButton("Haz clic pa generar el reporte", self)
        self.button.setGeometry(50, 100, 300, 30)
        self.button.setStyleSheet("background-color: #1DA1F2; color: white; font-size: 16px;")
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
