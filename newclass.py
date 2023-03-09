import xml.etree.ElementTree as ET
from stemming.stemming.porter2 import stem
import string
import pprint

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


class SearchEngine:
    def __init__(self, collectionName, create):
        if create:
            print("Creating index...")
            self.doc=XMLInter(collectionName).dic
            print('Done')


xmltree=XMLInter("nytsmall")
pprint.pprint(xmltree.dic)
'''xmltree.add_text()
xmltree.del_punc()
xmltree.stem()
pprint.pprint(xmltree.dic)'''
searchEngine = SearchEngine("nytsmall", True)
#pprint.pprint(searchEngine.xmlinter.dic)
pprint.pprint(searchEngine.doc)
#print(searchEngine.DOCT)


def executeQueryConsole(self):
    '''
    When calling this, the interactive console should be started,
    ask for queries and display the search results, until the user
    simply hits enter.
    '''
    print("Please enter query, terms separated by whitespace: ")

    # loop asking for query terms ?

    self.queryTerms = input().split(" ")
    self.queryTerms = [stem(word) for word in self.queryTerms]  # stem
    query = np.zeros(len(self.globallist))  # horizontaler Vektor der Länge des Vokabulars
    self.queryset = set()
    for word in self.queryTerms:
        # word = stem(word)
        self.queryset.add(word)
    for word in self.queryset:
        for i in range(len(self.globallist)):
            if self.globallist[i] == word:
                query[i] = self.tf_idf(word, self.queryTerms)

    self.finaldict = {}  # instance attribute defined outside __init__
    for i in range(len(self.globallist)):
        self.finaldict[self.doclist[i]] = Math.sim(self.D[i], query)

    self.lst = list(self.finaldict.items())
    self.lst.sort(key=lambda x: x[1])

    res = "I found the following documents:\n"  # display function ?
    for i in range(10):
        res += self.lst[i][0] + " (" + str(self.lst[i][1]) + ") \n"
    return res