from chatFeatures import ChatFeatures
from sqlEmbeddings import SQLEmbeddings
import utils
from pprint import pprint
from operator import itemgetter

class Topic:

	def __init__(self):
		self.iChat = ChatFeatures(None)
		self.iChat.process()
		self.iSQL = SQLEmbeddings()
		#self.conversationEvolution()
		
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

		#for distance in distances:
		#	print distance[0],"\t",distance[1],"\t",distance[2]

		return distances

	def relevantDayDetection(self, precomputed=True):
		if precomputed:
			lines = open("./stats/distances.tsv").read().split("\n")
			distances = []
			minDist = 100
			maxDist = 0
			for line in lines:
				date1, date2, dist = line.strip().split("\t")
				distFloat = float(dist)
				if distFloat < minDist:
					minDist = distFloat
				if distFloat > maxDist:
					maxDist = distFloat

				distances.append((date1, date2, distFloat))
		else:
			distances = self.conversationEvolution()

		rng = maxDist - minDist
		quartileInc = rng*1.0/4

		quartiles = {}
		quartiles["low"] = []
		quartiles["midlow"] = []
		quartiles["midhigh"] = []
		quartiles["high"] = []

		for date1, date2, distance in distances:
			if distance > minDist and distance <= minDist+quartileInc:
				quartiles["low"].append(date1)
				quartiles["low"].append(date2)
			elif distance > minDist+quartileInc and distance <= minDist+2*quartileInc:
				quartiles["midlow"].append(date1)
				quartiles["midlow"].append(date2)
			elif distance > minDist+2*quartileInc and distance <= minDist+3*quartileInc:
				quartiles["midhigh"].append(date1)
				quartiles["midhigh"].append(date2)
			elif distance > minDist+3*quartileInc and distance <= maxDist:
				quartiles["high"].append(date1)
				quartiles["high"].append(date2)

		relevantDates = {}

		for category, listDates in quartiles.iteritems():
			for date in listDates:
				if date not in relevantDates:
					relevantDates[date] = {}
					relevantDates[date]["low"] = 0
					relevantDates[date]["midlow"] = 0
					relevantDates[date]["midhigh"] = 0
					relevantDates[date]["high"] = 0

				relevantDates[date][category]+=1

		ranking = {}
		for date, categoryDict in relevantDates.iteritems():
			score = categoryDict["high"]+ 0.8 * categoryDict["midhigh"]+0.4*categoryDict["midlow"]+0.05*categoryDict["low"]
			ranking[date] = score

		pprint(relevantDates)
		lst = sorted(ranking.iteritems(), key=itemgetter(1),reverse=True)
		for t in lst: print '%s : %0.1f' % (t[0], t[1])


	'''
		1 - determinar bloques
		pillar primero bloque de N words. Despues ir mirando como varia el embedding medio y si no varia mucho, absorverlo

		2- con los bloques determinados, crear seeds de cada tema y hacer clustering.

	'''
	def topicAnalysis(self):
		MIN_TOKENS = 20

		#for date, listMsgs in self.conversation.iteritems():
		listMsgs = self.iChat.conversation["2018-05-15"]	

		lastVector = None
		acumTokens = 0
		acumText = []
		textBlocks = []

		for idx, dictMsg in enumerate(listMsgs):
			
			text = dictMsg["text"]
			cleanTokens = utils.clean_words(text.split())
			acumTokens+=len(cleanTokens)
			acumText.extend(cleanTokens)

			vector = self.iSQL.getMsgVector(text)

	
if __name__ == '__main__':
	
	iTopic = Topic()
	iTopic.relevantDayDetection()