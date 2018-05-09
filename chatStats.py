import os
from lxml import etree
import codecs
from pprint import pprint

path = "./raw/principal@conference.tensor-xat.tensor.xml"
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

content = []
while i< len(msg):
	username = users[i]
	text = msg[i]
	tokens = text.split()
	nTokens = len(tokens)

	#small hack
	if username == "null":
		username = VICTIM_NAME
		victimMsgs+=1
		wordsPerMsgVic+=nTokens
		wordsPerMsg+=nTokens
		for token in tokens:
			chars = len(token)
			charsPerWord+= chars
			charsPerWordVic+= chars

	elif username == "principal@conference.tensor-xat.tensor/jawad":
		username = RADICAL_NAME
		radicalizatorMsgs+=1
		wordsPerMsgRad+=nTokens
		wordsPerMsg+=nTokens
		for token in tokens:
			chars = len(token)
			charsPerWord+= chars
			charsPerWordRad+= chars

	else:
		username = "OTHER"

	content.append((dates[i],username,text))
	print dates[i]+" "+username+" : "+text
	i+=1

#pprint(content)

nMsgs = radicalizatorMsgs + victimMsgs
nWords = wordsPerMsgRad + wordsPerMsgVic
print "Number of messages " + str(nMsgs)
print "Number of words " + str(nWords)
print "Words per message " + str(wordsPerMsg/float(nMsgs))
print "Words per message Radicalizator " + str(wordsPerMsgRad/float(radicalizatorMsgs))
print "Words per message Victim " + str(wordsPerMsgVic/float(victimMsgs))
print "Number of Radicalizator Msgs " + str(radicalizatorMsgs)
print "Number of Victim Msgs " + str(victimMsgs)
print "Chars per word " + str(charsPerWord / float(nWords))
print "Chars per word Victim " + str(charsPerWordVic/float(wordsPerMsgVic))
print "Chars per word Radicalizator " + str(charsPerWordRad/float(wordsPerMsgRad))