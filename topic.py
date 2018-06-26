from chatFeatures import ChatFeatures
from sqlEmbeddings import SQLEmbeddings
import utils

class Topic:

	def __init__(self):
		self.iChat = ChatFeatures(None)
		self.iChat.process()
		self.iSQL = SQLEmbeddings()
		self.conversationEvolution()
		
	def conversationEvolution(self):
		vectorPerDay = {}

		for date, listMsgs in self.iChat.conversation.iteritems():
			listMsgs = self.iChat.conversation[date]
			acumText = ""
			for dictMsg in listMsgs:
				acumText += " "+dictMsg["text"]

			cleanText = " ".join(utils.clean_words(acumText.split(), True, ["n","v","a"]))

			vector = self.iSQL.getMsgVector(cleanText)
			vectorPerDay[date] = vector

		distances = []

		inserted = set()
		for date1, vector1 in vectorPerDay.iteritems():
			for date2, vector2 in vectorPerDay.iteritems():
				if date1!=date2 and (date2,date1) not in inserted:
					dist = str(self.iSQL.distance(vector1, vector2)[0][0]).replace(".",",")
					inserted.add((date1,date2))
					distances.append((date1,date2,dist))

		for distance in distances:
			print distance[0],"\t",distance[1],"\t",distance[2]


		return distances


	def topicAnalysis(self):
		#for date, listMsgs in self.conversation.iteritems():
		listMsgs = self.iChat.conversation["2018-05-15"]	

		lastVector = None
		for idx, dictMsg in enumerate(listMsgs):
			text = dictMsg["text"]
			vector = self.iSQL.getMsgVector(text)
			if lastVector and vector:
				print idx
				print self.iSQL.distance(vector,lastVector)
				lastVector = vector
			elif not lastVector and vector:
				lastVector = vector
	
if __name__ == '__main__':
	
	iTopic = Topic()
