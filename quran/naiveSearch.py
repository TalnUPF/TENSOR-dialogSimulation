# -*- coding: utf-8 -*-

import os
import string
import sys

print "loading"

path = "/home/joan/Escritorio/quran/filePerVerse/"
sortedKeys = sorted(os.listdir(path))

dictSuras = {}
for fname in sortedKeys:
	cleanSura = open(path+fname,"r").read().lower()
	cleanSura = cleanSura.replace("“","")
	cleanSura = cleanSura.replace("”","")
	cleanSura = cleanSura.replace("—"," ")
	cleanSura = cleanSura.translate(None,string.punctuation)
	dictSuras[fname] = cleanSura

text = sys.argv[1]
text = text.translate(None, string.punctuation)
text = text.replace("“","")
text = text.replace("”","")
text = text.replace("—"," ")
text = text.replace("’"," ").lower()

for sura, content in dictSuras.iteritems():
	if text in content:
		print "found in "+sura
		print "====================="

	if content in text:
		print "found in "+sura
		print "====================="
