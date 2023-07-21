import pandas as pd


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
        if folio_data[i][5] == "Estampadora":
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


def metros_re(nlcad, i):
    metros_r = nlcad[i][3]
    return metros_r


def cost_maquina(machine_times, cost_l, cost_w, cost_g, general_p_min):
    # noFolio, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama
    cost_p_min_atm, cost_p_min_jet, cost_p_min_com, cost_p_min_ht, cost_p_min_stork, cost_p_min_rama = consumos_maquina(
        cost_w, cost_l, cost_g)
    # costElitex = machineTimes[][]
    cost_atm = machine_times[1] * cost_p_min_atm + machine_times[1] * general_p_min
    cost_jet = machine_times[2] * cost_p_min_jet + machine_times[2] * general_p_min
    cost_com = machine_times[3] * cost_p_min_com + machine_times[3] * general_p_min
    cost_ht = machine_times[4] * cost_p_min_ht + machine_times[4] * general_p_min
    cost_stork = machine_times[5] * cost_p_min_stork + machine_times[5] * general_p_min
    cost_rama = machine_times[6] * cost_p_min_rama + machine_times[6] * general_p_min
    return cost_atm, cost_jet, cost_com, cost_ht, cost_stork, cost_rama


def general():
    gastos_data = pd.read_csv('Gastos.csv',
                              encoding='latin1')  # Lee el archivo de gastos generales
    list_gastos_data = gastos_data.values.tolist()
    net_general = list_gastos_data[0][3]
    net_general = net_general.replace("'", "")
    net_general = net_general.replace(",", "")
    net_general = float(net_general)
    return net_general


def net_times(folio_db, nlcad):
    machine_times = []
    len_c = len(folio_db)  # Largo de la primera dim equivalente al numero de folios revisados
    for i in range(len_c):  # Para cada folio
        folio_to_calc = folio_db[i][:][:]  # Toma la info de cada folio
        if len(folio_db[i][:][:]) > 0:
            no_folio = str(folio_db[i][0][1])  # Toma el folio
            no_folio = no_folio[0:5]
            no_folio = int(no_folio)
            metros_r = metros_re(nlcad, i)  # Metros totales recibidos en almacen
            # se envia el folio al que se desa calcular el tiempode cada maquina
            tiempo_atm, tiempo_jet, tiempo_combi, tiempo_ht, tiempo_stork, tiempo_rama = time_p_folio(folio_to_calc)
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
    return n_times


def consumos_maquina(cost_w, cost_l, cost_g):
    cost_p_min_atm = (0.0453334 * 1.478 * cost_l) + (0 * cost_w) + (0.1605555555555556 * cost_g)  #
    cost_p_min_jet = (0.3956667 * 1.478 * cost_l) + (0 * cost_w) + (0.1805555555555556 * cost_g)  #
    cost_p_min_com = (0.3483334 * 1.478 * cost_l) + (0 * cost_w) + (0.40625 * cost_g)  #
    cost_p_min_ht = (0.156667 * 1.478 * cost_l) + (0 * cost_w) + (0.3159722222222222 * cost_g)  #
    cost_p_min_stork = (0.62 * 1.478 * cost_l) + (0 * cost_w) + (2.03125 * cost_g)  #
    cost_p_min_rama = (0.870066855668766 * 1.478 * cost_l) + (0 * cost_w) + (0.7899305555555556 * cost_g)  #
    return cost_p_min_atm, cost_p_min_jet, cost_p_min_com, cost_p_min_ht, cost_p_min_stork, cost_p_min_rama
