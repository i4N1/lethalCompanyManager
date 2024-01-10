import zipfile
import os
import requests
import time
import json
import re
from pathlib import Path

namespaces = ['notnotnotswipez', 'FlipMods', 'FlipMods', 'FlipMods', 'RugbugRedfern']
names = ['MoreCompany', 'ReservedItemSlotCore', 'ReservedFlashlightSlot', 'ReservedWalkieSlot', 'Skinwalkers']
home_dir = str(Path.home())
mods_dir = home_dir + '\\modero\\'

def downloadMods(namespace, name):
    home_dir = str(Path.home())
    home_dir = home_dir + '\\modero\\' + name + '.zip'
    url = 'https://thunderstore.io/api/experimental/package/'
    r = requests.get(f'{url}{namespace}/{name}/')
    if r.status_code == 200:
        match = re.search(r'"latest":\s*({[^}]+})', r.text)
        latest = match.group(1)
        latest = json.loads(latest)
        download_url = latest["download_url"]
        rdown = requests.get(download_url, allow_redirects=True)
        with open(home_dir, 'wb') as file:
            file.write(rdown.content)
        print(download_url)
    else:
        print(f"Error, status code: {r.status_code}.")
def unzipMods():
    print(mods_dir)
    for zip in os.listdir(mods_dir):
        if zip.endswith(".zip"):
            zip_path = os.path.join(mods_dir, zip)
            with zipfile.ZipFile(zip_path, 'r') as unzipping:
                unzipping.extractall(f'{mods_dir}\\unzipped\\')
    for dll in os.listdir(f'{mods_dir}\\unzipped'):
        if dll.endswith('.dll'):
            print(dll)
            os.rename(f'{mods_dir}unzipped\\{dll}', f'{mods_dir}unzipped\\BepInEx\\plugins\\{dll}')
def main():
    for namespace, name in zip(namespaces, names):
        downloadMods(namespace, name)
    unzipMods()
main()
