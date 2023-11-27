import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import shutil


def getlasttxt(string1):
    string1 = [*string1]
    i = 0
    last_period_index = -1

    # Find the last occurrence of "."
    while i < len(string1):
        if string1[i] == ".":
            last_period_index = i
        i += 1

    # Remove all elements before the last period
    if last_period_index >= 0:
        string1 = string1[last_period_index + 1:]
        string1 = (''.join(string1))
    return string1


# find the key with a value
def findkey(filetype_dict, search_value):
    if not isinstance(filetype_dict, dict):
        raise TypeError("Input filetype_dict must be a dictionary.")
    if not isinstance(search_value, str):
        raise TypeError("Input search_value must be a string.")
    for key, value in filetype_dict.items():
        if search_value in value:
            return key
    return None


filetypedic = {
    "Videos": ["mp4", "mov", "avi", "wmv", "avchd", "webm", "flv"],
    "Pictures": ["jpeg", "jpg", "png", "gif", "tiff", "psd", "eps", "ai", "indo", "raw"],
    "Text": ["doc", "docx", "odt", "rtf", "tex", "txt", "wpd", "pdf"],
    "Audio": ["mp3", "m4a", "aac", "flac", "wav", "aiff"],
    "ZIP": ["zip"]
}


root = tk.Tk()
root.geometry("700x300")
root.resizable(0, 0)
title = tk.Label(root, text="Folder Sorter", font=("Ariel", 10))
title.pack()
folder_path = tk.StringVar()
folder_directory = folder_path.get()


def folderloc():
    filename = filedialog.askdirectory()
    folder_path.set(filename)


def retrieve_path():
    path = folder_path.get()
    if os.path.isdir(path):
        print("Selected Folder: ", path)
    else:
        print("Invalid Folder Path")


def howmanyfolders(listoffiles):
    result = []
    for file in listoffiles:
        filetype = getlasttxt(file)
        key = findkey(filetypedic, filetype)
        if key:
            result.append(key)
    result = list(set(result))
    return result


def startbutton():
    print("Starting To Sort...")
    path = folder_path.get()
    files = os.listdir(path)

    # Create necessary folders for each category
    categories = howmanyfolders(files)
    for category in categories:
        category_path = os.path.join(path, category)
        os.makedirs(category_path, exist_ok=True)

    # Create "Other" folder
    other_path = os.path.join(path, "Other")
    os.makedirs(other_path, exist_ok=True)

    # Move files to their corresponding category folders
    for file in files:
        dest = ""
        file_extension = getlasttxt(file)
        category = findkey(filetypedic, file_extension)
        if category:
            if category == "Videos":
                dest = os.path.join(path, "Videos")
            elif category == "Pictures":
                dest = os.path.join(path, "Pictures")
            elif category == "Text":
                dest = os.path.join(path, "Text")
            elif category == "Audio":
                dest = os.path.join(path, "Audio")
            elif category == "ZIP":
                dest = os.path.join(path, "ZIP")
        else:
            dest = other_path

        if dest:
            source = os.path.join(path, file)
            shutil.move(source, dest)

    print("Finished Sorting.")


# Buttons
folder_button = Button(root, text="Choose The Folder", command=folderloc)
folder_button.pack(pady=20)

retrieve_button = tk.Button(root, text="Retrieve Path", command=retrieve_path)
retrieve_button.pack(pady=10)

start_button = tk.Button(root, text="Start Sorting", command=startbutton)
start_button.pack(pady=5)

root.mainloop()
