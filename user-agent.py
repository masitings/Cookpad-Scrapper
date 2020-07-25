import requests
import json

def harvestProxy():
    url = "https://user-agent-strings.p.rapidapi.com/v1/user_agents/latest"

    headers = {
        'x-rapidapi-host': "user-agent-strings.p.rapidapi.com",
        # Use your own rapidapi apikey.
        'x-rapidapi-key': "d03a2f0d45msh07d2e7be11560d3p15275cjsn22b01f05fa5a"
    }

    # Save proxy 
    fOpen = open("ua.txt", "a+")

    response = requests.request("GET", url, headers=headers)
    jsonResp = json.loads(response.text)
    userAgent = jsonResp['results']
    #linux
    linuxChrome = userAgent['linux']['chrome']['string']
    fOpen.write(linuxChrome + "|")
    linuxFirefox = userAgent['linux']['firefox']['string']
    fOpen.write(linuxFirefox + "|")
    # macOs
    macChrome = userAgent['mac_os']['chrome']['string']
    macFirefox = userAgent['mac_os']['firefox']['string']
    macSafari = userAgent['mac_os']['safari']['string']
    fOpen.write(macChrome + "|")
    fOpen.write(macFirefox + "|")
    fOpen.write(macSafari + "|")
    #windows
    winChrome = userAgent['windows']['chrome']['string']
    winFirefox = userAgent['windows']['chrome']['string']
    fOpen.write(winChrome + "|")
    fOpen.write(winFirefox + "|")
    print('Harvest User Agent Complete')
    harvestProxy()

harvestProxy()