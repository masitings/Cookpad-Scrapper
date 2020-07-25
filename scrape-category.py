import json
import random
import uuid
import time
import requests
import re
from bs4 import BeautifulSoup as soup
from urllib.error import URLError, HTTPError

def getApiKey():
    openKey = open("tmp/api.txt", "r")
    readKey = openKey.read()
    apiKey = readKey.split("\n")
    randomApi = random.choice(apiKey)
    return str(randomApi)

def getCategory():
    url = 'https://cookpad.com/id/search_categories'
    myUrl = 'http://api.scraperapi.com?api_key=' + getApiKey() + '&url=' + url
    fOpen = open('tmp/kategori.txt', "a+")
    try:
        uClient = requests.get(myUrl)
        pageHtml = uClient.text
        pageSoup = soup(pageHtml, "html.parser")

        mainCard = pageSoup.find('div', {"class":"card p-5"})
        childCard = mainCard.find_all('div', {"class":"flex flex-wrap links"})
        for childs in childCard:
            childDiv = childs.find_all('div', {"class":"flex flex-col mb-3 mt-2 md:w-1/3 p-3 w-full"})
            for divider in childDiv:
                divs = divider.find_all('a', {"data-click-log": re.compile(r".*")})
                for ivs in divs:
                    catTitle = ivs.text.strip()
                    rewrite = catTitle.lower().replace(' ', '-')
                    fOpen.write(rewrite + "|")
                    print(rewrite)
    except HTTPError as e:
        print("Kode Error :", e.code)
    except URLError as e:
        print('Alasan Error : ', e.reason)
        fError.write(str(page) + ",")

getCategory()