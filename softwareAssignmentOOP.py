
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

class XMLInter:
    def __init__(self, collectionName):
        self.tree=ET.parse(collectionName+'.xml')
        self.root = self.tree.getroot()
        self.dic={}
        self.add_text()
        self.del_punc()
        self.stem()

    def add_text(self):
        for doc in self.root.findall('.//DOC'):
            self.dic[doc.attrib['id']] = []
            try:
                headline = doc.find('HEADLINE').text
            except AttributeError:
                continue #pass ? so erkennt es keine Texte, die keine Überschriften haben
            self.dic[doc.attrib['id']].extend(headline.lower().split())
            txt = doc.find('TEXT').text
            self.dic[doc.attrib['id']].extend(txt.lower().split())
            try:  # unnötig?
                doc.find('P')
            except AttributeError:
                continue
            for p in doc.findall('.//P'):
                self.dic[doc.attrib['id']].extend(p.text.lower().split())

    def del_punc(self):
    # delete punctuation
        p = {i: "" for i in string.punctuation}  # dictionary: translation for any i is the empty string
        for key, value in self.dic.items():
            table = str.maketrans(p)  # returns the translation table
            for i in range(len(value)):
                value[i] = value[i].translate(table)
    def stem(self):
        for doc in self.dic.keys():
            self.dic[doc] = list(filter(lambda w: w != '', self.dic[doc]))  # delete words that are the empty string from list
            self.dic[doc] = [stem(word) for word in self.dic[doc]]  # List Comprehension to stem every word

class Math:
    @staticmethod #similarity of two vectors
    def sim(a, b):
        if norm(a) * norm(b) != 0:
            return np.dot(a, b) / (norm(a) * norm(b))
        # return 0 # ? oder Fehler ?

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

###################################
        if create:
            print("Creating index...")
            self.dic=XMLInter(collectionName).dic

            self.maxocc = {}
            for doc in self.dic.keys():
                self.maxocc[doc] = self.maximumocc(doc)

            self.idf_file = open(collectionName + '.idf', 'w+')
            self.tf_file = open(collectionName + '.tf', 'w+')
            self.write_idf()
            self.write_tf()

            #seome test
            pprint.pprint(self.maxocc)  # ACHTUNG: maxocc values manchmal 0, obwohl
            print(self.maximumocc('NYT_ENG_19950101.0048'))  # works; 30

        if not create:
            print("Reading index from file...")

        self.idf_file=open(collectionName + '.idf', 'r')
        self.tf_file=open(collectionName + '.tf', 'r')




###################################

        # weight vector (tf.idf for each word in doc) for each doc (matrix)
        # dict[doc id]=[List of tfidf scores for word at position i], i referring to the vocab

        self.vocab=self.count_vocab()

        self.tidict = {}
        for key in self.dic.keys():
            self.tidict[key] = np.zeros(len(self.vocab))
        for key in self.tidict.keys():
            for i in range(len(self.vocab)): #=self.tidict[key])
                self.tidict[key][i] = self.tf_idf(self.vocab[i], self.tidict[key])  # tf_idf(term, doc)
        #hier bleibt es beim ersten tf_idf hängen

        pprint.pprint(self.tidict)

        print("Done.")


###########################
    def count_vocab(self):
        vocabset = set()
        for doc in self.dic:
            for word in self.dic[doc]:
                vocabset.add(word)
        return tuple(vocabset)

    # (6) compute idf, write idf into file
    def write_idf(self):
        setofwords = set()
        for doc in self.dic.keys():
            for word in self.dic[doc]:
                setofwords.add(word)
        listofwords = list(setofwords)
        listofwords.sort()  # alphabetisch ordnen: liste nach anfangsbuchstabe sortieren
        #schreiben
        for word in listofwords:
            self.idf_file.write(str(word) + '\t' + str(self.idf(word)) + '\n')

    def write_tf(self):
        for doc in self.dic:
            setofw = set()
            for word in self.dic[doc]:
                setofw.add(word)
            listofw = list(setofw)
            listofw.sort()
            #schreiben
            for word in listofw:
                self.tf_file.write(str(doc) + '\t' + str(word) + '\t' + str(self.tf(word, doc)) + '\n')

        # dict for maxOccurrence// or function?

    def maximumocc(self, doc):
        'maximum occurrences of any term in doc'
        numdoc = {}
        for word in set(self.dic[doc]):
            # count each word
            numdoc[word] = 0
            for i in self.dic[doc]:
                if word == i:
                    numdoc[word] += 1
        m = max(numdoc.values(), key=lambda x: x, default=0)  # max by value
        return m

    def idf(self, term):
        'log(number of all documents/number of documents that contain term)'
        numdocs = 0 # keine instance attributes mehr
        numdocsterm = 0
        for doc in self.dic.keys():
            numdocs += 1
            if term in self.dic[doc]:
                numdocsterm += 1
        return math.log(numdocs / numdocsterm)

    def tf(self, term, doc):
        'number of times term occurs in doc/maximum occurrences of any term in doc'
        numofterm = 0
        for word in self.dic[doc]:
            if word == term:
                numofterm += 1
        return numofterm / self.maxocc[doc] #oder maxocc[doc] als dict, sodass maxocc[doc]=maximumocc(doc) -> dict schneller




    def tf_idf(self, term, doc): #irgendwie hat es hier mit ein wahnsinniges Problem: TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
        idf_file=self.idf_file
        def read_idf(term):
            for line in idf_file.readlines():
                if line.split("\t", 2)[0] == term:
                    print(" hi", float(line.split("\t", 2)[1]))
                    return float(line.split("\t", 2)[1])
        tf_file=self.tf_file
        def read_tf(term, doc):
            for line in tf_file.readlines():
                if line.split("\t", 3)[0] == doc:
                    if line.split("\t", 3)[1] == term:
                        print(float(line.split("\t", 3)[2]))
                        return float(line.split("\t", 3)[2])

        return read_idf(term)*read_tf(term, doc)




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

        queryTerms=[stem(word) for word in queryTerms] #stem, List Comprehension
        query=np.zeros(len(self.vocab)) #horizontaler Vektor der Länge des Vokabulars
        queryset=set() #instance attribute defined outside __init__
        for word in queryTerms:
            queryset.add(word)
        for word in queryset:
            for i in range(len(self.vocab)):
                if self.vocab[i]==word:
                    query[i]=self.tf_idf(word, queryTerms) #tfidf Funktion muss Klassenfunktion sein


        def display_results(self):
            finaldict = {}  # instance attribute defined outside __init__
            for key in self.tidict.keys():
                finaldict[key] = Math.sim(self.self.tidict[key], query)

            # pprint.pprint(self.finaldict)

            lst = list(self.finaldict.items())  # instance attribute defined outside __init__
            lst.sort(key=lambda x: x[1])

            res = "I found the following documents:\n"
            for i in range(10):
                if self.lst[i][1] != 0:
                    res += self.lst[i][0] + " (" + str(self.lst[i][1]) + "\n"
            return res

        print(self.display_results)



        
    def executeQueryConsole(self):
        '''
        When calling this, the interactive console should be started,
        ask for queries and display the search results, until the user
        simply hits enter.
        '''
        pass
        print("Please enter query, terms separated by whitespace: ")
        #loop asking for query terms ?

    
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
