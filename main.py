import zipfile
import os
import requests
import re
import time
from pathlib import Path
from pwn import log
from threading import Thread

# Settings

url = 'https://thunderstore.io/api/experimental/package/'
namespaces = ['notnotnotswipez', 'FlipMods', 'FlipMods', 'FlipMods', 'RugbugRedfern']
names = ['MoreCompany', 'ReservedItemSlotCore', 'ReservedFlashlightSlot', 'ReservedWalkieSlot', 'Skinwalkers']
mods_dir = '/tmp/lethalModManager/'
plugins = f'{mods_dir}BepInEx/plugins/'

# Algo variables.

threads = []

def downloadMods(namespace, name):
    mod_dir = f'{mods_dir}{name}.zip'
    r = requests.get(f'{url}{namespace}/{name}/')
    if r.status_code == 200:
        match = re.search(r'"latest":\s*({[^}]+})', r.text)
        latest = r.json()["latest"]
        download_url = latest["download_url"]
        p = log.progress(f'Downloading {name}... ')
        try:
            rdown = requests.get(download_url, allow_redirects=True)
            p.success("\t\tDownload successful!")
        except:
            p.failure(f"Failed to download {name} ({download_url})")
        with open(mod_dir, 'wb') as file:
            file.write(rdown.content)
    else:
        print(f"Error, status code: {r.status_code}.")
        
def unzipMods():
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

def zipBepInEx():
    p = log.progress(f'Zipping BepInEx folder... ')
    with zipfile.ZipFile(mods_dir+"BepInEx.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(mods_dir+"BepInEx"):
            for filename in filenames:
                relative_path = os.path.relpath(os.path.join(foldername, filename), mods_dir+"BepInEx")
                zipf.write(os.path.join(foldername, filename), arcname=relative_path)
    p.success("Done!")

def clearFiles():
    p = log.progress(f'Clearing all files... ')
    for file in os.listdir(mods_dir):
        if file != "BepInEx":
            os.remove(mods_dir + file)
    p.success("Done!")

def moveZippedFile():
    p = log.progress(f'Moving files... ')
    os.rename(mods_dir+"BepInEx.zip", "/var/www/metacalled.tech/cdn.metacalled.tech/public/uploads/BepInEx.zip")
    p.success("Done!")

def main():
    if not os.path.isdir(mods_dir):
        os.makedirs(mods_dir)
    for namespace, name in zip(namespaces, names):
        t = Thread(target=downloadMods, args=(namespace, name))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join() # Lock program until all threads have finished.
    unzipMods() # Unzips all downloaded mods and adds them up into BepInEx
    clearFiles() # Clear all files from the folder except BepInExzipBepInEx()
    zipBepInEx()
    moveZippedFile()

if __name__ == "__main__":
    main()
