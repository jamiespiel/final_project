import requests
import json
import secrets
import nyt_info
import sqlite3

def makeRequestsUsingCache(url, ident):
    ident = ident
    try:
        cache_file1 = open('cache-nyt.json', 'r')
        cache_contents1 = cache_file1.read()
        CACHE_DICTION1 = json.loads(cache_contents1)
        #cache_file1.close()
    except:
        CACHE_DICTION1 = {}
    if ident in CACHE_DICTION1:
        return CACHE_DICTION1[ident]
    else:
        response = requests.get(url)
        CACHE_DICTION1[ident] = response.text
        dumpJSONCache = json.dumps(CACHE_DICTION1)
        f1 = open('cache-nyt.json', 'w')
        f1 = f1.write(dumpJSONCache)
        #f1.close()
    return CACHE_DICTION1[ident]

def nytRequest(ident):
    base_url = 'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key='
    my_key = nyt_info.api_key
    url = base_url + my_key
    response = makeRequestsUsingCache(url, ident)
    return response

def parseJSON(listOfCities):
    for city in listOfCities:
        nytRequest(city)

    fn = 'cache-nyt.json'
    with open(fn, 'r') as f:
        data = json.load(f)

    articleInfo = []
    for c in data:
        #print(json.loads(data[c])['results'])
        for result in json.loads(data[c])['results']:
            indivResult = {}
            indivResult['city'] = c
            indivResult['title'] = result['title']
            indivResult['views'] = result['views']
            indivResult['section'] = result['section']
            #print(indivResult)
            articleInfo.append(indivResult)
    return articleInfo

def create_table():
    #filename = 'cache-nyt.json'
    conn = sqlite3.connect('NYT.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS NYT')
    conn.commit()
    cur.execute('CREATE TABLE NYT (city TEXT, title TEXT, views INTEGER, section TEXT)')
    conn.commit()
    
    # nyt_file = open('cache-nyt.json','r')
    # contents = nyt_file.read()
    # nyt_file.close()
    # nyt_data = json.loads(contents)
    #print("num articles: " + str(len(nyt_data)))

def insert_data():
    create_table()
    conn = sqlite3.connect('NYT.sqlite')
    cur = conn.cursor()

    data = parseJSON(['New York', 'Ann Arbor', 'Miami', 'Los Angeles', 'Austin'])

    for article in data:
        info = list(article.values())
        _city = info[0]
        _title = info[1]
        _views = info[2]
        _section = info[3]
        cur.execute('INSERT INTO NYT (city, title, views, section) VALUES (?, ?, ?, ?)', (_city, _title, _views, _section))

    conn.commit()

insert_data()



#print(parseJSON(['New York', 'Ann Arbor', 'Miami', 'Los Angeles', 'Austin']))