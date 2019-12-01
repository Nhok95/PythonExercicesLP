#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ast import literal_eval

# Python1
def invert(ll):
    if isinstance (ll, list):
        nl = ()
        for l in ll:
            aux = invert (l)
            nl = nl+(aux,)
        return nl
    elif isinstance (ll, tuple):
        nl = []
        for l in ll:
            aux = invert (l)
            nl = nl+[aux]
        return nl
    else:
        return ll


# Python2
class Trie:
    def __init__(self):
        self.val = None
        self.entries = {}

    def value(self, k):
        if len(k) == 1:
            return self.val
        elif k[0] not in self.entries:
            #print ("Willy")
            return None
        else:
            #print ("something")
            return self.entries[k[0]].value(k[1:])

    def insert(self, k, v):
        if len(k) > 1:
            self.val = None
            a = Trie()
            #print ("i:", k[0])
            a.insert(k[1:],v)
            self.entries.[k[0]] = a
        elif len(k) == 1:
            self.val = v
            a = Trie()
            #print ("2:",k[0])
            #print ("v:", val)
            a.insert(k[1:],v)
            self.entries[k[0]] = a





def Main():
    #x = literal_eval(input("introduce x\n"))
    a = Trie()
    a.insert("sala",16)
    print (a.value("sala"))
    a.insert("sal",21)
    print (a.value("sal"))
    a.insert("sala",17)
    a.insert("sol",38)
    a.insert("son",57)
    print (a.value("sol"))
    print (a.value("sala"))
    print (a.value("salsa"))
    print (a.value("son"))
    print (a.value("sal"))


if __name__ == '__main__':
    Main()
