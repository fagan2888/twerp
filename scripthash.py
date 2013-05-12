import sys, json, string, time, numpy as np

start = 0
end = 1000

# -------- utilities
twtfile = open('output.txt')
#twtfile = open('output2_fed.txt')
tweets  = twtfile.readlines()
#tweets  = tweets[start:end]
ntweets = len(tweets)
mypunc  = '!"$%&\'()*+,-./:;<=>?[\\]^`{|}~'
hdict   = {} # hashtag dictionary



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
##    if itweet % 500 == 0:
##        print('{0} out of {1} tweets'.format(itweet,ntweets-1))

    # -------- load the tweet and encode
    ttweet = \
    jload[itweet].encode("ascii", 
        "ignore").encode("utf-8").lower().translate(string.maketrans("", 
        ""),mypunc)

    # -------- split the tweet
    ttweet = ttweet.split()

    # -------- get hashtags
    for iwrd in ttweet:
        if iwrd in ['#_','#rt','#__']: continue

        if (iwrd[0]=='#') and (len(iwrd)>1):
            if iwrd in hdict:
                hdict[iwrd] += 1l
            else:
                hdict[iwrd] = 1l
            """
            print("")
            print("tweet #: {0}".format(itweet))
            print(jload[itweet])
            print("hashtag:",iwrd)
            print("")
            time.sleep(2.5)
            """

