#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Python2
class BTree:
    def __init__ (self, x):
        self.rt = x
        self.left = None
        self.right = None
    def setLeft (self, a):
        self.left = a
    def setRight (self, a):
        self.right = a
    def root (self) :
        return self.rt
    def leftChild (self):
        return self.left
    def rightChild (self):
        return self.right


# Python1
class SBTree(BTree):
    mida = 1
    def setLeft(self, a):
        BTree.setLeft(self, a)
        SBTree.mida += 1

    def setRight(self,a):
        BTree.setRight(self, a)
        SBTree.mida += 1

    def getSize(self):
        return SBTree.mida

def min0(a):
    if a == None:
        None
    elif a.root() in d:
        d[a.root()] = d[a.root()]+1
    else:
        d[a.root()] = 1



def minOccur(a):
    global d
    d = {}
    d[a.root()] = 1
    min0 (a.leftChild())
    min0 (a.rightChild())
    print(d)
    return ("hill")




def Main():
    a = SBTree(8)
    a1 = SBTree(5)
    a2 = SBTree(8)
    a3 = SBTree(3)
    a4 = SBTree(8)
    a5 = SBTree(3)
    a6 = SBTree(5)
    a5.setRight(a6)
    a3.setRight(a4)
    a3.setLeft(a5)
    a1.setLeft(a3)
    a1.setRight(a2)
    a.setLeft(a1)
    print (a.getSize())
    print (minOccur(a))


if __name__ == '__main__':
    Main()
