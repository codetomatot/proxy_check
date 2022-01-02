import os
import json
import requests
import threading
from pathlib import Path
from bs4 import BeautifulSoup

cwd = os.getcwd()

DEFAULT_FILENAME = "output"
DEFAULT_TYPE = ".json"
FILE = DEFAULT_FILENAME + DEFAULT_TYPE
data_url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc"

if os.path.isfile(FILE):
    print(f"[*] file exists: {FILE} in {cwd}")
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
else:
    print(False)
    os.system(f'touch {FILE}')


proxy = {
    'http': 'socks5://67.109.31.192:20000'
}
#ip_req = requests.get("http://www.google.com",proxies=data)
#print(ip_req) 
