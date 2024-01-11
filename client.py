import os
import time
import zipfile
import requests
from tkinter import *
from tkinter import filedialog
from configparser import ConfigParser

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
                "gamePath": "None",
                "remoteServer": "None",
                "alternativeDownload": False
            }
            config_object.write(conf)
            conf.close()
        return [None,None,None]
    else:
        config_object.read("config.ini")
        return [config_object["AppConfig"]["gamePath"], config_object["AppConfig"]["remoteServer"], config_object["AppConfig"]["alternativeDownload"]]

def setRemoteURL(currentSettings):
    clearWidgets()
    button_pressed = StringVar()
    checkbox_value = BooleanVar()
    Label(uiRoot, text="Introduce el URL de donde se va a descargar el archivo.", font=("Verdana",12)).pack(anchor=CENTER)
    url = Entry(uiRoot, width=600)
    url.pack(anchor=CENTER)
    checkbox = Checkbutton(uiRoot, variable=checkbox_value, text="Alternative mode")
    checkbox.pack(anchor=CENTER)
    boton = Button(uiRoot, text="OK", command=lambda: button_pressed.set("ok"))
    boton.pack(anchor=CENTER)
    boton.wait_variable(button_pressed)
    with open('config.ini', 'w') as conf:
        config_object['AppConfig'] = {
                "gamePath": currentSettings[0],
                "remoteServer": url.get(),
                "alternativeDownload": checkbox_value.get()
        }
        config_object.write(conf)
        conf.close()
    currentSettings[1] = url.get()
    pathSelected(currentSettings)

def openFolder(currentSettings):
    directory = filedialog.askdirectory()
    currentSettings[0] = directory
    setRemoteURL(currentSettings)

def downloadAndExtract(gamePath, remote_url):
    clearWidgets()
    try:
        r = requests.get(remote_url)
        zip_path = gamePath+r"/BepInEx.zip"
        with open(zip_path, 'wb') as file:
            file.write(r.content)
        with zipfile.ZipFile(zip_path, 'r') as unzipping:
            unzipping.extractall(gamePath+r"/BepInEx")
        os.remove(zip_path)
        Label(uiRoot, text="Se han actualizado todos los mods!", font=("Verdana",12)).pack(anchor=CENTER)
    except Exception as e:
        Label(uiRoot, text="Ha ocurrido un error, mira la consola para más detalles.", font=("Verdana",12)).pack(anchor=CENTER)
        print(e)
    Button(uiRoot, text="OK", command=uiRoot.destroy).pack(anchor=CENTER)

def pathSelected(currentSettings):
    clearWidgets()
    gamePath = currentSettings[0]
    if currentSettings[2]:
        URL = requests.get(currentSettings[1]).content
    else:
        URL = currentSettings[1]
    Label(uiRoot, text="Path seleccionado: " + gamePath, font=("Verdana",12)).pack(anchor=CENTER)
    Label(uiRoot, text="Ya está todo listo, presiona UPDATE para actualizar los mods.", font=("Verdana",10)).pack(anchor=CENTER)
    Button(uiRoot, text="UPDATE", command=lambda: downloadAndExtract(gamePath, URL)).pack(anchor=CENTER)
    Button(uiRoot, text="...", command=lambda: openFolder(currentSettings)).pack(anchor=E)

def main():
    uiRoot.title("Lethal Company Manager")
    uiRoot.resizable(False, False)
    currentSettings = checkConfig()
    uiRoot.geometry("650x100")
    if currentSettings[0] == None:
        Label(uiRoot, text="Presiona select y selecciona la carpeta base del juego.", font=("Verdana",12)).pack(anchor=CENTER)
        Button(uiRoot, text="SELECT", command=lambda: openFolder(currentSettings)).pack(anchor=CENTER)
    else:
        pathSelected(currentSettings)
        
    
    
if __name__ == "__main__":
    main()
    uiRoot.mainloop()
