#!/usr/bin/python3
# -*- coding: utf-8 -*-
from ast import literal_eval
from functools import reduce
# aux
def mul2(x):
    return x*x


# problem 1.1
def diferents(llista):
    count = 0
    new_set= set(llista)
    return len(new_set)


# problem 1.2
def max_list(llista):
    max_l = 0
    for x in llista:
        if x > max_l:
            max_l = x
    return max_l

# problem 1.3
def mitjana_list(llista):
    suma = 0
    media = 0
    for x in llista:
        suma = suma + x
    media = suma / len(llista)
    return media

# problem 1.4
def aplanar(llista):
    if len(llista) == 0:
        return []
    else:
        e = llista.pop()
        if isinstance (e, int):
            new_l = aplanar(llista)+[e]
        else:
            new_l = aplanar(llista)+aplanar(e)
    return new_l


# problem 1.5
def insert(x, llista):
    t = False
    for e in llista:
        if (x < e) and not t:
            llista.insert(llista.index(e), x)
            t = True
    return llista

# problem 1.6
def dos(llista):
    senars = [x for x in llista if x%2 != 0]
    parells = [x for x in llista if x not in senars]
    return senars, parells

# problem 1.7
def div(x):
    noprimers = [j for i in range(2, x) for j in range(i*2, x, i)]
    primers = [x for x in range(2, x) if x not in noprimers]
    l = [i for i in primers if x%i == 0]
    return l


# problem 2.1
def mul_list(llista):
    l = reduce(lambda x,y: x*y, llista)
    return l


# problem 2.2.1
def mul_list_p(llista):
    n_l = dos(llista)
    if len(n_l[1]) > 0:
        l = mul_list(n_l[1])
    else:
        l = 1
    return l


# problem 2.2.2
def mul_list_p_2(llista):
    p = 1
    l = list(filter(lambda x: x%2==0, llista))
    if len(l) > 0:
        p = mul_list(l)
    return p


# problem 2.3
def invertir(llista):
    l = aplanar(reduce(lambda x,y: [y]+[x],llista,[]))
    return l

# problem 2.4
def apareix(x, llista):
    l = []
    for ll in llista:
        l = l + [len(list(filter(lambda y: y==x, ll)))]
    return l

# problem 3.1
def zipWith(f, l1, l2):
    l = list(map(f,l1,l2))
    return l


def takeWhile(f,ll):
    l = []
    t = True
    for x in ll:
        if f(x) and t:
            l.append(x)
        else:
            t = False
    return l

def dropWhile(f,ll):
    l = []
    t = True
    for x in ll:
        if not f(x):
            l.append(x)
    return l


def foldl(f, x, ll):
    for l in ll:
        x = f(x,l)
    return x


def foldr (f, x, ll):
    i = len(ll)-1
    while i >= 0:
        x = f(ll[i],x)
        i -= 1
    return x

def scanl(f, x, ll):
    s = []
    s.append(x)
    for l in ll:
        x = f(x,l)
        s.append(x)
    return s


# problem 3.2
def countIf(f, ll):
    count = 0
    for l in ll:
        if f(l):
            count += 1
    return count

# problema 4.1
def new_map(fun, llista):
    new_list = [fun(x) for x in llista]
    return new_list


# problem 4.2
def new_filter(fun, llista):
    new_list = [x for x in llista if fun(x)]
    return new_list


# problem 4.3
def doble_llista(l1,l2):
    l = [(x,y) for x in l1 for y in l2 if x%y== 0]
    return l


def Main():
    l = literal_eval(input("introduce x\n"))
    print (doble_llista([1,2,3,4,5],l))

if __name__ == '__main__':
    Main()
