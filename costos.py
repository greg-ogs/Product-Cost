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

def orderByFolio(NLCAD, NLCD):
#Replica la funcion folioData pero para todos los folios
    folioDB = []
    lenA = len(NLCAD) #Largo de la base de datos de revisado
    for i in range(lenA):
        toSearchA = str(NLCAD[i][0]) #Folio a ser comparado
        toSearchA = toSearchA[0:5]
        lenB = len(NLCD) #Largo de la base de datos del compilado de produccion
        folioData = []
        for j in range(lenB):
            toSearchB = str(NLCD[j][1]) #Folio a ser comparado 
            toSearchB = toSearchB[0:5]
            if toSearchA == toSearchB: #Comparacion
                #print("==============" + str(NLCD[i][:]) + "==============")
                folioData.append(NLCD[j][:])
        folioDB.append(folioData) #Crea una matriz de 3D donde:
            #La primera dim es para cada folio diferente
            #La segunda dim es para cada registro de ese folio
            #La tercera es para cada dato de ese registro
    return(folioDB)

def calAndPrintAllTimes(folioDB, NLCAD): #Funcion que recolecta el resultado de varias
    #toma la base de datos tridimencional y busca en cada folio (primera dim)
    #En cada una manda a llamar la funcion de tiempo total por folio 
    #para asi dar el tiempo total de maquina para cada folio
    lenC = len(folioDB) #Largo de la primera dim equivalente al numero de folios revisados
    times = []
    for i in range(lenC): #Para cada folio 
        folioToCalc = folioDB[i][:][:] #Toma la info de cada folio
        if len(folioDB[i][:][:]) > 0:
            noFolio = str(folioDB[i][0][1]) #Toma el folio
            noFolio = noFolio[0:5]
            noFolio = int(noFolio)
            metrosR = metrosRe(NLCAD, i) #Metros totales recibidos en almacen
            #se envia el folio al que se desa calcular el tiempode cada maquina
            tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama = timePFolio(folioToCalc)
            #Se toman los tiempos que devolvieron y se calcula la velocidad de produccion por maquina
            velATM, velJet, velCom, velHT, velStork, velRama = timePerMeter(metrosR, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama) #Tiempo de maquina por metro
            # se guarda todo en una lista
            machineTimes = [noFolio, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama, metrosR, velATM, velJet, velCom, velHT, velStork, velRama] #Var to incert into csv
            #Call cost function
            costATM ,costJet, costCom ,costHT, costEstampadora, costRama = costomaquina(machineTimes)
            #Add cost per machine 
            machineCost = [noFolio, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama, metrosR, velATM, velJet, velCom, velHT, velStork, velRama, costATM ,costJet, costCom ,costHT, costEstampadora, costRama]
            #Se agrega a una matriz con la forma folio-tiempos-velocidades
            times.append(machineCost)
    #al terminar de recorrer todos los folios se imprime en un archivo delimitados por comas
    with open('TimePMachine.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times)
        file.close()
    return(machineTimes, times)

def timePFolio(folioData):    #Calcula el tiempo de cada maquina para un folio
    #El argumento es la informacion de un folio, es decir, los procesos de cada folio dentro de la fabrica
    #ADD TO MACHINE
    
    #Rama
    tiempoRama = 0
    lenFD = len(folioData) #tamaño de la lista con la informacion del folio
    for i in range(lenFD): #corre en el largo de la lista con la informacion del folio
        if folioData[i][5] == "Rama Bruckner" or folioData[i][5] == "Rama bruckner": #compara la cadena para determinar si es de una maquina u otra
            tiempoRama = tiempoRama + int(folioData[i][11]) #Suma los tiempos si concide la maquina
    print("=============================================")
    print("El tiempo total en Rama es:" + str(tiempoRama) + " minutos ") #Imprime el tiempo
    print("=============================================")    
    
    #Stork
    tiempoStork = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Estampadora Stork":
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
        if folioData[i][5] == "Jigger Combi" or folioData[i][5] == "Jigger combi":
            tiempoCombi = tiempoCombi + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Jigger Combi es:" + str(tiempoCombi) + " minutos ")
    print("=============================================")
    
    #Jigger ATM
    tiempoATM = 0
    lenFD = len(folioData)
    for i in range(lenFD):
        if folioData[i][5] == "Jigger ATM":
            tiempoATM = tiempoATM + int(folioData[i][11])
    print("=============================================")
    print("El tiempo total en Jigger ATM es:" + str(tiempoCombi) + " minutos ")
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
    
    return(tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama)


def timePerMeter(metrosR, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama):
    if tiempoATM > 0:
        velATM = metrosR/tiempoATM
    else:
        velATM = 0
    if tiempoJet > 0: 
        velJet = metrosR/tiempoJet
    else:
        velJet = 0
    if tiempoCombi > 0:
        velCom = metrosR/tiempoCombi
    else:
        velCom = 0
    if tiempoHT > 0:
        velHT = metrosR/tiempoHT
    else:
        velHT = 0
    if tiempoStork > 0:
        velStork =metrosR/tiempoStork
    else:
        velStork = 0
    if tiempoRama > 0:
        velRama = metrosR/tiempoRama
    else: 
        velRama = 0
    return(velATM, velJet, velCom, velHT, velStork, velRama)
 
def metrosRe(NLCAD, i):
    metrosR = NLCAD[i][3]
    return(metrosR)

def costomaquina(machineTimes):
    #noFolio, tiempoATM, tiempoJet, tiempoCombi, tiempoHT, tiempoStork, tiempoRama
    costPminRama = 10#input()
    costPminEstampadora = 10#input()
    costPminHT = 10#input()
    costPminATM = 10#input()
    costPminJet = 10#input()
    costPminCom = 10#input()
    #costPminElitex = input()
    #costElitex = machineTimes[][]
    costRama = machineTimes[6]*costPminRama
    costEstampadora = machineTimes[5]*costPminEstampadora
    costHT = machineTimes[4]*costPminHT
    costATM = machineTimes[1]*costPminATM
    costJet = machineTimes[2]*costPminJet
    costCom = machineTimes[3]*costPminCom
    return(costATM ,costJet, costCom ,costHT, costEstampadora, costRama)

def consumosMaquina():
    costPminRama = (costtoAgua*consumoAguaR)+(costoLuz*consumoLuzR)+(costoGas*ConsumoGasR)
