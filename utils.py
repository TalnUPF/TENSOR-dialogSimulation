import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import string
from nltk.tag.stanford import StanfordPOSTagger
from nltk.corpus import stopwords
import spacy
from spacy.lang.es.examples import sentences

def clean_words(tokens, filterStopwords=False, filterPos=None):
	cleanTokens = []
	stopwordList = stopwords.words('spanish')
	
	if filterPos:
		tagger = StanfordPOSTagger('stanford/models/spanish.tagger', 'stanford/stanford-postagger.jar', encoding='utf8')

	for token in tokens:
		cleanToken = token
		for char in string.punctuation:
			cleanToken = cleanToken.replace(char, "")
		
		if filterPos and not filterStopwords:
			res = tagger.tag([cleanToken])
			if len(res)>0:
				word, pos = res[0]
				if pos[0] in filterPos:
					cleanTokens.append(cleanToken)
		
		elif filterStopwords and not filterPos:
			if cleanToken not in stopwordList:
				cleanTokens.append(cleanToken)
		
		elif filterStopwords and filterPos:
			res = tagger.tag([cleanToken])
			if len(res)>0:
				word, pos = res[0]
				if cleanToken not in stopwordList and pos[0] in filterPos:
					cleanTokens.append(cleanToken)

		elif not filterStopwords and not filterPos:
			cleanTokens.append(cleanToken)
	
	return cleanTokens

def clean_text(text, filterStopwords=False, filterPos=None):

	nlp = spacy.load('es_core_news_sm')
	cleanTokens = []
	stopwordList = stopwords.words('spanish')
	doc = nlp(text.decode("utf8"))

	for token in doc:
		if filterPos and not filterStopwords:
			if token.pos_ in filterPos:
				cleanTokens.append(token.text)
		
		elif filterStopwords and not filterPos:
			if token.text not in stopwordList:
				cleanTokens.append(token.text)
		
		elif filterStopwords and filterPos:
			if token.text not in stopwordList and token.pos_ in filterPos:
				cleanTokens.append(token.text)

		elif not filterStopwords and not filterPos:
			cleanTokens.append(token.text)
	
	return cleanTokens

def clean_get_lemmas(text):
	nlp = spacy.load('es_core_news_sm')
	cleanTokens = []
	doc = nlp(text.decode("utf8"))

	for token in doc:
		cleanTokens.append(token.lemma_)

	return cleanTokens