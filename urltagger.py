import urllib2

class urltagger():


    def __init__(self,url,processor):
        self.url = url
        self.processor = processor
        html = urltagger.getHTMLFromURL(url)
        self.summery = {}
        self.summery.update(self.process(html,processor.callorder)) #import and set process order


    def process(self,html,flow):
        summery = {}
        result = html
        #result['data'] holds data for next func
        for stage in flow:
            stagefunction = getattr(self.processor, stage)
            result = stagefunction(result)
            a = result['data']
            del result['data']
            summery.update(result)
            result = a
        return summery

    def sum(self):
        for i in self.summery:
            print i,self.summery[i]

    @staticmethod
    def getHTMLFromURL(url):
        return urllib2.urlopen(url)

