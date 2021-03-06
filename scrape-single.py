import requests
import random
import json
import os
from bs4 import BeautifulSoup as soup
from slugify import slugify
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

# def getUa():
#     openUa = open("ua.txt", "r")
#     readUa = openUa.read()
#     ua = readUa.split("|")
#     randomUa = random.choice(ua)
#     return randomUa

def getApiKey():
    openKey = open("tmp/api.txt", "r")
    readKey = openKey.read()
    apiKey = readKey.split("\n")
    randomApi = random.choice(apiKey)
    return str(randomApi)

def randCategory(array):
    openProxy = open("tmp/kategori.txt", "r")
    readProxy = openProxy.read()
    proxy = readProxy.split("|")
    return proxy[array]

def getCategory(array):
    openProxy = open("tmp/kategori.txt", "r")
    readProxy = openProxy.read()
    proxy = readProxy.split("|")
    return proxy[array]

def getSingle(url, category):
    myUrl = 'http://api.scraperapi.com?api_key=' + getApiKey() + '&url=' + url
    try:
        uClient = requests.get(myUrl)
        pageHtml = uClient.text
        pageSoup = soup(pageHtml, "html.parser")
        # save files
        bahan = []
        langkah = []

        # get title and main image
        
        if pageSoup.h1 is not None:
            recipeTitle = pageSoup.h1.string.strip()
            images = pageSoup.find('div', {"class":"tofu_image"})
            if images is not None:
                # get ingredient
                mainImage = images.find('img')['src']
                mainIngridient = pageSoup.find('section', {"id":"ingredients"})
                ingredientList = mainIngridient.find('div', {"class":"ingredient-list"})
                ingredients = ingredientList.find_all('li', {"class":"ingredient"})
                for ingredient in ingredients:
                    ingWrap = ingredient.find('div', {"itemprop":"ingredients"})
                    Qty = ingWrap.find('bdi', {"class":"ingredient__quantity"}).text.strip()
                    if Qty:
                        bahan.append(ingWrap.text.strip())
                mainStep = pageSoup.find('section', {"id": "steps"})
                listStep = mainStep.find_all('li', {"class":"step"})
                for step in listStep:
                    steps = {}
                    textStep = step.find('div', {"itemprop": "recipeInstructions"}).text.strip()
                    langkah.append(textStep)

                urlFilename = PurePosixPath(
                    unquote(
                        urlparse(
                            url
                        ).path
                    )
                ).parts[3]

                filename = urlFilename + '.json'
                catName = category.replace('.txt', '')
                pathFinder = 'results/' + catName + '/' + filename

                os.makedirs(os.path.dirname(pathFinder), exist_ok=True)
                dataJson = {"title": recipeTitle, "image": mainImage,"bahan": bahan, "langkah": langkah}
                with open(pathFinder, "a+") as writeJson:
                    json.dump(dataJson, writeJson, ensure_ascii=False)
                    print('Category : ' + catName)
                    print('Filename : ' + filename)
                    print('------------------------')
            else:
                errorFile = open('error_single.log', "a+")
                errorFile.write(myUrl + "\n")

                print('Error getting image, may caused by proxy')
                print('------------------------')
        else:
            errorFile = open('error_single.log', "a+")
            errorFile.write(myUrl + "\n")

            print('Error Getting Title Recipe')
            print('------------------------')
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def looping():
    a = []
    for i in range(1, 115):
        category = randCategory(i) + '.txt'
        catOpen = open('recipe/' + category, 'r')
        readCat = catOpen.read()
        cat = readCat.split("\n")
        for url in cat:
            if url:
                getSingle(url, category)
looping()