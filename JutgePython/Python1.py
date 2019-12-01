#!/usr/bin/python3

import sys


def absValue(x):
    if x < 0:
        x *= -1
    return(x)


def power(x, p):
    if p == 0:
        return 1
    return x * power(x, p-1)


def isPrime(x):
    if x < 2:
        return False
    for i in range(2, x):
        if x % i == 0:
            return False
    return True


def slowFib(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return slowFib(x-1) + slowFib(x-2)


def quickFib(n):
    #diccionario
    fibo = {}
    fibo[0] = 0
    fibo[1] = 1
    for i in range(2, n + 1):
        fibo[i] = fibo[i-1] + fibo[i-2]
    return fibo[n]
