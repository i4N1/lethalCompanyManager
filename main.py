import zipfile
import os
import requests
import json
import re
from pathlib import Path
from pwn import log
from threading import Thread

url = 'https://thunderstore.io/api/experimental/package/'
namespaces = ['notnotnotswipez', 'FlipMods', 'FlipMods', 'FlipMods', 'RugbugRedfern']
names = ['MoreCompany', 'ReservedItemSlotCore', 'ReservedFlashlightSlot', 'ReservedWalkieSlot', 'Skinwalkers']
mods_dir = '/tmp/lethalModManager/'
plugins = f'{mods_dir}BepInEx/plugins/'
def downloadMods(namespace, name):
    mod_dir = f'{mods_dir}{name}.zip'
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
        with open(mod_dir, 'wb') as file:
            file.write(rdown.content)
    else:
        print(f"Error, status code: {r.status_code}.")
def unzipMods():
    print(mods_dir)
    for zip in os.listdir(mods_dir):
        if zip.endswith(".zip"):
            zip_path = os.path.join(mods_dir, zip)
            with zipfile.ZipFile(zip_path, 'r') as unzipping:
                unzipping.extractall(mods_dir)
    for dll in os.listdir(mods_dir):
        if dll.endswith('.dll'):
            try:
                os.rename(os.path.join(mods_dir, dll), os.path.join(plugins, dll))
            except FileExistsError:
                log.failure(f"{dll} already exists in {plugins}...")
def main():
    for namespace, name in zip(namespaces, names):
        threading.Thread(target=downloadMods, args=(namespace, name)).start()
    unzipMods()

if __name__ == "__main__":
    main()
