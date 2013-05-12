import sys, json, string, time, numpy as np

# load tabel from http://answers.google.com/answers/threadview?id=149284
stcoords = {
    'Alabama': ['AL', [85., 88.], [30., 35.]],
    'Alaska': ['AK', [130., 187.], [55., 72.]],
    'Arizona': ['AZ', [109., 115.], [31., 37.]],
    'Arkansas': ['AR', [90., 95.], [33., 37.]],
    'California': ['CA', [114., 124.], [33., 42.]],
    'Colorado': ['CO', [102., 109.], [37., 41.]],
    'Connecticut': ['CT', [72., 74.], [41., 42.]],
    'Delaware': ['DE', [75., 76.], [38., 40.]],
    'Florida': ['FL', [80., 88.], [25., 31.]],
    'Georgia': ['GA', [81., 86.], [31., 35.]],
    'Hawaii': ['HI', [155., 162.], [17., 23.]],
    'Idaho': ['ID', [111., 117.], [42., 49.]],
    'Illinois': ['IL', [88., 92.], [37., 43.]],
    'Indiana': ['IN', [85., 88.], [38., 42.]],
    'Iowa': ['IA', [89., 97.], [41., 44.]],
    'Kansas': ['KS', [95., 102.], [37., 40.]],
    'Kentucky': ['KY', [82., 90.], [37., 39.]],
    'Louisiana': ['LA', [89., 94.], [29., 33.]],
    'Maine': ['ME', [67., 71.], [43., 47.]],
    'Maryland': ['MD', [75., 80.], [38., 40.]],
    'Massachusetts': ['MA', [70., 74.], [41., 43.]],
    'Michigan': ['MI', [82., 91.], [42., 48.]],
    'Minnesota': ['MN', [90., 97.], [44., 49.]],
    'Mississippi': ['MS', [88., 92.], [30., 35.]],
    'Missouri': ['MO', [89., 96.], [36., 41.]],
    'Montana': ['MT', [104., 116.], [44., 49.]],
    'Nebraska': ['NE', [95., 104.], [40., 43.]],
    'Nevada': ['NV', [114., 120.], [35., 42.]],
    'New Hampshire': ['NH', [71., 73.], [43., 45.]],
    'New Jersey': ['NJ', [74., 76.], [39., 41.]],
    'New Mexico': ['NM', [103., 109.], [31., 37.]],
    'New York': ['NY', [72., 80.], [40., 45.]],
    'North Carolina': ['NC', [76., 84.], [34., 36.]],
    'North Dakota': ['ND', [97., 104.], [46., 49.]],
    'Ohio': ['OH', [81., 85.], [38., 42.]],
    'Oklahoma': ['OK', [94., 103.], [34., 37.]],
    'Oregon': ['OR', [117., 125.], [42., 46.]],
    'Pennsylvania': ['PA', [75., 81.], [40., 42.]],
    'Rhode Island': ['RI', [71., 72.], [41., 42.]],
    'South Carolina': ['SC', [78., 83.], [32., 35.]],
    'South Dakota': ['SD', [98., 104.], [42., 46.]],
    'Tennessee': ['TN', [82., 90.], [35., 37.]],
    'Texas': ['TX', [94., 107.], [26., 37.]],
    'Utah': ['UT', [109., 114.], [37., 42.]],
    'Vermont': ['VT', [71., 73.], [43., 45.]],
    'Virginia': ['VA', [75., 84.], [37., 40.]],
    'Washington': ['WA', [117., 125.], [46., 49.]],
    'West Virginia': ['WV', [78., 83.], [37., 41.]],
    'Wisconsin': ['WI', [87., 93.], [43., 47.]],
    'Wyoming': ['WY', [104., 111.], [41., 45.]]
}


'''

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
    """
    for i in xrange(len(wrd_spc)):
        sntsum[itweet] += snt_spc[i]*ttweet.count(wrd_spc[i])
    """

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
'''
