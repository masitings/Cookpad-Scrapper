import json
import random
import uuid
import time
import requests
from bs4 import BeautifulSoup as soup
from urllib.error import URLError, HTTPError

def getApiKey():
    openKey = open("scrapperApi.txt", "r")
    readKey = openKey.read()
    apiKey = readKey.split("\n")
    randomApi = apiKey.choice(proxy)
    return str(randomApi)

def getUa():
    openUa = open("ua.txt", "r")
    readUa = openUa.read()
    ua = readUa.split("|")
    randomUa = random.choice(ua)
    return randomUa

def randCategory(array):
    openProxy = open("kategori.txt", "r")
    readProxy = openProxy.read()
    proxy = readProxy.split("|")
    return proxy[array]


def loopfunction(search, page = 0):

    if (page > 1):
        url = 'https://cookpad.com/id/cari/'+ str(search) +'?page=' + str(page)
    else:
        url = 'https://cookpad.com/id/cari/' + str(search)
    
    myUrl = 'http://api.scraperapi.com?api_key=' + getApiKey() + '&url=' + url

    urList = []
    recipeId = uuid.uuid1()
    fOpen = open("recipe/" + str(search) + ".txt", "a+")
    fError = open("log/"+ str(search) +".txt", "a+")

    try: 
        uClient = requests.get(myUrl)
        pageHtml = uClient.text
        pageSoup = soup(pageHtml, "html.parser")
        mainContainer = pageSoup.find('div', {"id":"main_contents"})
        if mainContainer is not None:
            recipeUl = mainContainer.find('ul', {"class":"recipe-list"})
            recipeList = recipeUl.find_all('li', {"class":"ranked-list__item"})

            for listRecipe in recipeList:
                findAhref = listRecipe.find('a', {"class": "media"})
                if findAhref is not None:
                    fixUrl = 'https://cookpad.com' + findAhref['href']
                    fOpen.write(fixUrl.strip() + "\n")
            print("Category : " + str(search) + " | Halaman : " + str(page))
        else:
            print('Main Container tidak ditemukan : ' + str(page))
            fError.write(str(page) + ",")

    except HTTPError as e:
        print('Kode Error: ', e.code)
        fError.write(str(page) + ",")

    except URLError as e:
        print('Alasan Error : ', e.reason)
        fError.write(str(page) + ",")


# loopfunction()
for i in range(0, 120):
    for a in range (0, 18):
        loopfunction(randCategory(i), a)