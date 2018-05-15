import os
from lxml import etree
import codecs
from pprint import pprint
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

path = "./raw/15MAY.xml"
raw = open(path,"r")

tree = etree.parse(raw)
users = tree.xpath("/transcript/messages/message/from//text()")
msg = tree.xpath("/transcript/messages/message/body//text()")
dates = tree.xpath("/transcript/messages/message/date//text()")

VICTIM_NAME = "Azra"
RADICAL_NAME = "Jawad"

i = 0
victimMsgs = 0
radicalizatorMsgs = 0

charsPerWord = 0
charsPerWordRad = 0
charsPerWordVic = 0

wordsPerMsg = 0
wordsPerMsgRad = 0
wordsPerMsgVic = 0

tokensPerMsg = []
tokensPerMsgVictim = []
tokensPerMsgRadicalizator = []

dictMsgPerDay = {}
timePerDay = {}

content = []
lastHour = -1
lastDay = -1
print "\n==========================="
print "========= MESSAGES ========"
print "===========================\n"
while i< len(msg):
	username = users[i]
	text = msg[i]
	date = dates[i]
	day = date.split()[0]
	hour = date.split()[1]

	tokens = text.split()
	nTokens = len(tokens)
	tokensPerMsg.extend(tokens)
	
	if day not in timePerDay:
		timePerDay[day] = {}
		timePerDay[day]["start"] = hour
		print "\n==========================="
		print "  MESSAGES FROM "+day
		print "===========================\n"

		if lastHour != -1:
			timePerDay[lastDay]["end"] = lastHour

	if username == "azra":
		victimMsgs+=1
		wordsPerMsgVic+=nTokens
		wordsPerMsg+=nTokens
		tokensPerMsgVictim.extend(tokens)
		for token in tokens:
			chars = len(token)
			charsPerWord+= chars
			charsPerWordVic+= chars

		if day not in dictMsgPerDay:
			dictMsgPerDay[day] = {}
		if "victim" not in dictMsgPerDay[day]:
			dictMsgPerDay[day]["victim"] = []

		dictMsgPerDay[day]["victim"].append(tokens)

	elif username == "jawad":
		radicalizatorMsgs+=1
		wordsPerMsgRad+=nTokens
		wordsPerMsg+=nTokens
		tokensPerMsgRadicalizator.extend(tokens)
		for token in tokens:
			chars = len(token)
			charsPerWord+= chars
			charsPerWordRad+= chars

		if day not in dictMsgPerDay:
			dictMsgPerDay[day] = {}

		if "radicalizator" not in dictMsgPerDay[day]:
			dictMsgPerDay[day]["radicalizator"] = []
			
		dictMsgPerDay[day]["radicalizator"].append(tokens)

	print dates[i].replace(" CEST","").split()[1].split(".")[0]+" "+username+" : "+text.encode("utf-8")
	i+=1
	lastHour = hour
	lastDay = day
	if i == len(msg):
		timePerDay[day]["end"] = hour

######### 	VOCABULARY RICHNESS
generalRichness= len(set(tokensPerMsg))/float(len(tokensPerMsg))
victimRichness= len(set(tokensPerMsgVictim))/float(len(tokensPerMsgVictim))
radicalRichness= len(set(tokensPerMsgRadicalizator))/float(len(tokensPerMsgRadicalizator))


nMsgs = radicalizatorMsgs + victimMsgs
nWords = wordsPerMsgRad + wordsPerMsgVic

print "\n==========================="
print "====== GENERAL STATS ======"
print "===========================\n"

print "Total Number of messages " + str(nMsgs)
print "Total Number of words " + str(nWords)
print "Words per message " + str(wordsPerMsg/float(nMsgs))
print "Words per message Radicalizator " + str(wordsPerMsgRad/float(radicalizatorMsgs))
print "Words per message Victim " + str(wordsPerMsgVic/float(victimMsgs))
print "Number of Radicalizator Msgs " + str(radicalizatorMsgs)
print "Number of Victim Msgs " + str(victimMsgs)
print "Chars per word " + str(charsPerWord / float(nWords))
print "Chars per word Victim " + str(charsPerWordVic/float(wordsPerMsgVic))
print "Chars per word Radicalizator " + str(charsPerWordRad/float(wordsPerMsgRad))
print "General Richness " + str(generalRichness)
print "Radicalizator Richness " + str(radicalRichness)
print "Victim Richness " + str(victimRichness)

print "\n========================="
print "====== DAILY STATS ======"
print "========================="

sortedKeys = sorted(dictMsgPerDay)

for day in sortedKeys:
	roleDict = dictMsgPerDay[day]
	print "\nDay: "+day
	total = 0
	for role, messages in roleDict.iteritems():
		print role + " messages " + str(len(messages))
		total+=len(messages)

	print "Total Number of messages " + str(total)

	dictTime = timePerDay[day]
	
	fmt = '%H:%M:%S.%f'
	d1 = datetime.strptime(dictTime["start"], fmt)
	d2 = datetime.strptime(dictTime["end"], fmt)

	difference = (d2-d1)

	print difference
