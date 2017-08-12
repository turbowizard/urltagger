import re
from collections import Counter
from bs4 import BeautifulSoup

'''
set of functions to extract tags from html
'''

callorder = ['extractBlocks','htmlBlocksCleanUp','paraTest',
                                        'paraBlocksCleanUp','calcTagsFrom']

stopwordlist = ["as","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","aint","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","arent","around","as","aside","ask","asking","associated","at","available","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","cmon","cs","came","can","cant","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldnt","course","currently","definitely","described","despite","did","didnt","different","do","does","doesnt","doing","dont","done","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadnt","happens","hardly","has","hasnt","have","havent","having","he","hes","hello","help","hence","her","here","heres","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","id","ill","im","ive","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isnt","it","itd","itll","its","its","itself","just","keep","keeps","kept","know","knows","known","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldnt","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","ts","take","taken","tell","tends","th","than","thank","thanks","thanx","that","thats","thats","the","their","theirs","them","themselves","then","thence","there","theres","thereafter","thereby","therefore","therein","theres","thereupon","these","they","theyd","theyll","theyre","theyve","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","wasnt","way","we","wed","well","were","weve","welcome","well","went","were","werent","what","whats","whatever","when","whence","whenever","where","wheres","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","whos","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","wont","wonder","would","would","wouldnt","yes","yet","you","youd","youll","youre","youve","your","yours","yourself","yourselves","zero"]


def extractBlocks(html):
    '''
    find possible html elements containing paragraph
    '''
    htmlblocks = []
    soup = BeautifulSoup(html, 'html.parser')
    htmlbody = soup.find('body') #might be more than 1
    for htmlblock in htmlbody.find_all('p'):
            a = htmlblock.text
            htmlblocks.append(a)
    return {'data': htmlblocks, 'blocklen': len(htmlblocks)}

def htmlBlocksCleanUp(blockstoclean):
    '''
    soft clean , to readable form
    '''
    cleanblocks = []
    for dblock in blockstoclean:
        dblock = re.sub('\n+', '', dblock)
        dblock = re.sub('\t+', '', dblock)
        dblock = cleanExtraSpaces(dblock)
        cleanblocks.append(dblock)
    return {'data': cleanblocks}

#helper
def cleanExtraSpaces(sample):
    return re.sub(' +', ' ', sample)

def paraTest(blocks,score=0):
    '''
    is this block of text is a paragraph?
    '''
    predictedparas = []
    for block in blocks:
        parascore = calcParaScore(block)
        if parascore > score:
            predictedparas.append(block)
    return {'data': predictedparas , 'paraok':len(predictedparas)}

#helper
def calcParaScore(block):
    parascore = 0
    if len(block) > 200 and len(block) < 1000:
        parascore += 1
    return parascore

def paraBlocksCleanUp(parablocks):
    '''
    hard clean to remove char combinations might not add value
    '''
    pureparablocks = []
    for parablock in parablocks:
        cparablock = paraBlockFilter(parablock)
        pureparablocks.append(cparablock)
    return {'data': pureparablocks}

#helper
def paraBlockFilter(parablock):
    cparablock = parablock.lower()
    cparablock = re.sub('[?,"!=;%:+*<>/)(]', '', cparablock)
    cparablock = re.sub("[']", '', cparablock)  # hacks!!!
    cparablock = re.sub("(\[)\d*]", " ", cparablock)
    cparablock = re.sub('\. ', ' ', cparablock)
    cparablock = stopWordFilter(cparablock)
    return cparablock

#helper
def stopWordFilter(con):
    global stopwordlist
    split = con.split()
    cleaned = ""
    for w in split:
        if w not in stopwordlist:
            cleaned+=w+' ' #i know
    return cleaned

def calcTagsFrom(twikedparablocks):
    '''
    1 way to make tags for text using keywords
    '''
    tagholder = []
    artblockcount = Counter({})
    for tparablock in twikedparablocks:
        splittparablock = tparablock.split()
        splittparablockcount = Counter(splittparablock)
        artblockcount += splittparablockcount
    mostcom = artblockcount.most_common(7)
    for key, val in mostcom:
        tagholder.append(str(key))
    return {'data': tagholder, 'tags': tagholder}
