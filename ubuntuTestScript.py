from __future__ import division
import re
from sqlEmbeddings import SQLEmbeddings
from sklearn.metrics import precision_recall_fscore_support as score
import os
from sklearn.metrics import fbeta_score

iSQL = SQLEmbeddings()

def loadSeeds(pathBase, embeddingsSelected):
	print "============================="
	print "selected seed is " + pathBase
	print "selected embeddings are "+embeddingsSelected
	seeds = {}

	for fname in os.listdir(pathBase):
		textSeed = open(pathBase+fname).read()
		seeds[fname] = iSQL.getMsgVector(textSeed, embeddingsSelected, 300, "en")

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

def topicClustering(conversation, seeds, embeddingsSelected):

	totalMsg = len(conversation)
	gold = []
	predictions = []

	for msgDict in conversation:
		msgVector = iSQL.getMsgVector(msgDict["msg"], embeddingsSelected, 300, "en")
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
	


	print "micro average"
	precision, recall, fscore, support = score(gold, predictions, average="micro")
	f2score = fbeta_score(gold, predictions, beta=2, average="micro")

	print 'precision: {}'.format(precision)
	print 'recall: {}'.format(recall)
	print 'fscore: {}'.format(fscore)
	print 'f2score: {}'.format(f2score)

	print "macro average"
	precision, recall, fscore, support = score(gold, predictions, average="macro")
	f2score = fbeta_score(gold, predictions, beta=2, average="macro")
	
	print 'precision: {}'.format(precision)
	print 'recall: {}'.format(recall)
	print 'fscore: {}'.format(fscore)
	print 'f2score: {}'.format(f2score)

	print "weighted"
	precision, recall, fscore, support = score(gold, predictions, average="weighted")
	f2score = fbeta_score(gold, predictions, beta=2, average="weighted")
	
	print 'precision: {}'.format(precision)
	print 'recall: {}'.format(recall)
	print 'fscore: {}'.format(fscore)
	print 'f2score: {}'.format(f2score)

conversation = loadTestData()

embeddingsSelected = "glove"

pathBase = "./ubuntuChatSeeds2/"
seeds = loadSeeds(pathBase, embeddingsSelected)
topicClustering(conversation, seeds, embeddingsSelected)

'''
pathBase = "./ubuntuWikiSeeds/"
seeds = loadSeeds(pathBase, embeddingsSelected)
topicClustering(conversation, seeds, embeddingsSelected)
'''
embeddingsSelected = "google"

pathBase = "./ubuntuChatSeeds2/"
seeds = loadSeeds(pathBase, embeddingsSelected)
topicClustering(conversation, seeds, embeddingsSelected)
'''
pathBase = "./ubuntuWikiSeeds/"
seeds = loadSeeds(pathBase, embeddingsSelected)
topicClustering(conversation, seeds, embeddingsSelected)
'''
embeddingsSelected = "wiki_en"

pathBase = "./ubuntuChatSeeds2/"
seeds = loadSeeds(pathBase, embeddingsSelected)
topicClustering(conversation, seeds, embeddingsSelected)
'''
pathBase = "./ubuntuWikiSeeds/"
seeds = loadSeeds(pathBase, embeddingsSelected)
topicClustering(conversation, seeds, embeddingsSelected)
'''
