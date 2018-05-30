import os
from lxml import etree
import codecs
from pprint import pprint
from datetime import datetime
import time
import string

class ChatFeatures:

	VICTIM_NAME = "Azra"
	RADICAL_NAME = "Jawad"
	THRESHOLD = 240.0

	def __init__ (self, path):
		self.raw = open(path,"r")
		self.tree = etree.parse(self.raw )
		self.users = self.tree.xpath("/transcript/messages/message/from//text()")
		self.msg = self.tree.xpath("/transcript/messages/message/body//text()")
		self.dates = self.tree.xpath("/transcript/messages/message/date//text()")
		self.dictMsgPerDay = {}

	def preprocess(self):
		i = 0
		lastHour = -1
		countMsg = 0
		lastDay = -1

		while i<len(self.msg):
			date = self.dates[i].replace(" CEST", "")
			microseconds = date.split(".")[1]
			rest = date.split(".")[0]
			firstOfDay = None
			day = date.split()[0].split("-")[2]

			if day != lastDay:
				countMsg = 1
			else:
				countMsg +=1

			if len(microseconds) < 3:
				n = len(microseconds)
				while n<3:
					microseconds = "0"+microseconds
					n+=1
				date = rest+"."+microseconds
				self.dates[i] = date

			message = self.msg[i]
			username = self.users[i]
			
			if username != "null" and not username.endswith("jawad"):
				self.dates.pop(i)
				self.msg.pop(i)
				self.users.pop(i)
				if i!=0:
					i-=1
	
			elif username.endswith("jawad"):
				if lastHour != -1:
					fmt = '%Y-%m-%d %H:%M:%S.%f'
					d1 = datetime.strptime(date, fmt)
					d2 = datetime.strptime(lastHour, fmt)

					difference = (d1-d2).total_seconds()*1000

					if difference < self.THRESHOLD:
						self.dates.pop(i)
						self.msg.pop(i)
						self.users.pop(i)

						if countMsg == 2:
							self.dates.pop(i-1)
							self.msg.pop(i-1)
							self.users.pop(i-1)
							if i!=0:
								i-=1

						if i!=0:
							i-=1

			lastDay = day
			lastHour = date
			i+=1
		


	def clean_words(self, tokens):
		cleanTokens = []
		for token in tokens:
			cleanToken = token
			for char in string.punctuation:
				cleanToken = cleanToken.replace(char, "")
			
			cleanTokens.append(cleanToken)
		
		return cleanTokens

	#### Computes and stores the tokens
	def getTokens(self, text, date, user):
		
		tokens = text.split()
		tokens = self.clean_words(tokens)
		date = date.split()[0]

		#### Tokens per day specific
		if date not in self.dictMsgPerDay:
			self.dictMsgPerDay[date] = {}
			if user not in self.dictMsgPerDay[date]:
				self.dictMsgPerDay[date][user] = []
			self.dictMsgPerDay[date][user].append(tokens)
		else:
			if user not in self.dictMsgPerDay[date]:
				self.dictMsgPerDay[date][user] = []
			self.dictMsgPerDay[date][user].append(tokens)

		#### Tokens Per msg general and specific
		self.tokensPerMsg.append(tokens)
		if user == "victim":
			self.tokensPerMsgVictim.append(tokens)
		elif user == "radicalizator":
			self.tokensPerMsgRadicalizator.append(tokens)

	def process(self):
		i=0
		self.tokensPerMsg = []
		self.tokensPerMsgVictim = []
		self.tokensPerMsgRadicalizator = []

		while i<len(self.msg):
			deleted = False
			if self.users[i] == "null":
				self.users[i] = "victim"
			elif self.users[i].endswith("jawad"):
				self.users[i] = "radicalizator"
			else:
				deleted = True

			if not deleted:
				text = self.msg[i]
				date = self.dates[i]
				user = self.users[i]
				self.getTokens(text, date, user)
			
			i+=1

		pprint(self.dictMsgPerDay)

'''
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
		if lastHour != -1:
			timePerDay[lastDay]["end"] = lastHour

	#small hack
	if username == "null":
		username = VICTIM_NAME
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

	elif username == "principal@conference.tensor-xat.tensor/jawad":
		username = RADICAL_NAME
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

	else:
		username = "OTHER"

	content.append((dates[i],username,text))
	print dates[i]+" "+username+" : "+text
	i+=1
	lastHour = hour
	lastDay = day
	if i == len(msg):
		timePerDay[day]["end"] = hour

######### 	VOCABULARY RICHNESS
generalRichness= len(set(tokensPerMsg))/float(len(tokensPerMsg))
victimRichness= len(set(tokensPerMsgVictim))/float(len(tokensPerMsgVictim))
radicalRichness= len(set(tokensPerMsgRadicalizator))/float(len(tokensPerMsgRadicalizator))

#pprint(content)

nMsgs = radicalizatorMsgs + victimMsgs
nWords = wordsPerMsgRad + wordsPerMsgVic

print "\n========================="
print "====== GENERAL STATS ======"
print "==========================="

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
	print "\n\n##############"
	print "Day: "+day
	total = 0
	for role, messages in roleDict.iteritems():
		print role + " messages " + str(len(messages))
		total+=len(messages)

	print "Total Number of messages " + str(total)


print timePerDay

'''
if __name__ == '__main__':
	path = "./raw/principal@conference.tensor-xat.tensor.xml"
	iChat = ChatFeatures(path)
	iChat.preprocess()
	iChat.process()