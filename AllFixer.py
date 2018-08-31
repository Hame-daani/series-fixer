import os
from myModule import fix, getId, natural_keys
from colorama import Fore, Style


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
            problems.extend(fix(serie, season[1:], id))

print("Problmes:")
for p in problems:
    print(p)
