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

class ChatFeatures:

	VICTIM = "azra"
	RADICALIZATOR ="jawad"

	def __init__ (self, path):
		self.raw = open(path,"r")
		self.tree = etree.parse(self.raw )
		self.users = self.tree.xpath("/transcript/messages/message/from//text()")
		self.msg = self.tree.xpath("/transcript/messages/message/body//text()")
		self.dates = self.tree.xpath("/transcript/messages/message/date//text()")
		self.dictMsgPerDay = {}


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
		if user == self.VICTIM:
			self.tokensPerMsgVictim.append(tokens)
		elif user == self.RADICALIZATOR:
			self.tokensPerMsgRadicalizator.append(tokens)

	def process(self):
		i=0
		self.tokensPerMsg = []
		self.tokensPerMsgVictim = []
		self.tokensPerMsgRadicalizator = []

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

	def wordsPerDay(self):
		s = StanfordPOSTagger('stanford/models/spanish.tagger', 'stanford/stanford-postagger.jar', encoding='utf8')
		stopwordList = stopwords.words('spanish')

		relevantWordsPerUser = {}

		for day, dictDay in self.dictMsgPerDay.iteritems():
			if day not in relevantWordsPerUser:
				relevantWordsPerUser[day] = {}

			for user, messagesUser in dictDay.iteritems():
				if user not in relevantWordsPerUser[day]:
					relevantWordsPerUser[day][user] = []

				for messageUser in messagesUser:
					'''
					for word in messageUser:
						if word not in stopwordList:
							relevantWordsPerUser[day][user].append(word)

					'''	
					tagged_words = s.tag(messageUser)

					for word,pos in tagged_words:
						if word not in stopwordList and pos.startswith("n"):
							relevantWordsPerUser[day][user].append(word)
					
				relevantWordsPerUser[day][user] = Counter(relevantWordsPerUser[day][user] )

		pprint(relevantWordsPerUser)

if __name__ == '__main__':
	path = "./raw/11JUN.xml"
	iChat = ChatFeatures(path)
	iChat.process()
	iChat.wordsPerDay()