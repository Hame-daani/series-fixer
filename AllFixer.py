import requests
import bs4
import os
import re
from colorama import Fore, Style


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def getEpisodes(id, season):
    url = "https://www.imdb.com/title/{}/episodes?season={}".format(
        id, season)
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


def fixFiles(serie, season, episodes):
    # print("Fixing Files {} Season {}".format(serie, season))
    path = "./{}/S{}".format(serie, season)
    list = [f for f in os.listdir(path) if not (f.endswith(
        ".srt") or f.endswith(".Srt") or f.endswith(".txt") or f.endswith(".py") or f.endswith(".ass") or f.endswith(".ico"))]
    list.sort(key=natural_keys)
    if len(episodes) == len(list):
        f = open("{}/files.txt".format(path), 'w')
        for l in list:
            f.write(l + "\n")
        f.close()
        for i in range(0, len(list)):
            episodes[i] = episodes[i].replace("/", "-")
            os.rename(
                "{}/{}".format(path, list[i]), "{}/{} - {}".format(path, i + 1, episodes[i]).encode("utf-8"))
        print(Fore.GREEN + "--- Fix {} Season {} files ---".format(serie, season))
        print(Style.RESET_ALL)
    else:
        problem = "*** Files {} Season {} episodes:{} list:{} ***".format(
            serie, season, len(episodes), len(list))
        print(Fore.RED + problem)
        print(Style.RESET_ALL)
        problems.append(problem)


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


def fixSubs(serie, season, episodes):
    # print("Fixing {} Season {} Subs".format(serie, season))
    path = "./{}/S{}".format(serie, season)
    list = [f for f in os.listdir(path) if (f.endswith(
        ".srt") or f.endswith(".Srt") or f.endswith(".ass"))]
    list.sort(key=natural_keys)
    if len(episodes) == len(list):
        f = open("{}/subs.txt".format(path), 'w')
        for l in list:
            f.write(l + "\n")
        f.close()
        for i in range(0, len(list)):
            episodes[i] = episodes[i].replace("/", "-")
            os.rename(
                "{}/{}".format(path, list[i]), "{}/{} - {}.srt".format(path, i + 1, episodes[i]).encode("utf-8"))
        print(Fore.GREEN + "--- Fix {} Season {} subs ---".format(serie, season))
        print(Style.RESET_ALL)
    else:
        problem = "*** Subs {} Season {} episodes:{} list:{} ***".format(
            serie, season, len(episodes), len(list))
        print(Fore.RED + problem)
        print(Style.RESET_ALL)
        problems.append(problem)


def fix(serie, season, id):
    season = season[1:]
    episodes = getEpisodes(id, season)
    if len(episodes) > 0:
        print("Get Episods for {} Season {}".format(serie, season))
        fixFiles(serie, season, episodes)
        fixSubs(serie, season, episodes)
    else:
        print(
            Fore.RED + "*** Problem Getting Episodes {} Season {} ***".format(serie, season))
        print(Style.RESET_ALL)
        problems.append("Getting Episodes {} Season {}".format(serie, season))


problems = []
series = [d for d in os.listdir("./") if os.path.isdir("./{}".format(d))]
series.sort(key=natural_keys)
for serie in series:
    print("Getting Id for " + serie)
    id = getId(serie)
    if id == 0:
        print(Fore.RED + "*** Problem Geting Id for {} ***".format(serie))
        print(Style.RESET_ALL)
        problems.append("Geting Id for {}".format(serie))
    else:
        print("Get Id for " + serie)
        seasons = [d for d in os.listdir(
            "./{}".format(serie)) if os.path.isdir("./{}/{}".format(serie, d))]
        for season in seasons:
            fix(serie, season, id)
print("Problmes:")
for p in problems:
    print(p)
