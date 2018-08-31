from myModule import fix, getId
from colorama import Fore, Style


serie = input("Input Serie Name: ")
serie = serie.title()
print("Getting Id for " + serie)
id = getId(serie)

if id == 0:
    print(Fore.RED + "*** Problem Geting Id for {} ***".format(serie))
    print(Style.RESET_ALL)
else:
    print(Fore.GREEN + "Get Id For {}".format(serie))
    print(Style.RESET_ALL)
    season = input("Input Season: ")
    fix(serie, season, id)
