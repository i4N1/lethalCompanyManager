import requests
import time
import json
import re

namespaces = ['notnotnotswipez', 'FlipMods', 'FlipMods', 'FlipMods', 'RugbugRedfern']
names = ['MoreCompany', 'ReservedItemSlotCore', 'ReservedFlashlightSlot', 'ReservedWalkieSlot', 'Skinwalkers']
def updateMod(namespace, name):
    r = requests.get(f'https://thunderstore.io/api/experimental/package/{namespace}/{name}/')
    if r.status_code == 200:
        match = re.search(r'"latest":\s*({[^}]+})', r.text)
        latest = match.group(1)
        latest = json.loads(latest)
        download_url = latest["download_url"]
        print(download_url)
    else:
        print("Error")
def main():
    for namespace, name in zip(namespaces, names):
        updateMod(namespace, name)

main()