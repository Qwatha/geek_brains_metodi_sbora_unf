import requests
import json


def save_json(response):
    with open("response.json", "w") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)


def get_repos(username, tokenpath):
    token = open(tokenpath).read()

    r = requests.get("https://api.github.com/user", auth=(username, token))

    return r, r.text
