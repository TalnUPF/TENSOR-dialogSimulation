import string
from nltk.tag.stanford import StanfordPOSTagger
from nltk.corpus import stopwords

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