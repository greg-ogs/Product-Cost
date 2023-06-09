# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
"""

import pandas as pd
import numpy as np

def loadData():
    compiladoData = pd.read_csv('compilado.csv', encoding = 'latin1')
    shapeA = compiladoData.shape
       
    ListCompiladoData = compiladoData.values.tolist()
    NLCD = []
    for i in range(shapeA[0]):
        if str(ListCompiladoData[i][1]) != "nan":
            NLCD.append(ListCompiladoData[:][i])
    
    calidadData = pd.read_csv('calidad.csv', encoding = 'latin1')
    shapeB = calidadData.shape
    
    ListCalidadData = calidadData.values.tolist()
    NLCAD = []
    for i in range(shapeB[0]):
        if str(ListCalidadData[i][0]) != "nan":
            NLCAD.append(ListCalidadData[:][i])
    return(NLCAD, NLCD)        
    

def searchFolio(NLCAD, NLCD):
    print("Busqueda de folio")
    FOLIO = input()
    print("Usted desa buscar el folio " + str(FOLIO) + ", oprima ENTER para confirmar, oprima C + ENTER para cancelar")
    ans = input()
    if ans == "c" or ans == "C":
        print("Cancel")
        return(ans)
    else:
        lenA = len(NLCAD)
        for i in range(lenA):
            toSearch = str(NLCAD[i][0])
            if toSearch == FOLIO:
                print("Folio revisado")
                
        lenB = len(NLCD)
        folioData = []
        for i in range(lenB):
            toSearch = str(NLCD[i][1])
            if toSearch == FOLIO:
                #print("==============" + str(NLCD[i][:]) + "==============")
                folioData.append(NLCD[i][:])
        return(folioData)
    
try:
    NLCAD, NLCD = loadData()
    folioData = searchFolio(NLCAD, NLCD)
    
    #ADD TO MACHINE
    #Rama
    tiempoRama = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Rama Bruckner":
            tiempoRama = tiempoRama + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Rama es:" + str(tiempoRama) + " minutos ")
    print("=============================================")    

    #Stork
    tiempoStork = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Estampadora":
            tiempoStork = tiempoStork + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Estampadora es:" + str(tiempoStork) + " minutos ")
    print("=============================================")    
    
    #Jigger HT
    tiempoHT = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Jigger HT":
            tiempoHT = tiempoHT + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Jigger HT es:" + str(tiempoHT) + " minutos ")
    print("=============================================")  
    
    #Jigger Combi
    tiempoCombi = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Jigger Combi":
            tiempoCombi = tiempoCombi + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Jigger Combi es:" + str(tiempoCombi) + " minutos ")
    print("=============================================")
    
    #Jet
    tiempoJet = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Jet 1" or folioData[i][5] == "Jet 2":
            tiempoJet = tiempoJet + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Jet es:" + str(tiempoJet) + " minutos ")
    print("=============================================")
    
    
except(KeyboardInterrupt()):
    print("error, cierre del programa por usuario, vuelva a correr el programa")