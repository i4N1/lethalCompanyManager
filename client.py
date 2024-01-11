import requests
import customtkinter
from customtkinter import filedialog
from pathlib import Path
import zipfile

default_steam = 'C:\Program Files (x86)\Steam\steamapps\common'
folder_path = '/home/kali/lethalModManager'
zip_path = f'{folder_path}/BepInEx.zip'
url = 'https://cdn.metacalled.tech/uploads/BepInEx.zip'
#GUI
app = customtkinter.CTk()
app.title("lethalModManager")
app.geometry("500x100")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
def browseButton():
    global folder_path
    folder_path = filedialog.askdirectory()
    with open('config.cfg', 'w') as file:
        file.write(folder_path)
def updateMods():
    global folder_path
    try:
        with open('config.cfg', 'r') as file:
            folder_path = file.read()
    except FileNotFoundError:
        with open('config.cfg', 'w') as file:
            file.write(default_steam)
        print("[-] config.cfg not found, creating it and using default steam location...")
    r = requests.get(url)
    with open(zip_path, 'wb') as file:
        file.write(r.content)
    with zipfile.ZipFile(zip_path, 'r') as unzipping:
        unzipping.extractall(folder_path)

#GUI Buttons
updateButton = customtkinter.CTkButton(app, text="Update mods", command=updateMods)
updateButton.grid(row=0, column=0, padx=10, pady=10)
locationButton = customtkinter.CTkButton(app, text="...",fg_color="gray" , command=browseButton)
locationButton.grid(row=0, column=1, padx=10, pady=10)

app.mainloop()