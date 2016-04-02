#!/usr/bin/env python

from Bio import SeqIO

import re
import json
import itertools
import time

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


    def json_dump(object):
        json.dump(seed_map, open("hsa_mirna_seed_map.json",'w'))
        json.dump(seed_pairs, open("hsa_mirna_seed_pairs.json",'w'))

class SeedSyncHit(object):
    def __init__(self, seedpair, utr):
        self.seedpair = seedpair
        self.utr = utr

class SeedSync(object):
    hits = []

    def __init__(self, seedObject, utrObject):
        self.Seed = seedObject
        self.UTR = utrObject

    def findPairs(self):
        count = 0
        start = time.time()
        for pair in Seed.seed_pairs:
            for k, v in UTR.substrings_dict.iteritems():
                if pair[0] in v and pair[1] in v:
                    self.hits.append(SeedSyncHit(pair, k))
            count = count + 1
            print count, time.time()
        end = time.time()
        print (end - start)
        print "Number of co-occurrences: %d" % len(self.hits)

if __name__ == '__main__':
    UTR = UTR()
    Seed = Seeds()
    UTR.parse()
    Seed.parse()
    ss = SeedSync(Seed, UTR)
    ss.findPairs()
