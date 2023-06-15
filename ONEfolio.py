# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
"""

import pandas as pd
import csv

def searchFolio(NLCAD, NLCD): #Busca la informacion de un folio tanto dentro de la fabrica como en el revisado
    #para asi comparar y conocer su estado.
    print("Busqueda de folio")
    print("Ingrese el folio que desea buscar (Agregue un '.0' al final)")
    FOLIO = input()
    print("Usted desa buscar el folio " + str(FOLIO) + ", oprima ENTER para confirmar, oprima C + ENTER para cancelar")
    ans = input()
    if ans == "c" or ans == "C": #condicion para cancelar, falta mejorarla
        print("Cancel")
        return(ans)
    else: # si no se cancela, se continua
        lenA = len(NLCAD) #Largo de la base de datos de revisado
        for i in range(lenA):
            toSearch = str(NLCAD[i][0]) #Folio a ser comparado con el ingresado/solicitado
            if toSearch == FOLIO: #Comparacion
                print("Folio revisado")
                
        lenB = len(NLCD) #Largo de la base de datos del compilado de produccion
        folioData = []
        for i in range(lenB):
            toSearch = str(NLCD[i][1]) #Folio a ser comparado con el ingresado/solicitado
            if toSearch == FOLIO: #Comparacion
                #print("==============" + str(NLCD[i][:]) + "==============")
                folioData.append(NLCD[i][:]) #se agrega el registro/proceso a la lista
        return(folioData)
