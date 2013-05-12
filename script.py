import sys, json, string, time, numpy as np

# http://answers.google.com/answers/threadview?id=149284

start = 0
end = 1000

# -------- utilities
#twtfile = open('output.txt')
twtfile = open('output2_fed1000.txt')
tweets  = twtfile.readlines()
#tweets  = tweets[start:end]
ntweets = len(tweets)
dlim    = '\t'
dt      = ('S20, i4')
cols    = (0,1)
mypunc  = '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~'
absent  = {} # dictionary of absent words
wrdcnt  = {}


# -------- read the sentiment file and initialize the tweet sentiment sum
wrd, snt = np.loadtxt('AFINN-111.txt', usecols=cols, dtype=dt, \
                      delimiter=dlim, unpack=True)
wrd, snt = list(wrd),list(snt)
nsnt     = len(snt)
sntsum   = np.zeros(ntweets, dtype=np.int64)

# -------- strip words of punctuation
wrd_cln = [i.translate(string.maketrans("",""), mypunc) for i in wrd]

# -------- make special cases
wrd_spc, snt_spc = [], []
for i in xrange(len(wrd_cln)):
    if len(wrd_cln[i].split())>1:
        wrd_spc.append(wrd_cln[i])
        snt_spc.append(snt[i])

# -------- make dictionary of all words
for i in wrd: wrdcnt[i] = 0L


# -------- make sure that the tweet has text
def checktext(tweet):
    try:
        text = tweet[u'text']
    except:
        text = None
    return text



# -------- parse tweets with json
jload = [checktext(json.loads(i)) for i in tweets]
w     = np.where(jload)[0]



# -------- loop through tweets
for itweet in w:

    # -------- print progress
#    if itweet % 500 == 0:
#        print('{0} out of {1} tweets'.format(itweet,ntweets-1))

    # -------- load the tweet and encode
    ttweet = \
    jload[itweet].encode("ascii", 
        "ignore").encode("utf-8").lower().translate(string.maketrans("", 
        ""),mypunc)
#    jload[itweet].encode("utf-8").lower().translate(string.maketrans("", 
#            ""),mypunc)

    # -------- check for special case instances
    for i in xrange(len(wrd_spc)):
        sntsum[itweet] += snt_spc[i]*ttweet.count(wrd_spc[i])

    # -------- split the tweet
    ttweet = ttweet.split()

    # -------- get indices of found words and list of not found words
    #          (this would probably be cleaner using "pop"...)
    find, aind = [], []
    for iwrd in ttweet:
        fflag = 0
        for i, jwrd in enumerate(wrd_cln):
            if iwrd==jwrd:
                find.append(i)
                break
            if i==len(wrd_cln)-1: fflag=1
        if fflag==1: aind.append(iwrd)

    # -------- update the words dictionary
    for i in find: wrdcnt[wrd[i]] += 1

    # -------- get the sum and mean of found words
    meansnt = 0.0
    if len(find)>0:
        sntsum[itweet] += sum([snt[i] for i in find])
        meansnt = np.mean([snt[i] for i in find]) # this ignores wrd_spc's

    # -------- add to the dictionary of absent words (also ignores wrd_spcs's)
    for i in aind:
        if (max([ord(c) for c in i])>128) or ('http' in i):
            continue
        else:
            numflag = 0
            for j in '@_0123456789':
                if j in i: numflag=1
            if numflag==1: continue
        if i in absent:
            asum       = absent[i][0]*absent[i][1] + sntsum[itweet]
            atot       = absent[i][1] + len(find)
            absent[i]  = [asum/float(max(1,atot)),atot] # careful about /0
            wrdcnt[i] += 1
        else:
            absent[i] = [meansnt, len(find)]
            wrdcnt[i] = 1L

            #    if itweet in np.array(w)[np.array([51,221,264,306,316,621,678,796,810, 
            #                                       817])]:
"""
    print("")
    print("tweet #: {0}".format(itweet))
    print(jload[itweet])
    print(sntsum[itweet])
    print("tried",ttweet)
    print("found",[wrd_cln[i] for i in find])
    print("absent",aind)
    print("")
    time.sleep(2.5)
"""
"""
for i in w: print("%1.1f"%sntsum[i])
"""
"""
for i in absent.iterkeys(): print("{0}:{1:1.6f}".format(i, absent[i][0]))
"""

# -------- get the total occurance of all words
wrdtot = 0L
for i in wrdcnt.keys(): wrdtot += wrdcnt[i]

for i in sorted(wrdcnt.keys()):
    print("{0} {1} {2} {3}".format(i,wrdcnt[i],wrdtot, 
                                   float(wrdcnt[i])/float(wrdtot)))
