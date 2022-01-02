import os
import json
import requests
import threading
import argparse
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)

ap = argparse.ArgumentParser()
ap.add_argument('-u', '--url', type=str, required=True, help="The URL which contains proxy data")
ap.add_argument('-lt', '--list_type', type=str, required=True, help="name")
ap.add_argument('-v', '--verbose', help="more descri[tive output")
args = ap.parse_args()

cwd = os.getcwd()

DEFAULT_FILENAME = "output"
DEFAULT_TYPE = ".json"
FILE = DEFAULT_FILENAME + DEFAULT_TYPE
data_url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc"

def file_handler():
    if os.path.isfile(FILE):
        print(f"{Fore.GREEN+'[*]'} {Style.RESET_ALL + f'file exists: {FILE} in {cwd}'}")
        req = requests.get(url=data_url)
        if req.status_code == 200:
            with open(FILE, "w") as ft:
                ft.write(req.text)
                fr = open(FILE, "r")
                cdata = json.dumps(json.load(fr), indent=4)
                fr.close()
                ft.close()
            os.system("rm {}".format(FILE))
            os.system("touch {}".format((FILE)))
            with open(FILE, "w") as tfw:
                tfw.write(cdata)
                tfw.close()  
            f = open(FILE, "r")
            return f   
    else:
        print(False)
        os.system(f'touch {FILE}')
        return "0"

def main():
    bolf = file_handler()
    ips = []
    ports = []
    protos = []
    if bolf != "0":
        fre = json.load(bolf)
        for i in fre["data"]:
            ips.append(i["ip"])
            ports.append(i["port"])
            protos.append(i["protocols"][0])

    for i in range(len(ips)):
        proxy = {
            f"{protos[i]}": f'{protos[i]}://{ips[i]}:{ports[i]}'
        }
        try:
            print(f"{Fore.GREEN + '[*]'} {Style.RESET_ALL + f'Trying proxy: {proxy}'} ")
            mkreq = requests.get("https://www.google.com", proxies=proxy)
            print(mkreq)
        except:
            print(f"{Fore.RED + '[!]'} {Style.RESET_ALL + 'Bad proxy.'} ")

# if __name__ == "__main__":
    # main()
