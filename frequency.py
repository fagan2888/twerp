import sys, json, string, time

# -------- utilities
twtfile = open(sys.argv[1])
tweets  = twtfile.readlines()
ntweets = len(tweets)
mypunc  = '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~'
wrdcnt  = {}


# -------- make sure that the tweet has text
def checktext(tweet):
    try:
        text = tweet[u'text']
    except:
        text = None
    return text


# -------- parse tweets with json
jload = [checktext(json.loads(i)) for i in tweets]



# -------- loop through tweets
for itweet in xrange(ntweets):
    # -------- skip if no text
    if jload[itweet] == None: continue

    # -------- load the tweet and encode
    ttweet = \
    jload[itweet].encode("ascii", 
        "ignore").encode("utf-8").lower().translate(string.maketrans("", 
        ""),mypunc)

    # -------- split the tweet
    ttweet = ttweet.split()

    # -------- get indices of found words and list of not found words
    for iwrd in ttweet:
        if (max([ord(c) for c in iwrd])>128) or ('http' in iwrd):
            continue
        else:
            numflag = 0
            for j in '@_0123456789':
                if j in iwrd: numflag=1
            if numflag==1: continue
        if iwrd in wrdcnt:
            wrdcnt[iwrd] += 1L
        else:
            wrdcnt[iwrd] = 1L


# word frequency
wrdtot = 0L
for i in wrdcnt.keys(): wrdtot += wrdcnt[i]

for i in sorted(wrdcnt.keys()):
    print("{0} {1}".format(i,float(wrdcnt[i])/float(wrdtot)))

