import requests
import bs4
import os
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def getEpisodes(title, season):
    url = "https://www.imdb.com/title/{}/episodes?season={}".format(
        title, season)
    selector = "#episodes_content strong a"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, features="html5lib")
    data = soup.select(selector)
    episodes = []
    for d in data:
        episodes.append(d['title'])
    return episodes


def getId(title):
    selector = ".lister-item-header a"
    url = "https://www.imdb.com/search/title?title="
    title = title.replace(" ", "+")
    data = requests.get(url + title)
    soup = bs4.BeautifulSoup(data.content, features="html5lib")
    d = soup.select(selector)
    if d != 0:
        id = str(d[0])
    else:
        print("Problem Geting Id")
        return 0
    id = id[id.index("tt"):id.index("/?")]
    return id


def listSeason():
    print("**** List Seasons ****")
    for root, dirs, files in os.walk("./"):
        print(dirs)


def printEpisodes():
    print("**** Print Episodes ****")
    season = input("Input Season: ")
    episodes = getEpisodes(id, season)
    for ep in episodes:
        print(ep)


def fixFiles():
    print("**** Fix Files ****")
    season = input("Input Season: ")
    path = "./S{}".format(season)
    list = [f for f in os.listdir(path) if not (f.endswith(
        ".srt") or f.endswith(".Srt"))]
    list.sort(key=natural_keys)
    episodes = getEpisodes(id, season)
    if len(episodes) == len(list):
        for i in range(0, len(list)):
            os.rename(
                "{}/{}".format(path, list[i]), "{}/{} - {}".format(path, i + 1, episodes[i]).encode("utf-8"))
        print("Fix Season {} files".format(season))
    else:
        print("Problem! {} - {}".format(len(episodes), len(list)))


def printFiles():
    print("**** Print Files ****")
    season = input("Input Season: ")
    path = "./S{}".format(season)
    list = [f for f in os.listdir(path) if not (f.endswith(
        ".srt") or f.endswith(".Srt"))]
    list.sort(key=natural_keys)
    for l in list:
        print(l)


def printSubs():
    print("**** Print Subs *****")
    season = input("Input Season: ")
    path = "./S{}".format(season)
    list = [f for f in os.listdir(path) if (f.endswith(
        ".srt") or f.endswith(".Srt"))]
    list.sort(key=natural_keys)
    for l in list:
        print(l)


def fixSubs():
    print("**** Fix Subs ****")
    season = input("Input Season: ")
    path = "./S{}".format(season)
    list = [f for f in os.listdir(path) if (f.endswith(
        ".srt") or f.endswith(".Srt"))]
    list.sort(key=natural_keys)
    episodes = getEpisodes(id, season)
    if len(episodes) == len(list):
        for i in range(0, len(list)):
            os.rename(
                "{}/{}".format(path, list[i]), "{}/{} - {}.srt".format(path, i + 1, episodes[i]).encode("utf-8"))
        print("Fix Season {} subs".format(season))
    else:
        print("Problem! {} - {}".format(len(episodes), len(list)))


serie = input("Input Serie: ")
id = getId(serie)
if id != 0:
    print("Get Id: ", id)
else:
    print("Problem Get Id!")

a = input("Input: ")
while a != "close":
    if a.startswith("list"):
        listSeason()
    elif a.startswith("episodes"):
        printEpisodes()
    elif a.startswith("files"):
        printFiles()
    elif a.startswith("fix files"):
        fixFiles()
    elif a.startswith("subs"):
        printSubs()
    elif a.startswith("fix subs"):
        fixSubs()
    else:
        print("Wrong!!!!!!!")
    a = input("Input: ")
