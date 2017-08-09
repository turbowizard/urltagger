import urllib2
from collections import Counter
import re
from bs4 import BeautifulSoup


#rules set for paragraph
def calcParaScore(block):
    parascore = 0
    if len(block) > 200 and len(block) < 1000:
        parascore += 1
    return parascore

def paraTest(score,blocks):
    predictedparas = []
    for block in blocks:
        parascore = calcParaScore(block)
        if parascore > score:
            predictedparas.append(block)
    return predictedparas

def cleanExtraSpaces(sample):
    return re.sub(' +', ' ', sample)

def stopWordFilter(con):
    #try except empty list nti
    global stopwordlist
    split = con.split()
    cleaned = ""
    for w in split:
        if w not in stopwordlist:
            cleaned+=w+' '
    return cleaned

#text clean up for analysis
def paraBlocksCleanUp(parablocks):
    pureparablocks = []
    for parablock in parablocks:
        parablock = parablock.lower()
        parablock = re.sub('[?,"!]','',parablock)
        parablock = re.sub("[']", '', parablock)
        parablock = re.sub('[.-]', ' ', parablock)
        parablock = stopWordFilter(parablock)
        pureparablocks.append(parablock)
    return pureparablocks


def getHTMLFromURL(url):
    return urllib2.urlopen(url)

#remove unusful chars
def doPreClean(blockstoclean):
    '''for i,dirtyblock in enumerate(blockstoclean):TypeError: 'unicode' object does not support item assignment
        dirtyblock[i] = re.sub('\n+', '', dirtyblock) string are immutable!!!
        dirtyblock[i] = re.sub('\t+', '', dirtyblock)
        dirtyblock[i] = cleanExtraSpaces(dirtyblock)
    return blockstoclean '''
    cleanblocks = []
    for dblock in blockstoclean:
        dblock = re.sub('\n+', '', dblock)
        dblock = re.sub('\t+', '', dblock)
        dblock = cleanExtraSpaces(dblock)
        cleanblocks.append(dblock)
    return cleanblocks


def extractBlocks(html):
    htmlblocks = []
    soup = BeautifulSoup(html, 'html.parser')
    htmlbody = soup.find('body') #might be more than 1
    for htmlblock in htmlbody.find_all('p'):
            a = htmlblock.text
            htmlblocks.append(a)
    return htmlblocks

def getCountLog():
    global countlog
    dictcon = []
    for c in countlog:
        dictcon.append(dict(c.most_common()))
    return dictcon

#more readable style
def showCountLog():
    countl = getCountLog()
    for d in countl:
        line = ""
        for i in d:
            line += i.encode('ascii', 'ignore')+' '+str(d[i])+'  ,'
        print line

def calcTagsFrom(twikedparablocks):
    global countlog
    tagholder = []
    artblockcount = Counter({})
    for tparablock in twikedparablocks:
        splittparablock = tparablock.split()
        splittparablockcount = Counter(splittparablock)
        artblockcount += splittparablockcount
        countlog.append(splittparablockcount)
    mostcom = artblockcount.most_common(5)
    for key, val in mostcom:
        tagholder.append(str(key))
    return tagholder

def initStopWordList():
    global stopwordlist
    with open('stopwords.txt') as f:
        for line in f:
            stopwordlist.append(line[:-1])


def getTags(url):
    html = getHTMLFromURL(url)
    htmlblocks = extractBlocks(html)
    cleanblocks = doPreClean(htmlblocks)
    parablocks = paraTest(0,cleanblocks) #returns suspected as paras ..paraqualification
    initStopWordList() #used in paraBlocksCleanUp
    twikedparablocks = paraBlocksCleanUp(parablocks)
    return calcTagsFrom(twikedparablocks)

stopwordlist = []
countlog = []