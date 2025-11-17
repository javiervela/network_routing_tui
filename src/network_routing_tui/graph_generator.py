from graph import Graph
import random

def get_name(i):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    k = len(alpha)
    res = ""
    n = 1
    while i != 0:
        j = i%pow(k,n)
        i -= j
        res = alpha[j] + res
        n += 1
    return res

def gen_random(n = 10, p = 0.5):
    G = Graph()
    for i in range(n):
        for j in range(i+1,n):
            if random.random() < p:
                pass
