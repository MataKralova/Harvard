#!/usr/bin/env python3

# Algorithms to produce list of similar elements between 2 files
# Done by Mata

import csv
from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    list = []
    alines = a.splitlines()
    blines = b.splitlines()
    # allset = {line for line in aset if line in bset}
    allset = set(alines) & set(blines)
    for x in allset:
        list.append(x)
    return list


def sentences(a, b):
    """Return sentences in both a and b"""

    list = []
    asent = sent_tokenize(a)
    bsent = sent_tokenize(b)
    allset = set(asent) & set(bsent)
    for x in allset:
        list.append(x)
    return list


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    list = []
    astr = []
    bstr = []
    alimit = len(a) - n + 1
    blimit = len(b) - n + 1
    for i in range(alimit):
        astr.append(a[i:(i + n)])
    for i in range(blimit):
        bstr.append(b[i:(i + n)])
    allset = set(astr) & set(bstr)
    for x in allset:
        list.append(x)
    return list
