import os
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup


f = open("test.json")
data = json.load(f)
print(data["people"]["sam"])
f.close()