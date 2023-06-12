# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:07:01 2023

@author: Gregorio Alejandro Oropeza Gomez
"""

import pandas as pd
import csv

def loadData():
    compiladoData = pd.read_csv('compilado.csv', encoding = 'latin1')#Lee el archivo de compilado de produccion "procesos"
    shapeA = compiladoData.shape#Dimencion de la base de datos
       
    ListCompiladoData = compiladoData.values.tolist()#pasa de dataframe a lista
    #Eliminar valores nan
    NLCD = []
    #Recorre la lista en busca de valores nan
    for i in range(shapeA[0]):
        if str(ListCompiladoData[i][1]) != "nan":
            NLCD.append(ListCompiladoData[:][i]) #Si cumple la condicion los agrega a una lista vacia
    
    calidadData = pd.read_csv('calidad.csv', encoding = 'latin1')#repite lo anterior pero con la lista de revisado
    shapeB = calidadData.shape
    
    ListCalidadData = calidadData.values.tolist()
    NLCAD = []
    for i in range(shapeB[0]):
        if str(ListCalidadData[i][0]) != "nan":
            NLCAD.append(ListCalidadData[:][i])
    return(NLCAD, NLCD)        
    

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

def timePFolio(folioData):    #Calcula el tiempo de cada maquina para un folio
    #El argumento es la informacion de un folio, es decir, los procesos de cada folio dentro de la fabrica
    #ADD TO MACHINE
    
    #Rama
    tiempoRama = 0
    lenFD = len(folioData) #tamaño de la lista con la informacion del folio
    for i in range(lenFD): #corre en el largo de la lista con la informacion del folio
        if folioData[i][5] == "Rama Bruckner": #compara la cadena para determinar si es de una maquina u otra
            tiempoRama = tiempoRama + int(folioData[i][11]) #Suma los tiempos si concide la maquina
    print("=============================================")
    print("El tiempo total en Rama es:" + str(tiempoRama) + " minutos ") #Imprime el tiempo
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
    
    return(tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama)

def orderByFolio(NLCAD, NLCD):
#Replica la funcion folioData pero para todos los folios
    folioDB = []
    lenA = len(NLCAD) #Largo de la base de datos de revisado
    for i in range(lenA):
        toSearchA = str(NLCAD[i][0]) #Folio a ser comparado
        lenB = len(NLCD) #Largo de la base de datos del compilado de produccion
        folioData = []
        for j in range(lenB):
            toSearchB = str(NLCD[j][1]) #Folio a ser comparado 
            if toSearchA == toSearchB: #Comparacion
                #print("==============" + str(NLCD[i][:]) + "==============")
                folioData.append(NLCD[j][:])
        folioDB.append(folioData) #Crea una matriz de 3D donde:
            #La primera dim es para cada folio diferente
            #La segunda dim es para cada registro de ese folio
            #La tercera es para cada dato de ese registro
    return(folioDB)

def calAndPrintAllTimes(folioDB):
    lenC = len(folioDB) #Largo de la primera dim equivalente al numero de folios revisados
    times = []
    for i in range(lenC): #Para cada folio 
        folioToCalc = folioDB[i][:][:] #Toma la info de cada folio
        if len(folioDB[i][:][:]) > 0:
            noFolio = str(folioDB[i][0][1]) #Toma el folio
            noFolio = noFolio[0:5]
            noFolio = int(noFolio)
        tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama = timePFolio(folioToCalc)
        machineTimes = [noFolio, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama] 
        times.append(machineTimes)
    with open('TimePMachine.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times)
        file.close()
        
