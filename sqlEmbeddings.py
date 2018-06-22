import MySQLdb

class SQLEmbeddings:

	def __init__(self, dbname="Embeddings"):
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="pany8491", db=dbname, use_unicode=True) 


	def getWordVector(self, word, tableName ="joseembeddings" ,nDims = 400):
		cursor = self.db.cursor()
		dimList = []
		for i in range(1,nDims+1):
			dimList.append("dim"+str(i))

		dims = ",".join(dimList)
		strQuery = "SELECT "+dims+" FROM "+tableName + " WHERE word='"+word+"'"
		cursor.execute(strQuery)
		results = cursor.fetchone()
		vector = []
		for dim in results:
			vector.append(float(dim))

		return vector


if __name__ == '__main__':
	iSQL = SQLEmbeddings()
	print iSQL.getWordVector("hola")