#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ast import literal_eval

def evaluate(e):
    if isinstance(e, list):
        if len(e) == 0:
            return 1
        else:
            t = 1
            for elem in e:
                n = evaluate(elem)
                if isinstance(n, bool):
                    t = t
                else:
                    t = t * n
            return t
    elif isinstance(e, tuple):
        if len(e) == 0:
            return 0
        else:
            t = 0
            for elem in e:
                n = evaluate (elem)
                if isinstance(n, bool):
                    t = t
                else:
                    t = t + n
            return t

    elif isinstance(e, int):
        return e
    else:
        return False


def s(*xs):
    m = 0
    for x in xs: m += x
    return m


def s2(a,b):
    return a+b


def partial(f,x):
    def g(*xs):
        return f(*xs,x)
    return g

def Main():
    x = literal_eval(input("introduce x\n"))
    ff = partial(partial(s, 3), 1)
    print (ff(x))


if __name__ == '__main__':
    Main()
