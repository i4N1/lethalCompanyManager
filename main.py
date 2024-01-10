import zipfile
import os
import requests
import json
import re
from pathlib import Path
from pwn import log

url = 'https://thunderstore.io/api/experimental/package/'
namespaces = ['notnotnotswipez', 'FlipMods', 'FlipMods', 'FlipMods', 'RugbugRedfern']
names = ['MoreCompany', 'ReservedItemSlotCore', 'ReservedFlashlightSlot', 'ReservedWalkieSlot', 'Skinwalkers']
home_dir = str(Path.home())
mods_dir = home_dir + '\\modero\\'
unzipped = f'{mods_dir}unzipped\\'
plugins = f'{unzipped}\\BepInEx\\plugins\\'
def downloadMods(namespace, name):
    home_dir = f'{mods_dir}{name}.zip'
    r = requests.get(f'{url}{namespace}/{name}/')
    if r.status_code == 200:
        match = re.search(r'"latest":\s*({[^}]+})', r.text)
        latest = match.group(1)
        latest = json.loads(latest)
        download_url = latest["download_url"]
        p = log.progress(f'Downloading {name} from: {download_url}')
        try:
            rdown = requests.get(download_url, allow_redirects=True)
            p.success("\n\tDownload successful.")
        except:
            p.failure(f"Failed to download {name} ({download_url})")
        with open(home_dir, 'wb') as file:
            file.write(rdown.content)
    else:
        print(f"Error, status code: {r.status_code}.")
def unzipMods():
    print(mods_dir)
    for zip in os.listdir(mods_dir):
        if zip.endswith(".zip"):
            zip_path = os.path.join(mods_dir, zip)
            with zipfile.ZipFile(zip_path, 'r') as unzipping:
                unzipping.extractall(unzipped)
    for dll in os.listdir(unzipped):
        if dll.endswith('.dll'):
            try:
                os.rename(os.path.join(unzipped, dll), os.path.join(plugins, dll))
            except FileExistsError:
                log.failure(f"{dll} already exists in {plugins}...")
def main():
    for namespace, name in zip(namespaces, names):
        downloadMods(namespace, name)
    unzipMods()
main()