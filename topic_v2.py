from chatFeatures import ChatFeatures
from sqlEmbeddings import SQLEmbeddings
import utils
from pprint import pprint
from operator import itemgetter
import os
from sortedcontainers import SortedList

class Topic:

	def __init__(self):

		self.seeds = None

		self.iChat = ChatFeatures(None)
		self.iChat.process()
		self.iSQL = SQLEmbeddings()
		
		
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
	def buildTextBlocks(self, filterPos=None, days_to_avoid=[]):
		MIN_TOKENS = 10
		THRESHOLD = 0.4

		textBlocksPerDay = {}
		blockVectorsPerDay = {}
		userBlocksPerDay = {}

		for date, listMsgs in self.iChat.conversation.iteritems():
			#print date
			if date in days_to_avoid:
				continue

			textBlocksPerDay[date] = []
			blockVectorsPerDay[date] = []

			listMsgs = self.iChat.conversation[date]	
			#print "Num msg",len(listMsgs)
			lastVector = None
			acumTokens = 0
			acumText = []
			acumTextToAppend = []
			acumUsers = []
			textBlocks = []
			userBlocks = []
			blockVector = None
			blockVectors = []
			for idx, dictMsg in enumerate(listMsgs):
				
				text = dictMsg["text"]
				user = dictMsg["user"]

				if not filterPos:
					cleanTokens = utils.clean_text(text)
				else:
					cleanTokens = utils.clean_text(text, True, filterPos)

				acumTokens+=len(cleanTokens)
				acumText.extend(cleanTokens)
				acumTextToAppend.append(cleanTokens)
				acumUsers.append(user)

				if acumTokens >= MIN_TOKENS:
					if not blockVector:
						vector = self.iSQL.getMsgVector(" ".join(acumText))
						blockVector = vector
					else:
						vector = self.iSQL.getMsgVector(text)
						if not vector:
							continue
						
						distance = self.iSQL.distance(vector, blockVector)
						if distance > THRESHOLD:
							textBlocks.append(acumTextToAppend)
							blockVectors.append(blockVector)
							userBlocks.append(acumUsers)
							blockVector = []
							acumText = []
							acumTextToAppend = []
							acumUsers = []
							acumTokens = 0
						else:
							blockVector = self.iSQL.aggregateVectors(blockVector,vector)



			blockVectorsPerDay[date] = blockVectors
			textBlocksPerDay[date] = textBlocks
			userBlocksPerDay[date] = userBlocks

		return blockVectorsPerDay, textBlocksPerDay, userBlocksPerDay


	def turnBasedBlocks(self, filterPos=None, days_to_avoid=[], store=False):
		blockVectorsPerDay = {}
		textBlocksPerDay = {}

		for date, listMsgs in self.iChat.conversation.iteritems():
			listMsgs = self.iChat.conversation[date]
			if date in days_to_avoid:
				continue

			textBlocksPerDay[date] = []
			blockVectorsPerDay[date] = []
			lastUser = None
			acumText = []
			textBlocks = []
			blockVectors = []

			for idx, dictMsg in enumerate(listMsgs):
				text = dictMsg["text"]
				user = dictMsg["user"]
				if not filterPos:
					cleanTokens = utils.clean_text(text)
				else:
					cleanTokens = utils.clean_text(text, True, filterPos)

				if not lastUser:
					acumText.extend(cleanTokens)
					lastUser = user
				else:
					if lastUser == user:
						acumText.extend(cleanTokens)
					else:
						vector = self.iSQL.getMsgVector(" ".join(acumText))
						textBlocks.append(acumText)
						blockVectors.append(vector)

						acumText = cleanTokens
						lastUser = user

			blockVectorsPerDay[date] = blockVectors
			textBlocksPerDay[date] = textBlocks

		if store:
			for date, textList in textBlocksPerDay.iteritems():
				strRepr = ""
				for turn in textList:
					strRepr+= " ".join(turn) + "\n\n"

				fd = open("./webResources/turns/"+date+"_turns","w")
				fd.write(strRepr)
				fd.close()

		return blockVectorsPerDay, textBlocksPerDay

	def load_seeds(self, dictSeeds):
		self.seeds = {}
		if not dictSeeds:
			pathBase = "./seeds/"
		else:
			pathBase = "./dictSeeds/"

		for fname in os.listdir(pathBase):
			textSeed = open(pathBase+fname).read()
			self.seeds[fname] = self.iSQL.getMsgVector(textSeed)

	def buildTopicHierarchy(self):
		self.seedHierarchy =[["conversation","emotions","religion","news","yijad","suspActivities"]]
		#self.seedHierarchy =[["emotions","religion","news","yijad","trips","suspActivities"]]
	
	def printResults(self,results):
		orderedDates = []
		for date, listMsgs in self.iChat.conversation.iteritems():
			orderedDates.append(date)

		orderedDates = sorted(orderedDates)
		i = 0

		updatedVectorBlocks = {}
		updatedTextBlocks = {}
		
		for date in orderedDates:
			key = date+"_"+str(i)
			while key in results.keys():
				dictDate = results[key]
				categories = "" 
				dists = dictDate["distances"]
				catList = []

				for cat in dists:
					#categories+=cat[1]+" : "+str(cat[0])+" "
					catList.append(cat[1])

				text = dictDate["text"]
				catList = catList[:2]
				catString = ",".join(catList)

				print text,"\t",catString,"\n"
				#print "\t".join(catList),"\n\n"

				i+=1
				key = date+"_"+str(i)

			i=0

	def storeResults(self, results):
		orderedDates = []
		for date, listMsgs in self.iChat.conversation.iteritems():
			orderedDates.append(date)

		orderedDates = sorted(orderedDates)
		i = 0
		
		for date in orderedDates:
			fd = open("./webResources/"+date+"_topics","w")

			key = date+"_"+str(i)
			while key in results.keys():
				dictDate = results[key]
				categories = "" 
				dists = dictDate["categories"]
				catList = []

				text = dictDate["text"]
				catString=""
				catString += dists[0][0][0]+","+dists[0][1][0]
				fd.write(text+"\t"+catString+"\n")
				i+=1
				key = date+"_"+str(i)

			fd.close()

			i=0

	def topicClustering(self, dictSeeds=False, filterPos=None, vectorBlocksPerDay=None, textBlocksPerDay=None, store=False):
		self.buildTopicHierarchy()
		self.load_seeds(dictSeeds)

		days_to_avoid = ["2018-05-15","2018-05-31"]
		if not vectorBlocksPerDay and not textBlocksPerDay:
			vectorBlocksPerDay, textBlocksPerDay, userBlocksPerDay = self.buildTextBlocks(filterPos,days_to_avoid)

		results = {}
		for date, listVec in vectorBlocksPerDay.iteritems():
			if date in days_to_avoid:
				continue

			for idx, vec in enumerate(listVec):
				if not vec:
					continue

				minDist = 1000000000
				minText = None
				selectedCategory = None
				i = 0
				idx = str(idx)
				selectedSubList = -1
				
				results[date+"_"+idx] = {}
				results[date+"_"+idx]["categories"] = []
				txtblock = textBlocksPerDay[date][int(idx)]

				strBlocks = ""
				for idxUser , block in enumerate(txtblock):
					strBlocks+= " ".join(block)+" [--["+userBlocksPerDay[date][int(idx)][idxUser]+"]--] "

				results[date+"_"+idx]["text"] = strBlocks
				results[date+"_"+idx]["distances"] = []

				while i < len(self.seedHierarchy):
					if selectedSubList == -1:
						categories = self.seedHierarchy[i]
					else:
						categories = self.seedHierarchy[i][selectedSubList]

					orderedCats = []
					for idxCat, category in enumerate(categories):
						seedVector = self.seeds[category]
						distance = self.iSQL.distance(vec,seedVector)
						orderedCats.append((category, distance[0]))
						if distance < minDist:							
							minDist = distance[0]
							selectedCategory = category
							selectedSubList = idxCat

					ordered = sorted(orderedCats,key=itemgetter(1))
					results[date+"_"+idx]["distances"].append(minDist)
					results[date+"_"+idx]["categories"].append(ordered)
					minDist = 1000
					minText = None
					selectedCategory = None

					i+=1

		if store:
			self.storeResults(results)

		return results


if __name__ == '__main__':
	
	iTopic = Topic()
	#iTopic.turnBasedBlocks(store=True)
	iTopic.topicClustering(store=True)
