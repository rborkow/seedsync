#!/usr/bin/env python
from multiprocessing import Pool

import json
import sys
import getopt
import os

seedpairs = []

def loadUTR(utrfile):
    utr = set(json.load(open("utr/%s" % utrfile, 'r')))
    return utr


def findPairs(utrfile):
    utr = loadUTR(utrfile)

    hits = []
    print utrfile
    for seed_pair in seedpairs:
        if seed_pair[0] in utr and seed_pair[1] in utr:
            hits.append(seed_pair)
    json.dump(hits, open("hits/%s.json" % utrfile,'w'))

if __name__ == '__main__':
    seedfile = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:",["seedfile="])
    except getopt.GetoptError:
        print 'hitfinder.py -s <mirna seeds json>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'hitfinder.py -s <mirna seeds json>'
            sys.exit()
        elif opt in ("-s", "--seedfile"):
            seedfile = arg

    seedpairs = json.load(open("mirna/%s" % seedfile, 'r'))
    utrfiles = os.listdir('utr')


    pool = Pool()
    pool.map(findPairs, utrfiles)
    pool.close()
    pool.join()
