#!/usr/bin/env python3
import shutil
import zipfile
import os
import requests
import re
import time
from pathlib import Path
from pwn import log
from threading import Thread
from datetime import datetime

# Settings

url = 'https://thunderstore.io/api/experimental/package/'
mods_dir = '/tmp/lethalModManager/'
win_mods_dir = './tmp/lethalModManager/' # This is for debugging meanings, the script is not meant to be used in windows but just in case.
plugins = f'{mods_dir}BepInEx/plugins/'
uploads_path = '/var/www/metacalled.tech/cdn.metacalled.tech/public/uploads/'

# Algo variables.

threads = []
mods = []

# Checking OS.

if os.name == 'nt': # Windows
    mods_dir = win_mods_dir
    plugins = f'{mods_dir}BepInEx/plugins/'

def downloadMods(namespace, name):
    mod_dir = f'{mods_dir}{name}.zip'
    r = requests.get(f'{url}{namespace}/{name}/')
    if r.status_code == 200:
        match = re.search(r'"latest":\s*({[^}]+})', r.text)
        latest = r.json()["latest"]
        download_url = latest["download_url"]
        version = latest["version_number"]
        p = log.progress(f'Downloading {name} ({version})... ')
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
                file_path: os.path.join(foldername, filename)
                relative_path = os.path.relpath(file_path, mods_dir+"BepInEx")
                zipf.write(file_path, arcname=relative_path)
    p.success("Done!")

def clearFiles():
    p = log.progress(f'Clearing all files... ')
    for file in os.listdir(mods_dir):
        if file != "BepInEx":
            if os.path.isdir(mods_dir + file):
                shutil.rmtree(mods_dir + file)
            else:
                os.remove(mods_dir + file)
    p.success("Done!")

def moveZippedFile():
    p = log.progress(f'Moving files... ')
    os.rename(mods_dir+"BepInEx.zip", uploads_path+"BepInEx.zip")
    p.success("Done!")

def main():
    print('-'*50)
    print(str(datetime.now()))
    print('-'*50)
    if not os.path.isdir(mods_dir):
        os.makedirs(mods_dir)
    with open("mods.txt", "r") as modsfile:
        content = modsfile.read().splitlines()
        for mod in content:
            t = Thread(target=downloadMods, args=(mod.split("/")[0], mod.split("/")[1]))
            t.start()
            threads.append(t)
    for thread in threads:
        thread.join() # Lock program until all threads have finished.
    unzipMods() # Unzips all downloaded mods and adds them up into BepInEx
    clearFiles() # Clear all files from the folder except BepInExzipBepInEx()
    zipBepInEx()
    moveZippedFile()
    print('-'*50)
    print(str(datetime.now()))
    print('-'*50)

if __name__ == "__main__":
    main()
