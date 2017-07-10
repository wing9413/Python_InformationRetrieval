import math
from collections import OrderedDict
from nltk.stem import PorterStemmer
import re

N = 3204 #number of document

def getResult(input):
	input = re.sub(r'[^\w]', ' ', input)
	input = input.lower()
	input = input.split(" ")
	for x in range(0,len(input)):
		if input[x] in query_list.keys():
			temp=input[x]
			if stemmer_on == "on":
				temp = stemmer.stem(temp)
			query_list[temp] += 1
		else:
			temp=input[x]
			if stemmer_on == "on":
				temp = stemmer.stem(temp)
			print(temp)
			query_list[temp] = 1

	print("\nQuery Frequency:")
	print(query_list)
	print("\n")

	###   Start to Calculate
	documentXquery = {}

	for term,f in query_list.items():
		if term in dictionary.keys():
			link = dictionary[term]
			line = postingFile.readline()
			while line:
				line = line.replace("\n","")
				line = line.split(",")
				heading = line[0].split()
				if link == heading[0]:
					idf = heading[1]
					w = f * float(idf)
					query_list[term] = w
					for x in range(1,len(line)):
						info = line[x].split()
						if info[0] in documentXquery.keys():
							documentXquery[info[0]] += round(float(info[1]) * w,3)
						else:
							documentXquery[info[0]] = round(float(info[1]) * w,3)
				line = postingFile.readline()
		else:
			query_list[term] = 0	
		postingFile.seek(0,0)		
	
	
	print(query_list)
	
	

	total = 0
	for k,w in query_list.items():
		total += w*w
	queryVector = round(math.sqrt(total),3)



	for id,w in documentXquery.items():
		base = documentVector[int(id)-1] * queryVector
		final = round(w/base,3)
	
	result = showResult(documentXquery,title,author)
	return result




def getTitle():
	temp = []
	file = open('title.txt')
	line = file.readline()
	line = file.readline()
	while line:
		line = line.split("#")
		temp.append(line[1].replace("\n",""))
		line = file.readline()

	file.close()
	return temp

def getAuthor():
	temp = {}
	file = open('author.txt')
	line = file.readline()
	line = file.readline()
	while line:
		line = line.split("#")
		temp[line[0]] = line[1]
		line = file.readline()

	file.close()
	return temp

def getStopWord():
	temp = []
	file = open('stopwords.txt')
	line = file.readline()

	while line:
		line = line.split()
		temp.append(line[0])
		line = file.readline()

	file.close()
	return temp
	
def getDocumentVector():
	temp = []
	documentVector_file = open('documentNormalize.txt')
	line = documentVector_file.readline()
	while line:
		line = line.split()
		temp.append(float(line[1]))
		line = documentVector_file.readline()
	documentVector_file.close()
	return temp
	
def getDictionary():
	temp = {}
	dictionaryFile = open('dictionary.txt')
	line = dictionaryFile.readline() 
	line = dictionaryFile.readline() 
	while line:
		line = line.split()
		temp[line[0]] = line[2]
		line = dictionaryFile.readline() 
	dictionaryFile.close()
	return temp

def showResult(documentXquery,title,author):
	count = len(documentXquery)
	
	documentXquery = OrderedDict(sorted(documentXquery.items(), key=lambda t: t[1]))	
	
	id = [0] * count
	simScore = [0] * count
	count -= 1
	for number, score in documentXquery.items():
		id[count]= number
		simScore[count] = score
		count -= 1
	
	
	for x in range(len(id)):
		if id[x] in author.keys():
			name = author[id[x]]
		else:
			name = ""
		number = int(id[x])
		print("%s. id:%s, Score:%s"%(x+1,id[x],simScore[x]))
		print("Title:%s\nAuthor:%s"%(title[number-1], name)  )
	
	return id
	
def getQuery():
	flag = ""
	temp = [""] * 64
	query_file = open('query.text')
	line = query_file.readline()
	while line:
		original_line = line
		if line.strip():
			line = line.split()
			if line[0] == ".I":
				id = int(line[1])
			elif line[0] == ".W":
				flag = ".W"
			elif line[0] == ".A" or line[0] == ".N":
				flag = ""
			else:
				if flag == ".W":
					original_line = original_line.replace("\n"," ")
					temp[id-1] += original_line
		
		line = query_file.readline()
	query_file.close()
	return temp
	
######       Main Program Start here         ##########

stopword_on = raw_input("stop word: on / off ")
stemmer_on = raw_input ("stemmer: on / off  ")
stemmer = PorterStemmer()

#get stopword when on
if stopword_on == "on":
	stopword = getStopWord()

#get document Vector
documentVector = getDocumentVector()

#get dictionary
dictionary = getDictionary()

#get Title
title = getTitle()

#get Author
author = getAuthor()

postingFile = open('postings_lists.txt')


while True:
	query_list = {}
	##When Enter query
	input = raw_input("please enter query\n")
	if input == "quit":
		break
	result = getResult(input)
	
	

###################       eval program start HERE        ###############
query = getQuery()
print(query[63])








############             eval program END HERE            ##########
postingFile.close()