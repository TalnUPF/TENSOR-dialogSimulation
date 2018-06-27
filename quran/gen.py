# -*- coding: utf-8 -*-

import os
from pprint import pprint
import string

path = "/home/joan/Escritorio/quran/filePerVerse/"

dictSuras = {}
ordered = sorted(os.listdir(path))
for fname in ordered:
	pieces = fname.split("-")
	idSura = pieces[0]
	idVerse = pieces[1].replace(".txt","")
	if idSura not in dictSuras:
		dictSuras[idSura] = []

	text = open(path+fname,"r").read()
	text = text.translate(None, string.punctuation)
	text = text.replace("“","")
	text = text.replace("”","")
	text = text.replace("—"," ")
	text = text.replace("’"," ")
	dictSuras[idSura].append(text)

keys = sorted(dictSuras.keys())

for key in keys:
	out = open("/home/joan/Escritorio/quran/filePerSura/"+key,"w")
	out.write("\n".join(dictSuras[key]))
	out.close()
