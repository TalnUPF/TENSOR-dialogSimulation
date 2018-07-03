from chatFeatures import ChatFeatures
from sqlEmbeddings import SQLEmbeddings
import utils
from pprint import pprint
from operator import itemgetter
import os


class Topic:

	def __init__(self):

		self.seeds = None

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

			cleanText = " ".join(utils.clean_text(acumText, True, ["NOUN","VERB","ADJ"]))

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


	def conversationEvolutionPerUser(self):
		distancesPerUser = {}
		for user in self.iChat.userSet:
			vectorPerDay = {}

			for date, listMsgs in self.iChat.conversation.iteritems():
				listMsgs = self.iChat.conversation[date]
				acumText = ""
				for dictMsg in listMsgs:
					if dictMsg["user"] == user:
						acumText += " "+dictMsg["text"]

				cleanText = " ".join(utils.clean_text(acumText, True, ["NOUN","VERB","ADJ"]))

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

			distancesPerUser[user] = distances
			#for distance in distances:
			#	print distance[0],"\t",distance[1],"\t",distance[2]

		for user in self.iChat.userSet:
			distances = distancesPerUser[user]
			print user
			for distance in distances:
				print distance[0],"\t",distance[1],"\t",distance[2]

		return distances

	def relevantDayDetection(self, path="./stats/distances.tsv"):
		if path:
			lines = open(path).read().split("\n")
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

		#pprint(relevantDates)
		#lst = sorted(ranking.iteritems(), key=itemgetter(1),reverse=True)
		#for t in lst: print '%s : %0.1f' % (t[0], t[1])

		return ranking

	'''
		1 - determinar bloques
		pillar primero bloque de N words. Despues ir mirando como varia el embedding medio y si no varia mucho, absorverlo

		2- con los bloques determinados, crear seeds de cada tema y hacer clustering.

	'''
	def buildTextBlocks(self):
		MIN_TOKENS = 20
		THRESHOLD = 0.5

		textBlocksPerDay = {}
		blockVectorsPerDay = {}

		for date, listMsgs in self.iChat.conversation.iteritems():
			#print date
			
			textBlocksPerDay[date] = []
			blockVectorsPerDay[date] = []

			listMsgs = self.iChat.conversation[date]	
			#print "Num msg",len(listMsgs)
			lastVector = None
			acumTokens = 0
			acumText = []
			textBlocks = []
			blockVector = None
			blockVectors = []
			for idx, dictMsg in enumerate(listMsgs):
				
				text = dictMsg["text"]
				cleanTokens = utils.clean_text(text)
				acumTokens+=len(cleanTokens)
				acumText.extend(cleanTokens)

				if acumTokens >= MIN_TOKENS:
					if not blockVector:
						vector = self.iSQL.getMsgVector(" ".join(acumText))
						blockVector = vector
					else:
						vector = self.iSQL.getMsgVector(text)
						if not vector:
							continue
						
						distance = self.iSQL.distance(vector, blockVector)
						#print distance
						if distance > THRESHOLD:
							textBlocks.append(acumText)
							blockVectors.append(blockVector)
							blockVector = vector
							#print acumText
							acumText = cleanTokens
							acumTokens = len(cleanTokens)
						else:
							#print "aggregating"
							blockVector = self.iSQL.aggregateVectors(blockVector,vector)

			blockVectorsPerDay[date] = blockVectors
			textBlocksPerDay[date] = textBlocks
			#print len(textBlocks)

		return blockVectorsPerDay, textBlocksPerDay


	def load_seeds(self):
		self.seeds = {}
		pathBase = "./seeds/"
		for fname in os.listdir(pathBase):
			textSeed = open(pathBase+fname).read()
			self.seeds[fname] = self.iSQL.getMsgVector(textSeed)

	def buildTopicHierarchy(self):
		self.seedHierarchy =[["Form","Content"], [["Question","Short_Turn","Long_Turn"],["Religion","News","Yihad"]]]
		

	def topicClustering(self):
		self.buildTopicHierarchy()
		print "loading seeds"
		self.load_seeds()
		print "loaded, building blocks"
		vectorBlocksPerDay, textBlocksPerDay = self.buildTextBlocks()
		print "blocks built"

		results = {}
		print "clustering"
		for date, listVec in vectorBlocksPerDay.iteritems():
			for idx, vec in enumerate(listVec):
				minDist = 1000
				minText = None
				selectedCategory = None
				i = 0
				idx = str(idx)
				selectedSubList = -1
				
				results[date+"_"+idx] = {}
				results[date+"_"+idx]["categories"] = []
				results[date+"_"+idx]["text"] = " ".join(textBlocksPerDay[date][int(idx)])
				results[date+"_"+idx]["distances"] = []

				while i < len(self.seedHierarchy):
					if selectedSubList == -1:
						categories = self.seedHierarchy[i]
					else:
						categories = self.seedHierarchy[i][selectedSubList]

					for idxCat, category in enumerate(categories):
						print category
						seedVector = self.seeds[category]
						distance = self.iSQL.distance(vec,seedVector)
						if distance < minDist:
							minDist = distance[0]
							selectedCategory = category
							selectedSubList = idxCat

					results[date+"_"+idx]["distances"].append(minDist)
					results[date+"_"+idx]["categories"].append(selectedCategory)
					minDist = 1000
					minText = None
					selectedCategory = None

					i+=1

		return results

if __name__ == '__main__':
	
	iTopic = Topic()
	#iTopic.relevantDayDetection("./stats/distancesJawad.tsv")
	#iTopic.relevantDayDetection("./stats/distancesAzra.tsv")
	pprint(iTopic.topicClustering())