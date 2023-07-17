# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
"""
import costos as co
import ONEfolio as single

try:
    # Multiple folio data
    # noFolio,tiempoATM,tiempoJet,tiempoCombi,tiempoHT,tiempoStork,tiempoRama,metrosR,costATM,costJet,costCom,costHT,costStork,costRama,velATM,velJet,velCom,velHT,velStork,velRama
    nlcad, nlcd = co.load_data()
    folioDB = co.order_by_folio(nlcad, nlcd)
    co.cal_and_print_all_times(folioDB, nlcad)
    # single folio data
    # folioData = searchFolio(NLCAD, NLCD) buscar un solo folio
except(KeyboardInterrupt()):
    print("error, cierre del programa por usuario, vuelva a correr el programa")
