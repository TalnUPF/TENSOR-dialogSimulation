import string

def clean_words(tokens):
	cleanTokens = []
	for token in tokens:
		cleanToken = token
		for char in string.punctuation:
			cleanToken = cleanToken.replace(char, "")
		
		cleanTokens.append(cleanToken)
	
	return cleanTokens