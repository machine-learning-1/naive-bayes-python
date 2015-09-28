import csv
import random
from collections import Counter
from matplotlib import pyplot as plt

def loadCsv(archivo):
	lines = csv.reader(open(archivo,"rb"))
	dataSet = list(lines)
	return dataSet

def categorias(datos):
	categorias_datos={}
	for i in range(len(datos)):
		if datos[i][-1] not in categorias_datos:
			categorias_datos[datos[i][-1]] = 1
		else:
			categorias_datos[datos[i][-1]] = categorias_datos[datos[i][-1]] + 1 
	return categorias_datos

def splitDataset(datos, porcentaje):
	Train_Size = int(len(datos)*porcentaje)
	TrainSet = []
	copy = list(datos)
	while len(TrainSet)<Train_Size:
		index = random.randrange(len(copy))
		TrainSet.append(copy.pop(index))
	return [TrainSet, copy]

def features(p):
	contadores = {}
	for x in range(len(p)):	
		y = Counter(p[x])
		contadores[x] = y
	return contadores

def clases(entrenamiento):
	separated = {}
	for i in range(len(entrenamiento)):
		vector = entrenamiento[i]
		if (vector[-1]) not in separated:
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated

def entrenamiento(entrenamiento, categorico, testData):
	categoria = ""
	probCategoria = 0
	p = zip(*entrenamiento)
	frecuencia_features = features(p)
	por_categorias = clases(entrenamiento)
	probabilidad = 0
	cat = int(len(frecuencia_features)) - 1
	for c in categorico:
		prob_categorias = float(categorico[c])/len(entrenamiento)
		x = zip(*por_categorias[c])
		prob = prob_categorias
		for i in range(cat):
			contador = Counter(x[i])
			prob_feature = float(contador[testData[i]])/float(categorico[c])
			if prob_feature == 0:
				prob_feature = 0.001 #corrector laplaciano
			
			prob = prob*prob_feature
		if probCategoria<prob:
			categoria=c
			probCategoria = prob
	return (categoria,probCategoria)

def main():
	porcentaje = 0.7
	dataTraining, testData = splitDataset(datos, porcentaje)
	prueba = ['YELLOW', 'SMALL', 'DIP', 'CHILD'] #es true
	categorico = categorias(dataTraining)
	queCategoria, cualProb = entrenamiento(dataTraining, categorico, prueba)
	print('Pertenece a la categoria: {0}, con una probabilidad de {1}').format(queCategoria,cualProb)

archivo="datos-prueba-discritos.csv"
datos = loadCsv(archivo)

def itera():
	porcentaje = 0.4
	performance = []
	for i in range(6):
		contador = 0
		promedio = 0
		x = [50 , 60 ,70 , 80 , 90 , 100]
		porcentaje = porcentaje + 0.1
		print porcentaje
		dataTraining, testData = splitDataset(datos, porcentaje)
		categorico = categorias(dataTraining)
		for n in range(len(testData)):
			queCategoria, cualProb = entrenamiento(dataTraining, categorico, testData[n])
			if testData[n][-1] == queCategoria:
				contador = contador + 1
			if  n == (len(testData)-1):
				promedio = (float(contador)/len(testData))*100
				performance.append(promedio)
	plt.plot(x, performance, color='green', marker='o', linestyle='solid')
	plt.show()
			#print('Pertenece a la categoria: {0}, con una probabilidad de {1}').format(queCategoria,cualProb)

itera()
