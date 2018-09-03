from __future__ import division
import re
from sqlEmbeddings import SQLEmbeddings
from sklearn.metrics import precision_recall_fscore_support as score

iSQL = SQLEmbeddings()

def load_seeds():
	pathBase = "./ubuntuWikiSeeds/"
	#pathBase = "./ubuntuChatSeeds/"
	
	seeds = {}

	for fname in os.listdir(pathBase):
		textSeed = open(pathBase+fname).read()
		seeds[fname] = iSQL.getMsgVector(textSeed, "google", 300, "en")

	return seeds

def loadTestData():
	conversation = []
	pathTestData = "./ubuntuTest/Unity_Testing.txt"
	rawLines = open(pathTestData,"r").read().strip().split("\n")
	
	for line in rawLines:
		if line[10] == "<":
			label = line[0]
			timestamp = re.findall(r'\[([0-9][0-9]:[0-9][0-9])\]',line)
			user = line.split(">")[0].split("<")[1]
			msg = line.split("> ")[1]
			dictLine = {"label":label,"user":user,"msg":msg,"timestamp":timestamp}
			conversation.append(dictLine)

	return conversation

def topicClustering(conversation, seeds):

	totalMsg = len(conversation)
	gold = []
	predictions = []

	for msgDict in conversation:
		msgVector = iSQL.getMsgVector(msgDict["msg"], "google", 300, "en")
		distances = {}
		for seedName, seedVector in seeds.iteritems():
			distance = iSQL.distance(msgVector,seedVector)
			distances[seedName] = distance

		if distances["ubuntu"] > distances["unity"]:
			predictedLabel = 1
		else:
			predictedLabel = 0

		gold.append(int(msgDict["label"]))
		predictions.append(predictedLabel)

		#print msgDict["msg"], distances, predictedLabel, msgDict["label"]

	precision, recall, fscore, support = score(gold, predictions)
	print 'precision: {}'.format(precision)
	print 'recall: {}'.format(recall)
	print 'fscore: {}'.format(fscore)

conversation = loadTestData()
seeds = loadSeeds()
topicClustering(conversation, seeds)