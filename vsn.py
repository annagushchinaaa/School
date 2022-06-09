import requests

entrypoint = "https://www.chitai-gorod.ru/shops/"
r = requests.get(entrypoint)
r.text()