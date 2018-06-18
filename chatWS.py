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
from flask import Flask, app, request, url_for, Response
from logging.handlers import RotatingFileHandler
from logging import Formatter, INFO
import json
import os
from flask_jsonpify import jsonpify
from chatFeaturesWS import ChatFeatures

app = Flask(__name__)

iChat = None

@app.route('/computeChatInfo', methods=['GET'])
def computeChatInfo():
	conversation = request.args.get('conversation')

	iChat = ChatFeatures(conversation)
	iChat.process()

	data = jsonpify(tokenDict)
	return data

@app.route('/getWordsPerDay', methods=['GET'])
def getWordsPerDay():
	conversation = request.args.get('conversation')
	iChat = ChatFeatures(conversation)
	iChat.process()

	wpd = iChat.wordsPerDay()
	data = jsonpify(wpd)
	return data

@app.route('/getTurnsPerDay', methods=['GET'])
def turnsPerDayUser():
	conversation = request.args.get('conversation')

	iChat = ChatFeatures(conversation)
	iChat.process()
	tpd = iChat.turnsPerDay()
	data = jsonpify(tpd)
	return data

@app.route('/orthographic',methods=["GET"])
def orthographic():
	conversation = request.args.get('conversation')
	iChat = ChatFeatures(conversation)
	iChat.process()
	ort = iChat.orthographic()
	data = jsonpify(ort)
	return data

if __name__ == '__main__':

    app.debug = True
    app.config['PROPAGATE_EXCEPTIONS'] = True

    LOG_FILEPATH = "log.txt"

    formatter = Formatter("[%(asctime)s]\t%(message)s")
    handler = RotatingFileHandler(LOG_FILEPATH, maxBytes=10000000, backupCount=1)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000, debug=True)