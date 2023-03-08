dic={
    'germany': ['bmw!', '#benz', ''],
    'japan': ['honda?', 't"()@oyota']#, ['hunday]]
}

import string
#print(dir(string))
puncs=''
for i in string.punctuation:
    puncs+=i
print(puncs)
#'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
p = {i:"" for i in string.punctuation} #dictionary: translation for any i is the empty string
print(p)

for key, value in dic.items():
    table=str.maketrans(p) #returns the translation table
    for car in range(len(value)):
        value[car]=value[car].translate(table)
import pprint
pprint.pprint(dic)
#for key, value in dic.items():
    #for car in range(len(value)):

numdict={
    'brackett': 1,
    'brackett,': 1,
    'brewster': 1,
    'brooklin': 3
}
m=max(numdict.items(), key=lambda x:x[1])
#print(m) #('brooklin', 3)
#print(m[1]) #3


#pprint.pprint(numdict)

my_list = ['Stem', 'constitute', 'Sedge', 'Eflux', 'Whim', 'Intrigue']
my_list.sort()
#print(my_list)

#arryas, vectors in python, dot product, sim

import numpy as np
from numpy.linalg import norm

a = np.array([1, 2, 3, 4, 5])
print(a)
b=np.array([1, 2, 1, 3, 0])
Dot=np.dot(a,b)
print(Dot)
sim=Dot/(norm(a)*norm(b)) #cosine similarity
print(sim)
b[1]=1
print(b)


txt = "hello, my name is Peter, I am 26 years old"

x = txt.split(", ")
print(x)
print(x[0])

a=np.array([[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]
             ]
            )

a[1][1]=1
print(a)
d=a[1][:] #zweite Zeile: gut, weil meine Vektoren laufen horizontal
print(d)

e=a[:][1]
print(e)

print('#')
print(a[:][1]) #funktioniert nicht :(, egal, brauche ich nicht

b=np.zeros((3,4)) #(Anzahl der Zeilen, Anzahl der Spalten)
b[1][1]=1
print(b)
k=1
for i in range(3):
    for j in range(4):
        b[i][j]=k
        k+=1
print(b)

query=np.zeros(5)
print(query)

for i in range(10):
    print(i)
