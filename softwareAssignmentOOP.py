
'''
Introduction to Python Programming (aka Programmierkurs I, aka Python I)
Software Assignment
'''

import sys
import xml.etree.ElementTree as ET
import string
from collections import defaultdict
from stemming.stemming.porter2 import stem
import math
import pprint
import numpy as np
from numpy.linalg import norm

class SearchEngine:
    def __init__(self, collectionName, create):
        '''
        Initialize the search engine, i.e. create or read in index. If
        create=True, the search index should be created and written to
        files. If create=False, the search index should be read from
        the files. The collectionName points to the filename of the
        document collection (without the .xml at the end). Hence, you
        can read the documents from <collectionName>.xml, and should
        write / read the idf index to / from <collectionName>.idf, and
        the tf index to / from <collectionName>.tf respectively. All
        of these files must reside in the same folder as THIS file. If
        your program does not adhere to this "interface
        specification", we will subtract some points as it will be
        impossible for us to test your program automatically!
        '''
        self.collectionName=collectionName
        self.a=0 #idf
        self.b=0 #tf
        if create==True:
            print("Creating index...")

            #xml file to python dictionary
            tree = ET.parse(collectionName+'.xml')
            root = tree.getroot()

            self.dic={}
            for doc in root.findall('.//DOC'):
                self.dic[doc.attrib['id']] = []
                try:
                    headline = doc.find('HEADLINE').text
                except AttributeError:
                    continue
                self.dic[doc.attrib['id']].extend(headline.lower().split())  # nicht append, weil append die Wörter jedes Paragraphen als extra Liste in der Liste anhängt
                txt = doc.find('TEXT').text
                # print(txt)
                self.dic[doc.attrib['id']].extend(txt.lower().split())
                try:  # unnötig?
                    doc.find('P')
                except AttributeError:
                    continue
                for p in doc.findall('.//P'):
                    self.dic[doc.attrib['id']].extend(p.text.lower().split())

            # delete punctuation
            p = {i: "" for i in string.punctuation}  # dictionary: translation for any i is the empty string
            for key, value in self.dic.items():
                table = str.maketrans(p)  # returns the translation table
                for i in range(len(value)):
                    value[i] = value[i].translate(table)
            # stem
            for doc in self.dic.keys():
                self.dic[doc] = list(filter(lambda w: w != '', self.dic[doc]))  # delete words that are the empty string from list
                self.dic[doc] = [stem(word) for word in self.dic[doc]]  # List Comprehension to stem every word

            # (6) compute idf, write idf into file
            self.setofwords = set()
            for doc in self.dic.keys():
                for word in self.dic[doc]:
                    self.setofwords.add(word)
            self.listofwords = list(self.setofwords)
            self.listofwords.sort()  # alphabetisch ordnen: liste nach anfangsbuchstabe sortieren

            with open(self.collectionName + '.idf', 'w+') as self.idffile:
                for word in self.listofwords:
                    self.idffile.write(str(word) + '\t' + str(self.idf(word)) + '\n')

            # (7) compute tf, write tf into file
            with open(self.collectionName + '.tf', 'w+') as self.tffile:
                for doc in self.dic:
                    self.setofw = set()
                    for word in self.dic[doc]:
                        self.setofw.add(word)
                    self.listofw = list(self.setofw)
                    self.listofw.sort()
                    for word in self.listofw:
                        self.tffile.write(str(doc) + '\t' + str(word) + '\t' + str(self.tf(word, doc)) + '\n')

        # dict for maxOccurrence// or function?

        def maximumocc(doc):
            'maximum occurrences of any term in doc'
            self.numdoc = {}
            for word in set(self.dic[doc]):
                # count each word
                self.numdoc[word] = 0
                for i in self.dic[doc]:
                    if word == i:
                        self.numdoc[word] += 1
            m = max(self.numdoc.values(), key=lambda x: x, default=0)  # max by value
            return m

        self.maxocc = {}
        for doc in self.dic.keys():
            self.maxocc[doc] = maximumocc(doc)

        pprint.pprint(self.maxocc) # ACHTUNG: maxocc values manchmal 0, obwohl
        print(maximumocc('NYT_ENG_19950101.0048')) # works; 30



        if create == False:
            print("Reading index from file...")


        # weight vector (tf.idf for each word in doc) for each doc (matrix)

        self.globalset=set()
        for doc in self.dic:
            for word in self.dic[doc]:
                self.globalset.add(word)
        self.globallist=list(self.globalset)

        #Liste mit doc ids
        self.doclist=list(self.dic.keys())

        #Matrix mit horizontalen Doc-Vektoren, vertikalem Vokabular
        self.D=np.zeros((self.numdocs, len(self.globallist)))
        print(self.globallist[0])
        print(self.doclist[0])
        print(self.tfidf(self.globallist[0], self.doclist[0]))
        print(self.tfidf('champion', 'NYT_ENG_19950101.0001'))  # funktioniert :)

        # das hier dauert sehr lange
        #tfidf score in die arrays schreiben: horizontal die docs, vertikal das Vokabular self.globallist
        for i in range(len(self.doclist)):
            for j in range(len(self.globallist)):
                if self.globallist[j] in self.dic[self.doclist[i]]:
                    self.D[i][j] = self.tfidf(self.globallist[j], self.doclist[i])
        print(self.D)
        print("Done.")


    def idf(self, term):
        'log(number of all documents/number of documents that contain term)'
        self.numdocs = 0 #instance attribute defined outside __init__
        self.numdocsterm = 0
        for doc in self.dic.keys():
            self.numdocs += 1
            if term in self.dic[doc]:
                self.numdocsterm += 1
        return math.log(self.numdocs / self.numdocsterm)



    def tf(self, term, doc):
        'number of times term occurs in doc/maximum occurrences of any term in doc'

        self.numofterm = 0
        for word in self.dic[doc]:
            if word == term:
                self.numofterm += 1
        return self.numofterm / 100 #self.maxocc[doc] #oder maxocc[doc] als dict, sodass maxocc[doc]=maximumocc(doc) -> dict schneller


    def tfidf(self, term, doc):
        # look up idf(term)
        idffile=open(self.collectionName + '.idf', 'r')
        for line in idffile.readlines():
            if line.split("\t")[0] == term:
                self.a+=float(line.split("\t")[1])
        # look up tf(term, doc)
        tffile=open(self.collectionName + '.tf', 'r')
        for line in tffile.readlines():
            if line.split("\t")[0] == doc:
                if line.split("\t")[1] == term:
                    self.b+= float(line.split("\t")[2]) #instance attribute defined outside __init__
        return self.a * self.b


    @staticmethod
    def sim(a, b):
        if norm(a)*norm(b)!=0:
            return np.dot(a, b) / (norm(a) * norm(b))
            #? oder Fehler ?

    def executeQuery(self, queryTerms):
        '''
        Input to this function: List of query terms

        Returns the 10 highest ranked documents together with their
        tf.idf-sum scores, sorted score. For instance,

        [('NYT_ENG_19950101.0001', 0.07237004260325626),
         ('NYT_ENG_19950101.0022', 0.013039249597972629), ...]

        May be less than 10 documents if there aren't as many documents
        that contain the terms.
        '''
        self.queryTerms=[stem(word) for word in queryTerms] #stem, List Comprehension
        query=np.zeros(len(self.globallist)) #horizontaler Vektor der Länge des Vokabulars
        self.queryset=set() #instance attribute defined outside __init__
        for word in queryTerms:
            #word=stem(word)
            self.queryset.add(word)
        for word in self.queryset:
            for i in range(len(self.globallist)):
                if self.globallist[i]==word:
                    query[i]=self.tfidf(word, queryTerms) #tfidf Funktion muss Klassenfunktion sein


        self.finaldict={} #instance attribute defined outside __init__
        for i in range(len(self.doclist)):
            self.finaldict[self.doclist[i]]=self.sim(self.D[i], query)

        #pprint.pprint(self.finaldict)

        self.lst=list(self.finaldict.items()) #instance attribute defined outside __init__
        self.lst.sort(key= lambda x:x[1])

        res="I found the following documents:\n"
        for i in range(10):
            if self.lst[i][1]!=0:
                res+=self.lst[i][0]+" ("+str(self.lst[i][1])+"\n"
        return res



        
    def executeQueryConsole(self):
        '''
        When calling this, the interactive console should be started,
        ask for queries and display the search results, until the user
        simply hits enter.
        '''
        print("Please enter query, terms separated by whitespace: ")

        #loop asking for query terms ?

        self.queryTerms=input().split(" ")
        self.queryTerms=[stem(word) for word in self.queryTerms] #stem
        query = np.zeros(len(self.globallist))  # horizontaler Vektor der Länge des Vokabulars
        self.queryset = set()
        for word in self.queryTerms:
            #word = stem(word)
            self.queryset.add(word)
        for word in self.queryset:
            for i in range(len(self.globallist)):
                if self.globallist[i] == word:
                    query[i] = self.tfidf(word, self.queryTerms)

        self.finaldict = {} # instance attribute defined outside __init__
        for i in range(len(self.globallist)):
            self.finaldict[self.doclist[i]] = self.sim(self.D[i], query)

        self.lst = list(self.finaldict.items())
        self.lst.sort(key=lambda x: x[1])

        res = "I found the following documents:\n"  # display function ?
        for i in range(10):
            res += self.lst[i][0] + " (" + str(self.lst[i][1]) + ") \n"
        return res

    
if __name__ == '__main__':
    '''
    write your code here:
    * load index / start search engine
    * start the loop asking for query terms
    * program should quit if users enters no term and simply hits enter
    '''
    print(dir(SearchEngine))
    print(SearchEngine.__dict__.keys())
    # print(SearchEngine.attr)

    # Example for how we might test your program:
    # Should also work with nyt199501 !
    searchEngine = SearchEngine("nytsmall", create=True)
    print(searchEngine.executeQuery(['hurricane', 'philadelphia']))
