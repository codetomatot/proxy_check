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
ap.add_argument('-fn', '--file_name', type=str, required=False, help="force change output file name") 
ap.add_argument('-ft', '--file_type', type=str, required=False, help="force change output file type") 
ap.add_argument('-v', '--verbose', help="more descriptive output") 
ap.add_argument('--testing_url', type=str, help="url to test proxy on") 
args = ap.parse_args()
cwd = os.getcwd()

if args.file_name or args.file_type:
    DEFAULT_FILENAME = args.file_name
    DEFAULT_TYPE = args.file_type
else:
    DEFAULT_FILENAME = "output"
    DEFAULT_TYPE = ".json"

FILE = DEFAULT_FILENAME + DEFAULT_TYPE
# print(FILE)
# default url = https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc
data_url = args.url

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
            #default = https://www.google.com
            if args.testing_url:
                mkreq = requests.get(args.testing_url, proxies=proxy)
            else:
                mkreq = requests.get("https://www.google.com", proxies=proxy)
            if args.verbose:
                print(f"{Fore.GREEN + '[*]'} {Style.RESET_ALL + f'Trying proxy: {proxy}'} ")
                print(mkreq)
            else:
                if mkreq.status_code == 200:
                    print(f'{proxy} is working')
                
        except:
            print(f"{Fore.RED + '[!]'} {Style.RESET_ALL + 'Bad proxy.'} ")

if __name__ == "__main__":
    main()