import requests

proxies = {'http': 'http://1.0.0.211:80'}
reads = requests.get("https://www.tumblr.com/", proxies=proxies)
# requests.post("https://www.tumblr.com/", proxies=proxies)
print(reads.text)