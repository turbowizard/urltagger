from urltagger import urltagger
import turbotagger #

from test import testurl
url = testurl
result = urltagger(url,turbotagger) # for default processing
print result.url
print result.sum()