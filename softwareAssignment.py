
'''
Introduction to Python Programming (aka Programmierkurs I, aka Python I)
Software Assignment
'''

#preprocessing

import sys
import xml.etree.ElementTree as ET
import string
from collections import defaultdict
from stemming.stemming.porter2 import stem
import math
import pprint

tree = ET.parse('nytsmall.xml')
root = tree.getroot()
print(root)

dic={}# self.dic

for doc in root.findall('.//DOC'):
    dic[doc.attrib['id']]=[]
    #print(doc.attrib['id']) #print statements sollen später Dictionaryeinträge werden
    try:
        headline= doc.find('HEADLINE').text
    except AttributeError:
        continue
    # print(headline)
    dic[doc.attrib['id']].extend(headline.lower().split()) #nicht append, weil append die Wörter jedes Paragraphen als extra Liste in der Liste anhängt
    txt = doc.find('TEXT').text
    # print(txt)
    dic[doc.attrib['id']].extend(txt.lower().split())
    try: #unnötig?
        doc.find('P')
    except AttributeError:
        continue
    for p in doc.findall('.//P'):
        #print(p.text)
        dic[doc.attrib['id']].extend(p.text.lower().split())

#delete punctuation
p = {i:"" for i in string.punctuation} #dictionary: translation for any i is the empty string
for key, value in dic.items():
    table=str.maketrans(p) #returns the translation table
    for i in range(len(value)):
        value[i]=value[i].translate(table)


#stem
for doc in dic.keys():
    dic[doc]=list(filter(lambda w:w!='', dic[doc])) # delete words that are the empty string from list
    #for i in range(len(dic[doc])): #modifying the list while iterating over it
        #if dic[doc][i] == '':
            #dic[doc].pop(i)
    dic[doc]=[stem(word) for word in dic[doc]] # List Comprehension to stem every word

import pprint
pprint.pprint(dic)



# (6) compute idf
def idf(term):
    'log(number of all documents/number of documents that contain term)'
    numdocs=0
    numdocsterm=0
    for doc in dic.keys():
        numdocs+=1
        if term in dic[doc]:
            numdocsterm+=1
    return math.log(numdocs/numdocsterm)
print(idf('can'))

#write idf for each word to a file (nytsmall.idf) -> writelines(word, idf)

setofwords=set()
for doc in dic.keys():
    for word in dic[doc]:
        setofwords.add(word)
listofwords=list(setofwords)
listofwords.sort() #müssen wir das alphabetisch ordnen ??, dann liste -> nach anfangsbuchstabe sortieren

with open('nytsmall.idf', 'w') as file:
    for word in listofwords:
        file.write(str(word)+'\t'+ str(idf(word))+'\n')


# (7) compute tf
#dict for maxOccurence
maxocc={}
numdict={}
for doc in dic.keys():
    #maxocc[doc]=None
    numdict[doc]={} #für jedes doc ein neues numdict
    for word in set(dic[doc]):
        numdict[doc][word]=0
        for i in dic[doc]:
            if word==i:
                numdict[doc][word]+=1
        #pprint.pprint(numdict) #ich brauche nur das Wort mit maximaler Anzahl//die maximale Anzahl
    m=max(numdict[doc].values(), key=lambda x:x, default=0)#max by value
    maxocc[doc]=m

#pprint.pprint(maxocc)

def tf(term, doc):
    'number of times term occurs in doc/maximum occurrences of a term in doc'
    numofterm=0
    for word in dic[doc]:
        if word==term:
            numofterm+=1
    #print(numofterm)
    #print(maxocc[doc])
    return numofterm/maxocc[doc]
print(tf('inventor', 'NYT_ENG_19950101.0060')) #=4

#write tf for each word in each document to a file (nytsmall.tf) -> writelines(doc id, word, tf)
with open('nytsmall.tf', 'w') as file:
    for doc in dic:
        setofw=set()
        for word in dic[doc]:
            setofw.add(word)
        listofw = list(setofw)
        listofw.sort()
        for word in listofw:
            file.write(str(doc)+'\t'+str(word)+'\t'+ str(tf(word, doc))+'\n') #später: if KeyError: tf(word, doc)=0



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
        pass
    
    
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
        pass
        
    def executeQueryConsole(self):
        '''
        When calling this, the interactive console should be started,
        ask for queries and display the search results, until the user
        simply hits enter.
        '''
        pass
    
if __name__ == '__main__':
    '''
    write your code here:
    * load index / start search engine
    * start the loop asking for query terms
    * program should quit if users enters no term and simply hits enter
    '''
    # Example for how we might test your program:
    # Should also work with nyt199501 !
    searchEngine = SearchEngine("nytsmall", create=True)
    #print(searchEngine.executeQuery(['hurricane', 'philadelphia']))
