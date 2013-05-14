import sys, json, string

# -------- utilities
twtfile = open(sys.argv[1])
tweets  = twtfile.readlines()
ntweets = len(tweets)
mypunc  = '!"$%&\'()*+,-./:;<=>?[\\]^`{|}~'
hdict   = {} # hashtag dictionary



# -------- make sure that the tweet has text
def checktext(tweet):
    try:
        text = tweet[u'text']
    except:
        tweet = None
    return tweet


# -------- parse tweets with json
jload = [checktext(json.loads(i)) for i in tweets]


# -------- loop through tweets
for itweet in xrange(ntweets):
    # -------- grab the tweet
    ttweet = jload[itweet]

    # -------- skip if no text
    if ttweet == None: continue

    # -------- check for hashtags
    numhash = len(ttweet[u'entities'][u'hashtags'])
    if numhash == 0: continue

    # -------- get the hashtags
    hashs = []
    for i in xrange(numhash):
        text = ttweet[u'entities'][u'hashtags'][i][u'text'].encode("utf-8")
#        text = text.encode("ascii", 
#            "ignore").encode("utf-8").lower().translate(string.maketrans("", 
#            ""),mypunc)
        hashs.append(text)

    # -------- get hashtags
    for iwrd in hashs:
 #       if iwrd in ['_','rt','__']: continue

        if (len(iwrd)>1):
            if iwrd in hdict:
                hdict[iwrd] += 1l
            else:
                hdict[iwrd] = 1l


# -------- top 10 keys
def argsort(x):
    return sorted(range(len(x)),key=x.__getitem__)

hashtag, value = [], []
for i in hdict.keys():
    hashtag.append(i)
    value.append(hdict[i])
sind = argsort(value)[::-1]
for i in sind[0:10]: print("{0} {1}".format(hashtag[i],float(value[i])))
    
