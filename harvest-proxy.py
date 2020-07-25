import requests
import json

def harvest():
    url = "https://getproxylist-getproxylist-v1.p.rapidapi.com/proxy"
    querystring = {"protocol":"http"}
    headers = {
        'x-rapidapi-host': "getproxylist-getproxylist-v1.p.rapidapi.com",
        'x-rapidapi-key': "d03a2f0d45msh07d2e7be11560d3p15275cjsn22b01f05fa5a"
    }
    fOpen = open("tmp/proxy.txt", "a+")
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code is not 200:
        print('Limit Exceed')
    else:
        result = json.loads(response.text)
        resp = result['protocol']+'://'+str(result['ip'])+':'+str(result['port'])
        fOpen.write(resp + ",")
        print('Success')
        harvest()

harvest()