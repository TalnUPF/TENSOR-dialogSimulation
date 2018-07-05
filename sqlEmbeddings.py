# -*- coding: utf-8 -*-

import MySQLdb
import utils
import numpy as np
from scipy.spatial.distance import cdist

class SQLEmbeddings:

	def __init__(self, dbname="Embeddings"):
		#self.db = MySQLdb.connect(host="10.80.28.153", user="monica", passwd="joanGuapete", db=dbname, use_unicode=True) 
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="pany8491", db=dbname, use_unicode=True) 


	def getWordVector(self, word, tableName ="joseembeddings" ,nDims = 400):
		cursor = self.db.cursor()
		dimList = []
		for i in range(1,nDims+1):
			dimList.append("dim"+str(i))

		dims = ",".join(dimList)
		strQuery = "SELECT "+dims+" FROM "+tableName + " WHERE word='"+word+"'"
		try:
			cursor.execute(strQuery)
		except:
			return np.zeros(400)
		vector = []

		if cursor.rowcount > 0:
			results = cursor.fetchone()
			for dim in results:
				vector.append(float(dim))
		else:
			vector = np.zeros(400)

		return vector

	def getMsgVector(self, msg, tableName ="joseembeddings" ,nDims = 400):
		cleanMsg = utils.clean_text(msg)
		vectors = []

		for token in cleanMsg:
			vector = self.getWordVector(token,tableName,nDims)
			vectors.append(vector)
		
		avgVector = np.mean(vectors,axis=0)
		return avgVector.tolist()


	def aggregateVectors(self, A, B):
		C = []
		C.append(A)
		C.append(B)
		C = np.mean(C,axis=0)
		return C.tolist()

	def getNormVector(self, vector):
		return np.linalg.norm(vector)

	def distance(self, A, B, distance = "cosine"):
		return cdist([A],[B],distance)

if __name__ == '__main__':
	
	iSQL = SQLEmbeddings()

	#Coran vs Coran	
	a = iSQL.getMsgVector("Decretamos en la Escritura respecto a los Hijos de Israel: Ciertamente, corromperéis en la tierra dos veces y os conduciréis con gran altivez.")
	b = iSQL.getMsgVector("Dimos a Moisés la Escritura e hicimos de ella dirección para los Hijos de Israel: «¡No toméis protector fuera de Mí")
	print iSQL.distance(a,b) 
	print iSQL.aggregateVectors(a,b)

	#Gasolina vs Coran
	a = iSQL.getMsgVector("Mamita yo sé que tú no te me va a quitar (duro) Lo que me gusta es que tú te dejas llevar (duro) Todos los weekends ella sale a vacilar (duro) Mi gata no para de janguear porque (yeah)")
	b = iSQL.getMsgVector("Dimos a Moisés la Escritura e hicimos de ella dirección para los Hijos de Israel: «¡No toméis protector fuera de Mí")
	print iSQL.distance(a,b)
	print iSQL.aggregateVectors(a,b)

	#Deportes vs Deportes
	a = iSQL.getMsgVector("Juventus y Manchester City han puesto sus ojos en el joven Daniel Arzani, internacional australiano de 19 años. Según The Sun, el joven delantero del Melbourne City les ha impresionado en el Mundial.")
	b = iSQL.getMsgVector("Mario Barco ha fichado por el Cádiz para las próximas tres temporadas. La temporada pasada militó en el Lugo, donde consiguió anotar cinco goles.")
	print iSQL.distance(a,b) 
	print iSQL.aggregateVectors(a,b)

	#Deportes vs Coran
	a = iSQL.getMsgVector("Juventus y Manchester City han puesto sus ojos en el joven Daniel Arzani, internacional australiano de 19 años. Según The Sun, el joven delantero del Melbourne City les ha impresionado en el Mundial.")
	b = iSQL.getMsgVector("Decretamos en la Escritura respecto a los Hijos de Israel: Ciertamente, corromperéis en la tierra dos veces y os conduciréis con gran altivez.")
	print iSQL.distance(a,b)
	print iSQL.aggregateVectors(a,b)