#!/usr/bin/env python
from progressbar import ProgressBar, Bar, Percentage, ETA
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

    widgets = [Percentage(),
               ' ', Bar(),
               ' ', ETA()]
    pbar = ProgressBar(widgets = widgets)

    for seed_pair in pbar(seedpairs):
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

    #for utrfile in os.listdir('utr'):
    #    utr = set(json.load(open("utr/%s" % utrfile, 'r')))
    #    hits = findPairs(utr)
    #    json.dump(hits, open("hits/%s.json" % utrfile,'w'))
