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
    #needs some implementation for retriving stop list
    stopwords = ['to','it','if','the','in','is','all','go','an','a','what','will','have','that',
                 'by','as','and','or','for','from','of']
    #print con
    split = con.split()
    cleaned = ""
    for w in split:
        if w not in stopwords:
            cleaned+=w+' '
    #print cleaned
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

def calcTagsFrom(twikedparablocks):
    tagholder = []
    artblockcount = Counter({})
    for tparablock in twikedparablocks:
        a = tparablock.split()
        artblockcount += Counter(a)
    mostcom = artblockcount.most_common(5)
    for key, val in mostcom:
        tagholder.append(str(key))
    return tagholder

def getTags(url):
    tagstoreturn = []
    html = getHTMLFromURL(url)
    htmlblocks = extractBlocks(html)
    cleanblocks = doPreClean(htmlblocks)
    parablocks = paraTest(0,cleanblocks) #returns suspected as paras ..paraqualification
    twikedparablocks = paraBlocksCleanUp(parablocks)
    return calcTagsFrom(twikedparablocks)
