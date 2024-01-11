import os
import time
import zipfile
import requests
from tkinter import *
from tkinter import filedialog
from configparser import ConfigParser

# Settings
remote_url = 'https://cdn.metacalled.tech/uploads/BepInEx.zip'

# Algo variables

uiRoot = Tk()
config_object = ConfigParser()

def clearWidgets():
    for widget in uiRoot.winfo_children():
        widget.destroy()

def checkConfig():
    if not os.path.isfile("config.ini"):
        with open('config.ini', 'w') as conf:
            config_object['AppConfig'] = {
                "gamePath": "None"
            }
            config_object.write(conf)
            conf.close()
        return ""
    else:
        config_object.read("config.ini")
        return str(config_object["AppConfig"]["gamePath"])

def openFolder():
    directory = filedialog.askdirectory()
    with open('config.ini', 'w') as conf:
        config_object['AppConfig'] = {
            "gamePath": directory
        }
        config_object.write(conf)
        conf.close()
    gamePath = checkConfig()
    pathSelected(gamePath)

def downloadAndExtract(gamePath):
    clearWidgets()
    r = requests.get(remote_url)
    zip_path = gamePath+r"/BepInEx.zip"
    with open(zip_path, 'wb') as file:
        file.write(r.content)
    with zipfile.ZipFile(zip_path, 'r') as unzipping:
        unzipping.extractall(gamePath+r"/BepInEx")
    os.remove(zip_path)
    Label(uiRoot, text="Se han actualizado todos los mods!", font=("Verdana",12)).pack(anchor=CENTER)
    Button(uiRoot, text="OK", command=exit).pack(anchor=CENTER)

def pathSelected(gamePath):
    clearWidgets()
    uiRoot.geometry("500x100")
    Label(uiRoot, text="Path seleccionado: " + gamePath, font=("Verdana",12)).pack(anchor=CENTER)
    Label(uiRoot, text="Ya está todo listo, presiona UPDATE para actualizar los mods.", font=("Verdana",10)).pack(anchor=CENTER)
    Button(uiRoot, text="UPDATE", command=lambda: downloadAndExtract(gamePath)).pack(anchor=CENTER)

def main():
    uiRoot.title("Lethal Company Manager")
    uiRoot.resizable(False, False)
    gamePath = checkConfig()
    if gamePath == "" or gamePath == "None":
        uiRoot.geometry("650x75")
        Label(uiRoot, text="Presiona select y selecciona la carpeta base del juego.", font=("Verdana",12)).pack(anchor=CENTER)
        Button(uiRoot, text="SELECT", command=openFolder).pack(anchor=CENTER)
    else:
        pathSelected(gamePath)
        
    
    
if __name__ == "__main__":
    main()
    uiRoot.mainloop()
