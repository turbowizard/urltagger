import urltagger
from test import testurl
url = testurl
print url
urltags = []
print urltagger.getTags(url)
print urltagger.showCountLog()