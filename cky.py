#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from greader import *
from treelib import Node, Tree


#### CKY ALGORITHM

#Pseudocode from wikipedia
def cky(Roots, NT, T, GT, GNT, words, show_table=True, gettree=True):
    #The input string s consist of n letters, a1... an.
    n = len(words)
    #The grammar contain r terminal and nonterminal symbols R1... Rr.
    r = len(NT)
    #Let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
    P = np.zeros((n,n,r))
    if gettree:
        BP = np.empty((n,n), dtype=object)
        for i in range(0, n):
            for j in range(0, n):
                BP[i,j] = []


    #For each i = 1 to n
    for i in range(0,n):
        # For each unit production Rj -> ai, set P[i,1,j] = true.
        for R,A in GT.items():
            w = words[i]
            for a in A:
                if words[i] == a[0]:
                    P[0, i, NT.index(R)] = 1
                    if gettree: BP[0,i].append(BackPointer(R, data=a[0]))

    #For each i = 2 to n -- Length of span
    for i in range(2, n+1):
        #For each j = 1 to n-i+1 -- Start of span
        for j in range(1, n-i+2):
            #For each k = 1 to i-1 -- Partition of span
            for k in range(1, i):
                #For each production RA -> RB RC
                for l,R in GNT.items():
                    for r in R:
                        #if P[k,j,B] and P[i-k,j+k,C] then set P[i,j,A] = true
                        if P[k-1, j-1, NT.index(r[0])] == 1 and \
                            P[i-k-1,j+k-1, NT.index(r[1])] == 1:
                            P[i-1,j-1,NT.index(l)] = 1

                            if gettree:
                                BP[i-1,j-1].append(BackPointer(l,
                                        p1=getBP(BP[k-1, j-1], r[0]),
                                        p2=getBP(BP[i-k-1,j+k-1], r[1])))


    # if any of P[n,1,x] is true (x is iterated over the set s, where s are all the indices for Rs) then
    #   Then string is member of language
    #   Else string is not member of language
    if show_table: display_table(P, T, NT, words)
    if gettree: create_trees(BP, Roots, NT, n)

    for r in Roots:
        j = NT.index(r)
        if P[n-1,0,j] == 1: return (True, P)

    return (False, P)

def getBP(BP, NT):
    for bp in BP:
        if bp.name == NT:
            return bp

    return None

def display_table(P, T, NT, words):
    d = P.shape

    ##calculate the padding and the cells content
    cells = words
    cells1 = []
    for i in range(d[0]):
        for j in range(0, d[1]):
            c = []
            for k in range(0, d[2]):
                if P[i,j, k] != 0:
                    c.append(NT[k])

            if len(c) != 0:
                cells1.append('|'.join(c))
                #cells.append(','.join(c))
            else:
                cells1.append("          ")
                #cells.append(".")
    l = np.array(cells1).reshape(d[0],d[0])

    #print the table
    for i in range(d[0]):
        for j in range(d[0]):
            if len(l[i,j]) < 10 :
                s = str(i) + str(j+1)
                l[i,j] = l[i,j] + '|' + str(i) + ',' + str(j+1)

    print(('\n0  ' + ''.join([("%-*s" % (15, i)) for i in words])))
    print("-"*100)
    for i in range(d[0]):
        print(("%d " % (i)), end=' ')
        print((''.join([("%-*s" % (15, l[i,j])) for j in range(d[0]) ])))
        print("-"*100)
        # time.sleep(1)

#### BACK POINTER

class BackPointer:

    def __init__(self, name, data=None, p1 = None, p2 = None):
        self.name = name
        self.data = data
        self.pointers = []
        if not p1 is None: self.pointers.append(p1)
        if not p2 is None: self.pointers.append(p2)


#### TREE PARSER

def create_trees(BP, Roots, NT, n):

    for bp in BP[n-1,0]:
        if bp.name in Roots:
            print('\nTree')
            t = Tree()
            create_tree(t, bp, 0, 1)
            t.show(key=lambda x: x.identifier)


def create_tree(t, bp, pid, nid):

    if pid == 0:
        t.create_node(bp.name, nid)
    else:
        tag = bp.name
        if not bp.data is None: tag = "%s (%s)"%(tag, bp.data)
        t.create_node(tag, nid, pid)

    if len(bp.pointers) > 0:
        pid = nid
        #left
        #print len(bp.pointers[0])
        nid = create_tree(t, bp.pointers[0], pid, nid+1)
        #right
        #print len(bp.pointers[1])
        nid = create_tree(t, bp.pointers[1], pid, nid+1)

    return nid
R, NT, T, Gt, GT, valid = parse_cnf(open("/home/wolf/Downloads/pyCKY-master/G1.txt"))
string = "lá thu kêu xào xạc"

list(string.split(" "))
cky(R, NT, T, Gt, GT, list(string.split(" ")))
