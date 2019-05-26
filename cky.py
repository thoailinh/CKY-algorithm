#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from greader import *
import time
###############################################################
#### CKY ALGORITHM
###############################################################
#Pseudocode from wikipedia
def cky(Roots, NT, T, GT, GNT, words):
    #The input string s consist of n letters, a1... an.
    # print(words) #['nam', 'hoc', 'bai', 'o', 'truong']
    # print(type(words))
    n = len(words)
    #The grammar contain r terminal and nonterminal symbols R1... Rr.
    # print(NT, type(NT)) # (['VB', 'PP', 'VP', 'S', 'IN', 'NP'], <type 'list'>)
    r = len(NT)
    #Let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
    P = np.zeros((n,n,r))


    #For each i = 1 to n
    for i in range(n):
        # For each unit production Rj -> ai, set P[i,1,j] = true.
        for R,A in GT.items():
            w = words[i]
            for a in A:
                if words[i] == a[0]:
                    P[0, i, NT.index(R)] = 1

    
    #For each i = 2 to n -- Length of span
    for i in range(2, n+2):
        #For each j = 1 to n-i+1 -- Start of span
        for j in range(1, n-i+2):
            #For each k = 1 to i-1 -- Partition of span
            for k in range(1, i):
                #For each production RA -> RB RC
                for l,R in GNT.items():
                    for r in R:
                        #if P[k,j,B] and P[i-k,j+k,C] then set P[i,j,A] = true
                        if P[k-1, j-1, NT.index(r[0])] == 1 and P[i-k-1,j+k-1, NT.index(r[1])] == 1:
                            P[i-1,j-1,NT.index(l)] = 1
    # if any of P[n,1,x] is true (x is iterated over the set s, where s are all the indices for Rs) then
    #   Then string is member of language
    #   Else string is not member of language
    display_table(P, T, NT, words)


def display_table(P, T, NT, words):
    d = P.shape 
    ##calculate the padding and the cells content
    cells = []

    for i in range(d[0]):
        for j in range(0, d[1]):
            c = []
            for k in range(0, d[2]):
                if P[i,j, k] != 0:
                    c.append(NT[k])
            if len(c) != 0:
                cells.append('|'.join(c))
            else:
                cells.append('             ')

    l = np.array(cells).reshape(d[0],d[0])

    #print the table
    for i in range(d[0]):
        for j in range(d[0]):
            if len(l[i,j]) < 10 :
                s = str(i) + str(j+1)
                l[i,j] = l[i,j] + '|' + str(i) + ',' + str(j+1)

    print(('\n0  ' + ''.join([("%-*s" % (15, i)) for i in words])))
    for i in range(d[0]):
        print(("%d " % (i)), end=' ')
        print((''.join([("%-*s" % (15, l[i,j])) for j in range(d[0]) ])))
        time.sleep(1)


R, NT, T, Gt, GT, valid = parse_cnf(open("/home/wolf/Downloads/pyCKY-master/G1.txt"))
string = "Nam có nhiều bạn ở trường"

list(string.split(" "))
cky(R, NT, T, Gt, GT, list(string.split(" ")))
