# Information Retrieval

This assignment was done in a part of the Information Retrieval and Web Searc Course (CPS842).

Build a text retrieve system (simple search engine) through python. This search engine implements the Vector Space Model and searches through a CACM document collection (3204 documents in total)

### What is the goal?
**When query is entered by a user, the output will be a list of relevant documents with ranks (The most similar documents showed first)**

Input:

![alt text](https://github.com/wing9413/Python_InformationRetrieval/blob/master/Pictures/input.jpg)

Output: shows the document id, similarity score(bigger score, more similar), title and author

![alt text](https://github.com/wing9413/Python_InformationRetrieval/blob/master/Pictures/output.jpg)

---------------------------------------------------

## Getting Started

This assignment included two main programs:

1. invert.py (generate inverted index, dictionary and posting list) </br>
[Click Here to view my program for generate the inverted index](https://github.com/wing9413/Python_InformationRetrieval/blob/master/MyProject/invert.py)

2. search.py (get query from user input and displayed the result) </br>
[Click Here to view my program for building the search engine](https://github.com/wing9413/Python_InformationRetrieval/blob/master/MyProject/search.py)


### invert.py

Generate dictionary.txt, posting_list.txt, title.txt and author.txt

![alt text](https://github.com/wing9413/Python_InformationRetrieval/blob/master/Pictures/inverted_index.jpg)






