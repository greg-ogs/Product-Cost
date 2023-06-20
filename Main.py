# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
"""
import costos as co
import ONEfolio as single

try:
    #Multiple folio data
    NLCAD, NLCD = co.loadData()
    folioDB = co.orderByFolio(NLCAD, NLCD)
    co.calAndPrintAllTimes(folioDB, NLCAD)
    #single folio data
    #folioData = searchFolio(NLCAD, NLCD) buscar un solo folio
except(KeyboardInterrupt()):
    print("error, cierre del programa por usuario, vuelva a correr el programa")