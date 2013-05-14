import sys, json, string

# load table from http://answers.google.com/answers/threadview?id=149284
stcoords = {'Alabama': ['AL', [85., 88.], [30., 35.], 0L, 0L],'Alaska': ['AK', [130., 187.], [55., 72.], 0L, 0L],'Arizona': ['AZ', [109., 115.], [31., 37.], 0L, 0L],'Arkansas': ['AR', [90., 95.], [33., 37.], 0L, 0L],'California': ['CA', [114., 124.], [33., 42.], 0L, 0L],'Colorado': ['CO', [102., 109.], [37., 41.], 0L, 0L],'Connecticut': ['CT', [72., 74.], [41., 42.], 0L, 0L],'Delaware': ['DE', [75., 76.], [38., 40.], 0L, 0L],'Florida': ['FL', [80., 88.], [25., 31.], 0L, 0L],'Georgia': ['GA', [81., 86.], [31., 35.], 0L, 0L],'Hawaii': ['HI', [155., 162.], [17., 23.], 0L, 0L],'Idaho': ['ID', [111., 117.], [42., 49.], 0L, 0L],'Illinois': ['IL', [88., 92.], [37., 43.], 0L, 0L],'Indiana': ['IN', [85., 88.], [38., 42.], 0L, 0L],'Iowa': ['IA', [89., 97.], [41., 44.], 0L, 0L],'Kansas': ['KS', [95., 102.], [37., 40.], 0L, 0L],'Kentucky': ['KY', [82., 90.], [37., 39.], 0L, 0L],'Louisiana': ['LA', [89., 94.], [29., 33.], 0L, 0L],'Maine': ['ME', [67., 71.], [43., 47.], 0L, 0L],'Maryland': ['MD', [75., 80.], [38., 40.], 0L, 0L],'Massachusetts': ['MA', [70., 74.], [41., 43.], 0L, 0L],'Michigan': ['MI', [82., 91.], [42., 48.], 0L, 0L],'Minnesota': ['MN', [90., 97.], [44., 49.], 0L, 0L],'Mississippi': ['MS', [88., 92.], [30., 35.], 0L, 0L],'Missouri': ['MO', [89., 96.], [36., 41.], 0L, 0L],'Montana': ['MT', [104., 116.], [44., 49.], 0L, 0L],'Nebraska': ['NE', [95., 104.], [40., 43.], 0L, 0L],'Nevada': ['NV', [114., 120.], [35., 42.], 0L, 0L],'New Hampshire': ['NH', [71., 73.], [43., 45.], 0L, 0L],'New Jersey': ['NJ', [74., 76.], [39., 41.], 0L, 0L],'New Mexico': ['NM', [103., 109.], [31., 37.], 0L, 0L],'New York': ['NY', [72., 80.], [40., 45.], 0L, 0L],'North Carolina': ['NC', [76., 84.], [34., 36.], 0L, 0L],'North Dakota': ['ND', [97., 104.], [46., 49.], 0L, 0L],'Ohio': ['OH', [81., 85.], [38., 42.], 0L, 0L],'Oklahoma': ['OK', [94., 103.], [34., 37.], 0L, 0L],'Oregon': ['OR', [117., 125.], [42., 46.], 0L, 0L],'Pennsylvania': ['PA', [75., 81.], [40., 42.], 0L, 0L],'Rhode Island': ['RI', [71., 72.], [41., 42.], 0L, 0L],'South Carolina': ['SC', [78., 83.], [32., 35.], 0L, 0L],'South Dakota': ['SD', [98., 104.], [42., 46.], 0L, 0L],'Tennessee': ['TN', [82., 90.], [35., 37.], 0L, 0L],'Texas': ['TX', [94., 107.], [26., 37.], 0L, 0L],'Utah': ['UT', [109., 114.], [37., 42.], 0L, 0L],'Vermont': ['VT', [71., 73.], [43., 45.], 0L, 0L],'Virginia': ['VA', [75., 84.], [37., 40.], 0L, 0L],'Washington': ['WA', [117., 125.], [46., 49.], 0L, 0L],'West Virginia': ['WV', [78., 83.], [37., 41.], 0L, 0L],'Wisconsin': ['WI', [87., 93.], [43., 47.], 0L, 0L],'Wyoming': ['WY', [104., 111.], [41., 45.], 0L, 0L]}

# -------- utilities
twtfile = open(sys.argv[2])
tweets  = twtfile.readlines()
ntweets = len(tweets)
mypunc  = '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~'

# -------- read the sentiment file and initialize the tweet sentiment sum
wrd, snt = [], []
sntfile  = open(sys.argv[1])
for line in sntfile:
    twrd, tsnt = line.split("\t")
    wrd.append(twrd)
    snt.append(int(tsnt))
sntfile.close()
wrd, snt = list(wrd),list(snt)
nsnt     = len(snt)
sntsum   = [0.0 for i in xrange(ntweets)]

# -------- strip words of punctuation
wrd_cln = [i.translate(string.maketrans("",""), mypunc) for i in wrd]

# -------- make special cases
wrd_spc, snt_spc = [], []
for i in xrange(len(wrd_cln)):
    if len(wrd_cln[i].split())>1:
        wrd_spc.append(wrd_cln[i])
        snt_spc.append(snt[i])

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
    # -------- access the tweet
    ttweet = jload[itweet]

    # -------- skip if no text
    if ttweet == None: continue

    # -------- check if there are coordinates
    try:
        geo  = ttweet[u'geo']
        if geo!=None:
            tlon = geo[u'coordinates'][1]
            tlat = geo[u'coordinates'][0]
        else:
            continue
    except:
        continue

    # -------- check if it's in the northern hemisphere
    if tlat < 0.0: continue
    if tlon > 0.0: continue

    tlon = abs(tlon)

    # -------- loop through states
    inUS = 0
    for state in stcoords.keys():
        slon_min = stcoords[state][1][0]
        slon_max = stcoords[state][1][1]
        slat_min = stcoords[state][2][0]
        slat_max = stcoords[state][2][1]

        if (tlon>=slon_min) and (tlon<slon_max) and \
                (tlat>=slat_min) and (tlat<slat_max):
            tstate = state
            inUS = 1
            break

    if inUS==0: continue

    # -------- congratulations, you have a tweet in a state.  get sentiment.
    ttext = ttweet[u'text'].encode("ascii", 
        "ignore").encode("utf-8").lower().translate(string.maketrans("", 
        ""),mypunc)

    # -------- check for special case instances
    for i in xrange(len(wrd_spc)):
        sntsum[itweet] += snt_spc[i]*ttext.count(wrd_spc[i])

    # -------- split the tweet
    ttext = ttext.split()

    # -------- get indices of found words and list of not found words
    find = []
    for iwrd in ttext:
        for i, jwrd in enumerate(wrd_cln):
            if iwrd==jwrd:
                find.append(i)
                break

    # -------- no words found, don't consider this tweet
    if len(find)==0: continue

    # -------- get the sum and mean of found words
    meansnt = 0.0
    sntsum[itweet] += sum([snt[i] for i in find])

    # -------- increment the counter of tweets from this state, add sentiment
    stcoords[tstate][3] += sntsum[itweet]
    stcoords[tstate][4] += 1L

# -------- get the average tweet sentiment in a given state and print the max
abbrv, avgsnt = [], []
for i in stcoords.keys():
    totsnt = stcoords[i][3]
    tottwt = stcoords[i][4]
    if tottwt > 0:
        avg = float(totsnt)/float(tottwt)
        abbrv.append(stcoords[i][0])
        avgsnt.append(avg)

m     = max(avgsnt)
index = [i for i, j in enumerate(avgsnt) if j == m]

print(abbrv[index[0]])

