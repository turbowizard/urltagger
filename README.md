# urltagger
"url tagger" is a tool for web page content analysis written in Python2.</br>
This tool was created to retrive "tags" for any given url</br>
used for content comparison and suggestions.</br>
"tags" are lables/keyword used to describe textual content.</be>
This also can be used for data gathering.</br>
</br></br>
Logics:</br>
    input url</br>
    get source</br>
    extract blocks</br>
    clean blocks</br>
    block qualification</br>
    pre-processing</br>
    analysis</br></br>

Example:</br>
    testurl = "https://en.wikipedia.org/wiki/Python_(programming_language)"</br>
    ['python', 'are', 'language', 'with', 'c']</be></br>

Plug and play:</br>
    download or clone https://github.com/turbowizard/urltagger</br>
    edit test.py</br>
        set url for testurl var</br>
        save file </br>
     from console: python main.py