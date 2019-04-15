import requests
import json
import secrets
import nyt_info

def makeRequestsUsingCache(url, ident): #params, headers, ident
    ident = ident
    try:
        cache_file1 = open('cache-nyt.json', 'r')
        cache_contents1 = cache_file1.read()
        CACHE_DICTION1 = json.loads(cache_contents1)
        cache_file1.close()
    except:
        CACHE_DICTION1 = {}
    if ident in CACHE_DICTION1:
        return CACHE_DICTION1[ident]
    else:
        response = requests.get(url) #params = params, headers = headers
        CACHE_DICTION1[ident] = response.text
        dumpJSONCache = json.dumps(CACHE_DICTION1)
        f1 = open('cache-nyt.json', 'w')
        f1 = f1.write(dumpJSONCache)
        f1.close()
    return CACHE_DICTION1[ident]

def nytRequest(ident):
    # header = 
    # params = {}
    # params['limit'] = 
    # params
    base_url = 'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key='
    my_key = nyt_info.api_key
    url = base_url + my_key
    response = makeRequestsUsingCache(url, ident) # params = params, headers = headers
    #response = requests.get(url)
    #data = json.loads(response)
    # l_ = []
    # for x in json.loads(response):
    #     print(x)
    return response

print(nytRequest('trump'))