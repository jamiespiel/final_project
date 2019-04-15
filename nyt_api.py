import requests
import json
import secrets
#import api_info

def makeRequestsUsingCache(url, params, headers, ident):
	try:
		cache_file1 = open('cache-nyt.json', 'r')
		cache_contents1 = cache_file1.read()
		CACHE_DICTION1 = json.loads(cache_contents1)
		cache_file1.close()
	except:
		CACHE_DICTION1 = {}
		response = requests.get("https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=JKiZea6whSW2E2AfOcJm1UgZHaCTrG2I")
	if ident in CACHE_DICTION1:
		return CACHE_DICTION1[ident]
	else:
		response = requests.get(url, params = params, headers = headers)
		CACHE_DICTION1[ident] = response.text
		dumpJSONCache = json.dumps(CACHE_DICTION1)
		f1 = open('cache-nyt.json', 'w')
		f1 = f1.write(dumpJSONCache)
		f1.close()
	return CACHE_DICTION1[ident]

def nytRequest(baseURL, params = {}):
    req = requests.Request(method = 'GET', url = baseURL, params = sorted(params.items()))
    prepped = req.prepare()
    fullURL = prepped.url
  
    if fullURL not in CACHE_DICTION1:
        response = requests.Session().send(prepped)
        CACHE_DICTION1[fullURL] = response.text
        
        cache_file = open('cache-nyt.json', 'w')
        cache_file.write(json.dumps(CACHE_DICTION1))
        cache_file.close()
    
    return CACHE_DICTION1[fullURL]
