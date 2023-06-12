# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
"""
import pandas as pd
import csv
import costos

try:
    NLCAD, NLCD = costos.loadData()
    #folioData = searchFolio(NLCAD, NLCD) buscar un solo folio
    folioDB = costos.orderByFolio(NLCAD, NLCD)
    costos.calAndPrintAllTimes(folioDB)


except(KeyboardInterrupt()):
    print("error, cierre del programa por usuario, vuelva a correr el programa")