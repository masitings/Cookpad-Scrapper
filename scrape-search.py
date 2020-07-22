import urllib.request
import json
import uuid
import time
from bs4 import BeautifulSoup as soup
from urllib.error import URLError, HTTPError



def loopfunction(Url = 0):
    if Url is not 0:
        myUrl = Url
    else:
        myUrl = 'https://cookpad.com/id/cari/resep%20masakan%20indonesia'
    
    req = urllib.request.Request(
        myUrl, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
    )

    urList = []
    recipeId = uuid.uuid1()
    fOpen = open("recipe.txt", "a+")

    try: 
        uClient = urllib.request.urlopen(req)
        pageHtml = uClient.read()
        uClient.close()
        pageSoup = soup(pageHtml, "html.parser")

        mainContainer = pageSoup.find('div', {"id":"main_contents"})
        recipeUl = mainContainer.find('ul', {"class":"recipe-list"})
        recipeList = recipeUl.find_all('li', {"class":"ranked-list__item"})

        for listRecipe in recipeList:
            findAhref = listRecipe.find('a', {"class": "media"})
            if findAhref is not None:
                fixUrl = 'https://cookpad.com' + findAhref['href']
                fOpen.write(fixUrl.strip() + "\n")
                # urList.append()
        paginate = mainContainer.find('div', {"class": "pagination"})
        nextUrl = paginate.find('a', {"class": "pagination__next"})
        urlPaginate = 'https://cookpad.com' + nextUrl['href']
        if Url is not 0:
            print("Success Scrape Paginate : " + urlPaginate)
        else:
            print("Success Scrape First Page")
        # Sleep Time
        time.sleep(5)
        # Then Continue
        loopfunction(urlPaginate)
    except HTTPError as e:
        print('Error code: ', e.code)
        time.sleep(5)
        if Url is not 0:
            loopfunction(Url)
        else:
            loopfunction()
    except URLError as e:
        print('Reason: ', e.reason)
        time.sleep(5)
        if Url is not 0:
            loopfunction(Url)
        else:
            loopfunction()
    
    
loopfunction()

