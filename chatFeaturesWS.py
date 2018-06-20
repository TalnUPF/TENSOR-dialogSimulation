import os
from lxml import etree
import codecs
from pprint import pprint
from datetime import datetime
import time
import string
from nltk.tag.stanford import StanfordPOSTagger
from nltk.corpus import stopwords
from collections import Counter
import copy

class ChatFeatures:

	def __init__ (self, conversation):

		#ToDo: receive conversation via parameter and use the raw txt
		self.raw = "./raw/11JUN.xml"
		self.tree = etree.parse(self.raw)
		self.users = self.tree.xpath("/transcript/messages/message/from//text()")
		self.userSet = set(self.users)
		self.msg = self.tree.xpath("/transcript/messages/message/body//text()")
		self.dates = self.tree.xpath("/transcript/messages/message/date//text()")
		self.dictMsgPerDay = {}
		self.loadDicts()

	def loadDicts(self):
		pathBase = "./dicts/"
		self.victoria = codecs.open(pathBase+"victoria.txt","r", encoding="utf-8").read().strip().lower().split("\r\n")
		self.terrorismo = codecs.open(pathBase+"terrorismo.txt","r", encoding="utf-8").read().strip().split("\r\n")
		self.emocion = codecs.open(pathBase+"emocion.txt","r", encoding="utf-8").read().strip().lower().split("\r\n")
		self.consejo = codecs.open(pathBase+"consejo.txt","r", encoding="utf-8").read().strip().lower().split("\r\n")
		self.enemigo = codecs.open(pathBase+"enemigo.txt","r", encoding="utf-8").read().strip().lower().split("\r\n")
		self.religion = codecs.open(pathBase+"religion.txt","r", encoding="utf-8").read().strip().lower().split("\r\n")
		self.alabanza = codecs.open(pathBase+"alabanza.txt","r", encoding="utf-8").read().strip().lower().split("\r\n")
		self.domainWords = copy.copy(self.victoria)
		self.domainWords.extend(self.terrorismo)
		self.domainWords.extend(self.emocion)
		self.domainWords.extend(self.consejo)
		self.domainWords.extend(self.enemigo)
		self.domainWords.extend(self.religion)
		self.domainWords.extend(self.alabanza)

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
		self.tokensPerUser = {}

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
		if user not in self.tokensPerUser:
			self.tokensPerUser[user] = []

		self.tokensPerUser[user].append(tokens)


	def orthographic(self):
		import enchant
		d = enchant.Dict("es")
		lMistakes = []

		for date, listMsgs in self.conversation.iteritems():
			for dictMsg in listMsgs:
				text = dictMsg["text"]
				user = dictMsg["user"]
				date = dictMsg["date"]
				tokens = text.split()
				tokens = self.clean_words(tokens)
				for token in tokens:
					if token and not d.check(token):
						lMistakes.append((user,token, d.suggest(token)[0:3]))

		return lMistakes

	def process(self):
		i=0
		self.tokensPerMsg = []
		self.conversation = {}

		while i<len(self.msg):

			text = self.msg[i]
			date = self.dates[i]
			simpleDate = date.split()[0]

			user = self.users[i]
			if simpleDate not in self.conversation:
				self.conversation[simpleDate] = []

			self.conversation[simpleDate].append({"user":user,"date":date,"text":text})
			self.getTokens(text, date, user)
			
			i+=1

	def computeRolesPerDay(self):
		msgPerDayUser, turnsPerDayUser = self.turnsPerDay()
		relevantWordsPerDayUser = self.wordsPerDay()

		days = msgPerDayUser.keys()






	def turnsPerDay(self):
		self.turnsPerDayUser = {}
		self.msgPerDayUser = {}

		for date, listMsgs in self.conversation.iteritems():
			if date not in self.turnsPerDayUser:
				self.turnsPerDayUser[date] = {}

			if date not in self.msgPerDayUser:
				self.msgPerDayUser[date] = {}

			lastUser = None
			for dictMsg in listMsgs:
				user = dictMsg["user"]
				if user not in self.turnsPerDayUser[date]:
					self.turnsPerDayUser[date][user] = 0
				if user not in self.msgPerDayUser[date]:
					self.msgPerDayUser[date][user] = 0

				if user != lastUser:
					self.turnsPerDayUser[date][user]+=1

				self.msgPerDayUser[date][user]+=1
				lastUser = user

		return self.msgPerDayUser, self.turnsPerDayUser

	def domainWordsPerDay(self):
		domainWordsPerDay = {}

		for day, dictDay in self.dictMsgPerDay.iteritems():
			if day not in domainWordsPerDay:
				domainWordsPerDay[day] = {}

			for user, messagesUser in dictDay.iteritems():
				if user not in domainWordsPerDay[day]:
					domainWordsPerDay[day][user] ={}
					domainWordsPerDay[day][user]["victoria"] = 0
					domainWordsPerDay[day][user]["emocion"] = 0
					domainWordsPerDay[day][user]["terrorismo"] = 0
					domainWordsPerDay[day][user]["dominio"] = 0
					domainWordsPerDay[day][user]["religion"] = 0
					domainWordsPerDay[day][user]["alabanza"] = 0
					domainWordsPerDay[day][user]["consejo"] = 0
					domainWordsPerDay[day][user]["enemigo"] = 0

				for messageUser in messagesUser:
					for word in messageUser:
						word = word.lower()
						if word in self.domainWords:
							domainWordsPerDay[day][user]["dominio"]+=1
						if word in self.victoria:
							domainWordsPerDay[day][user]["victoria"]+=1
						if word in self.emocion:
							domainWordsPerDay[day][user]["emocion"]+=1
						if word in self.terrorismo:
							domainWordsPerDay[day][user]["terrorismo"]+=1
						if word in self.religion:
							domainWordsPerDay[day][user]["religion"]+=1
						if word in self.alabanza:
							domainWordsPerDay[day][user]["alabanza"]+=1
						if word in self.consejo:
							domainWordsPerDay[day][user]["consejo"]+=1
						if word in self.enemigo:
							domainWordsPerDay[day][user]["enemigo"]+=1
		
		sortedDays = sorted(domainWordsPerDay.keys())
		for day in sortedDays:
			print "--------"
			print day
			for user, dictCategory in domainWordsPerDay[day].iteritems():
				print user
				for category, count in dictCategory.iteritems():
					print "\t",category, count

		return domainWordsPerDay

	def wordsPerDay(self):
		stopwordList = stopwords.words('spanish')
		relevantWordsPerUser = {}

		for day, dictDay in self.dictMsgPerDay.iteritems():
			if day not in relevantWordsPerUser:
				relevantWordsPerUser[day] = {}

			for user, messagesUser in dictDay.iteritems():
				if user not in relevantWordsPerUser[day]:
					relevantWordsPerUser[day][user] = []			

				for messageUser in messagesUser:
					for word in messageUser:
						if word.lower() not in stopwordList:
							relevantWordsPerUser[day][user].append(word.lower())
					
				relevantWordsPerUser[day][user] = Counter(relevantWordsPerUser[day][user]).most_common(10)

		return relevantWordsPerUser

if __name__ == '__main__':
	iChat = ChatFeatures(None)
	iChat.process()
	iChat.computeRolesPerDay()
	iChat.domainWordsPerDay()
