import operator
from collections import OrderedDict
import nltk
from nltk.stem import PorterStemmer
import re
import math

class Node:
	def __init__(self,id):
		self.id = id
		self.termFreq = 1
		self.next = None

class Linked_list:
    def __init__(self):
    	self.head_node = None
    	self.cur_node = None

    def add_node(self,id):
        newNode = Node(id)
        if self.head_node == None:
        	self.head_node = newNode
        	self.cur_node = newNode
        else:
        	self.cur_node.next = newNode
        	self.cur_node = newNode
    	
    def cur_node_id(self):
    	return self.cur_node.id
        
    def print_list(self):
    	node = self.head_node
    	while node:
    		print ("id  " , node.id, node.termFreq)
    		node = node.next

class Value:
	documentFreq = 0
	totalFreq = 0
	postingList =None


stopword_on = raw_input("stop word: on / off :")
stemmer_on = raw_input ("stemmer: on / off  :")


stopword = []
if stopword_on == "on":
	file = open('stopwords.txt')
	line = file.readline()

	while line:
		line = line.split()
		stopword.append(line[0])
		line = file.readline()

	file.close()



title_file = open('title.txt','w+')
author_file = open('author.txt','w+')
line_number = 0 
dictionary = {}
file = open('cacm.all')
line = file.readline()
id = 0
unwanted_chars = "'#?%^&*+=[]?$@{}!.,/()\""   #remove the unwanted characters from a word
stemmer = PorterStemmer()


flag = ""

#while reading the entire file
while line:
	line_number += 1 
	original_line = line
	line = line.split()
	#get id document
	if line[0] == ".I":
		id = line[1]
		title_file .write("\n%s# "%id)
		print(id)
		
	elif line[0] == ".T":
		flag = ".T"
		
	elif line[0] == ".A":
		flag = ".A"
		author_file.write("\n%s# "%id)
		
	elif line[0] == ".B" or line[0] == ".W":
		flag = " "
	
	#ignore the content in .N and .C 
	elif line[0] == '.N' or line[0] == '.C' or line[0] == '.K':
		flag = " "
		file.readline()
	
	#ignore the content in .X	
	elif line[0] == '.X':
		line = file.readline() 
		while line:
			line = line.split()
			if line[0] == '.I':
				id = line[1]
				title_file .write("\n%s# "%id)
				break
			line = file.readline()
	
	#add term in the dictionary and the posting list		
	elif line[0] != '.T' and line[0] != '.B' and line[0] != '.A' and line[0] != '.W' and line[0] != '.K':
		if flag == ".T":
			title = original_line.replace('\n','')
			title_file .write("%s"%title)
		elif flag == ".A":
			author = original_line.replace('\n','')
			author_file.write("%s"%author)
		
		line = original_line
		line = re.sub(r'[^\w]', ' ', line)
		line = line.lower()
		line = line.split()
		for word in line:
			#remove the unwanted character
			
			#word = word.replace(" ", "")
			#word = word.replace(".", "")
			if stemmer_on == "on":
				word = stemmer.stem(word)
			
			
			if word not in stopword:
				#when new term occur
				if word not in dictionary.keys():
					#create a new object for value
					value = Value()
					value.documentFreq += 1
					value.totalFreq += 1
				
					#created a new linked list for a new term
					linked_list = Linked_list()
					linked_list.add_node(id)
					value.postingList = linked_list
					
					#store the new value that just created for the specific term
					dictionary[word] = value
					
					
			
				#while term is already occur in the dictionary	
				else:
					value = dictionary[word]
					value.totalFreq += 1
				
					#while current id is not as same as the previous id
					if id != value.postingList.cur_node_id():
						value.documentFreq += 1
						#add a new node
						value.postingList.add_node(id)
						dictionary[word] = value
					
					else:
						value.postingList.cur_node.termFreq += 1
						#just append a new position for the current document
						dictionary[word] = value
	
	line = file.readline()
	

file.close()
title_file.close()


N = 3204 #number of document

dictionary_file = open('dictionary.txt', 'w+')
postings_list_file = open('postings_lists.txt', 'w+')
documentVector_file = open('documentNormalize.txt', 'w+')
other = OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
count = 0
dVector = [0] * N



for k,v in other.items():
    #print (k, "  documentFreq:", v.documentFreq,"  totalFreq:",v.totalFreq)
	dictionary_file.write("%s  %s  %s\n" %(k,v.documentFreq,count))
	
	idf = math.log(N/v.documentFreq,10)
	idf = round(idf,2)	
   
	linkedList = v.postingList
	node = linkedList.head_node
	postings_list_file.write("%s %s "%(count, idf))
	while node:
		w = math.log(node.termFreq,10) + 1
		w = w * idf
		w = round(w,2)
		postings_list_file.write(",%s %s " %(node.id, w))
		
		w = w*w
		dVector[int(node.id)-1] += round(w,3)
		
		node = node.next
		
    
	postings_list_file.write("\n")
    
    
    
	count += 1
	

count = 1
for item in dVector:
	temp = math.sqrt(item)
	documentVector_file.write("%s  %s\n" %(count, temp))
	count += 1

dictionary_file.close()
postings_list_file.close()
documentVector_file.close()



