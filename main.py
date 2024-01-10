import requests
import time
import json
import re
from pathlib import Path

namespaces = ['notnotnotswipez', 'FlipMods', 'FlipMods', 'FlipMods', 'RugbugRedfern']
names = ['MoreCompany', 'ReservedItemSlotCore', 'ReservedFlashlightSlot', 'ReservedWalkieSlot', 'Skinwalkers']
def updateMod(namespace, name):
    home_dir = str(Path.home())
    home_dir = home_dir + '/'
    url = 'https://thunderstore.io/api/experimental/package/'
    r = requests.get(f'{url}{namespace}/{name}/')
    if r.status_code == 200:
        match = re.search(r'"latest":\s*({[^}]+})', r.text)
        latest = match.group(1)
        latest = json.loads(latest)
        download_url = latest["download_url"]
        rdown = requests.get(url, allow_redirects=True)
        with open(f'{home_dir}')
        #save = open(f'{home_dir}Baixades/{name}.zip', 'wb').write(rdown.content)
        print(download_url)
        print(save)
    else:
        print(f"Error, status code: {r.status_code}.")

#def uploadMod(name):
   # mods_dir =
def main():
    for namespace, name in zip(namespaces, names):
        updateMod(namespace, name)
    #for mod in names:
     #
main()