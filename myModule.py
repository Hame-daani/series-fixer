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


def fixFiles(serie, season, episodes):
    problems = []
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

        problems.append(problem)
        print(Fore.RED + problem)
        print(Style.RESET_ALL)

    return problems


def fixSubs(serie, season, episodes):
    problems = []
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

        problems.append(problem)
        print(Fore.RED + problem)
        print(Style.RESET_ALL)

    return problems


def fix(serie, season, id):
    problems = []
    episodes = getEpisodes(id, season)
    if len(episodes) > 0:
        print("Get Episods for {} Season {}".format(serie, season))
        problems.extend(fixFiles(serie, season, episodes))
        problems.extend(fixSubs(serie, season, episodes))
    else:
        problem = "*** Problem Getting Episodes {} Season {} ***".format(
            serie, season)
        print(
            Fore.RED + "*** Problem Getting Episodes {} Season {} ***".format(serie, season))
        problems.append(problem)
        print(Style.RESET_ALL)

    return problems
