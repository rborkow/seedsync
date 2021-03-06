#!/usr/bin/env python

from Bio import SeqIO
from multiprocessing import Pool

import re
import json
import itertools
import time
import logging

logging.basicConfig(filename='run.log',level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%I:%M:%S.%f %p')

utr_strings = {}
hits = []

def findPairs(seed_pair):
    start = time.time()
    for k, v in utr_strings.iteritems():
        if seed_pair[0] in v and seed_pair[1] in v:
            hits.append(SeedSyncHit(seed_pair, k))
    end = time.time()
    delta = end-start
    logging.info('Seedpair %s | %s done. Time elapsed: %f', seed_pair[0], seed_pair[1], delta)

class UTR(object):
    substrings_dict = {}

    def window(self, fseq, window_size):
        for i in xrange(len(fseq) - window_size + 1):
            yield fseq[i:i+window_size]

    def parse(self):
        substrings = {}

        input_seq_iterator = SeqIO.parse(open("3p_hsa_utr_hg19", "rU"), "fasta")
        for record in input_seq_iterator:
            substrings[record.name] = list(self.window(str(record.seq), 6))
            json.dump(substrings[record.name], open("utr/%s" % record.name, 'w'))
        self.substrings_dict = substrings

    def json_dump(self):
        json.dump(substrings, open("utr_substrings.json",'w'))

class Seeds(object):
    seed_map = {}
    seed_pairs = []

    def dictinvert(self, d):
        inv = {}
        for k, v in d.iteritems():
            keys = inv.setdefault(v, [])
            keys.append(k)
        return inv

    def parse(self):
        substrings = {}

        input_seq_iterator = SeqIO.parse(open("mature.fa", "rU"), "fasta")
        for record in input_seq_iterator:
            if re.search('hsa', record.name):
                substrings[record.name] = str(record.seq)[1:7]

        self.seed_map = self.dictinvert(substrings)

        seeds = self.seed_map.keys()
        self.seed_pairs = list(itertools.combinations(seeds, 2))

        print "Number of seeds : %d" % len(substrings)
        print "Number of unique seeds : %d" % len(self.seed_map)
        print "Number of pairs : %d" % len(self.seed_pairs)


    def json_dump(self):
        json.dump(self.seed_map, open("mirna/hsa_mirna_seed_map.json",'w'))
        json.dump(self.seed_pairs, open("mirna/hsa_mirna_seed_pairs.json",'w'))

class SeedSyncHit(object):
    def __init__(self, seedpair, utr):
        self.seedpair = seedpair
        self.utr = utr

if __name__ == '__main__':
    UTR = UTR()
    Seed = Seeds()

    #UTR.parse()
    #utr_strings = UTR.substrings_dict


    Seed.parse()
    Seed.json_dump()


    #pool = Pool()
    #pool.map(findPairs, Seed.seed_pairs)
    #pool.close()
    #pool.join()

    #print "Number of co-occurrences: %d" % len(hits)
    #json.dump(hits, open("cooccurrence_hits.json",'w'))
