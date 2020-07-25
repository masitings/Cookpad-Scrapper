import requests
import random
import json
import os
from bs4 import BeautifulSoup as soup
from slugify import slugify
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

def getUa():
    openUa = open("ua.txt", "r")
    readUa = openUa.read()
    ua = readUa.split("|")
    randomUa = random.choice(ua)
    return randomUa

def getProxy():
    openProxy = open("proxy.txt", "r")
    readProxy = openProxy.read()
    proxy = readProxy.split("\n")
    randomProxy = random.choice(proxy)
    return 'https://' + randomProxy

def randCategory(array):
    openProxy = open("kategori.txt", "r")
    readProxy = openProxy.read()
    proxy = readProxy.split("|")
    return proxy[array]

def getCategory(array):
    openProxy = open("kategori.txt", "r")
    readProxy = openProxy.read()
    proxy = readProxy.split("|")
    return proxy[array]

def getSingle(myUrl, category):

    headers = {"User-Agent": getUa()}
    proxies = {'http': getProxy()}

    try:
        uClient = requests.get(myUrl, headers=headers, proxies=proxies)
        pageHtml = uClient.text
        pageSoup = soup(pageHtml, "html.parser")
        # save files
        bahan = []
        langkah = []

        # get title and main image
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
                        myUrl
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

            saveError = open('error.html', 'w')
            saveError.write(str(pageSoup))

            print('Error getting image, may caused by proxy')
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