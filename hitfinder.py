#!/usr/bin/env python
from progressbar import ProgressBar, Bar, Percentage, ETA

import json
import sys
import getopt

def findPairs(seeds, utr):
    hits = []

    widgets = [Percentage(),
               ' ', Bar(),
               ' ', ETA()]
    pbar = ProgressBar(widgets = widgets)

    for seed_pair in pbar(seeds):
        if seed_pair[0] in utr and seed_pair[1] in utr:
            hits.append(seed_pair)
    return hits

if __name__ == '__main__':
    utrfile = ''
    seedfile = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hu:s:",["utrfile=","seedfile="])
    except getopt.GetoptError:
        print 'hitfinder.py -u <utr json> -s <mirna seeds json>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'hitfinder.py -u <utr json> -s <mirna seeds json>'
            sys.exit()
        elif opt in ("-u", "--utrfile"):
            utrfile = arg
        elif opt in ("-s", "--seedfile"):
            seedfile = arg

    print seedfile
    print utrfile

    seeds = json.load(open("mirna/%s" % seedfile, 'r'))
    utr = json.load(open("utr/%s" % utrfile, 'r'))
    hits = findPairs(seeds, utr)

    json.dump(hits, open("hits/%s.json" % utrfile,'w'))
