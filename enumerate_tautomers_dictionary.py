#!/usr/bin/env python

import numpy as np
import time
import json

t = [] # time stamps

zids = []

t.append(time.time())

#for b in range(1, 6227):
for b in range(1, 6227):
    if b % 100 == 0: print("batch%04d" % b)
    try:
        with open('out/batch%04d.csv' % b) as f:
            first = True
            for line in f:
                if not first:
                    zinc = line.split(',')[4]
                    #nr = np.int64(zinc.strip()[-12:])
                    nr = int(zinc.strip()[-12:])
                    zids.append(nr)
                else:
                    first = False
    except:
        print('missing: %04d' % b)

t.append(time.time())
print("reading took %.2f seconds" % (t[-1] - t[-2]))

mydict = {}
for k in zids:
    mydict[k] = mydict.get(k, 0) + 1

t.append(time.time())
print("mydict %.2f seconds" % (t[-1] - t[-2]))

short = {}
for k in mydict:
    if mydict[k] > 1:
        short[k] = 0
    
t.append(time.time())
print("Cleaning %.2f seconds" % (t[-1] - t[-2]))


# 

for b in range(1, 6227):
    bybatch = {}
    if b % 100 == 0: print("batch%04d" % b)
    try:
        with open('out/batch%04d.csv' % b) as f:
            first = True
            for line in f:
                if not first:
                    zinc = line.split(',')[4]
                    nr = int(zinc.strip()[-12:])
                    if nr in short:
                        short[nr] += 1
                        bybatch[nr] = bybatch.get(nr, short[nr])
                else:
                    first = False
    except:
        print('missing: %04d' % b)

    json.dump(bybatch, open('tautjson/%04d.json' % b, 'w'))

t.append(time.time())
print("by batch %.2f seconds" % (t[-1] - t[-2]))

if 0:

    json.dump(short, open('/dev/shm/test.json', 'w'))
    t.append(time.time())
    print('json write %.2f seconds' % (t[-1] - t[-2]))
    
    d = json.load(open('/dev/shm/test.json'))
    t.append(time.time())
    print('json load %.2f seconds' % (t[-1] - t[-2]))



### PICKLE IS CRAZY SLOW
#cPickle.dump(mydict, open('/dev/shm/test.pickle', 'wb'), protocol=2)
#t.append(time.time())
#print('json write %.2f seconds' % (t[-1] - t[-2]))
#
#d = cPickle.load(open('/dev/shm/test.pickle'))
#t.append(time.time())
#print('json load %.2f seconds' % (t[-1] - t[-2]))
