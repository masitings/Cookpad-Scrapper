import urllib.request
import json
from bs4 import BeautifulSoup as soup

myurl = 'https://cookpad.com/id/resep/13230605-pepes-ikan'

req = urllib.request.Request(
    myurl, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
)

uClient = urllib.request.urlopen(req)
pageHtml = uClient.read()
uClient.close()
pageSoup = soup(pageHtml, "html.parser")

# save files
bahan = []
langkah = []

# get title and main image
recipeTitle = pageSoup.h1.string.strip()
mainImage = pageSoup.find('div', {"class":"tofu_image"}).find('img')['src']

# get ingredient
mainIngridient = pageSoup.find('section', {"id":"ingredients"})
ingredientList = mainIngridient.find('div', {"class":"ingredient-list"})
ingredients = ingredientList.find_all('li', {"class":"ingredient"})
for ingredient in ingredients:
    ingWrap = ingredient.find('div', {"itemprop":"ingredients"})
    Qty = ingWrap.find('bdi', {"class":"ingredient__quantity"}).text.strip()
    if Qty:
        bahan.append(ingWrap.text.strip())
    
    
# get steps
# print("-----------------------")

mainStep = pageSoup.find('section', {"id": "steps"})
listStep = mainStep.find_all('li', {"class":"step"})

for step in listStep:
    steps = {}
    textStep = step.find('div', {"itemprop": "recipeInstructions"}).text.strip()
    langkah.append(textStep)
    # print(textStep)


slugTitle = recipeTitle.lower().replace(' ', '-')
filename = slugTitle + '.json'
path = 'result/' + filename
dataJson = {"title": recipeTitle, "image": mainImage,"bahan": bahan, "langkah": langkah}

with open(path, "w") as writeJson:
    json.dump(dataJson, writeJson, ensure_ascii=False)
