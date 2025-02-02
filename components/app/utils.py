import os
from PIL import Image, ImageDraw, ImageFont
from tkinter import messagebox as mb


def open_folder(folder):
    if os.path.isdir(folder):
        os.startfile(folder)
    else:
        mb.showinfo('Info', 'Folder not found')


def folder_check(folder):  # Creates a new 'generated_certificates' folder if not already present
    if os.path.isdir(folder):
        pass
    else:
        mb.showinfo('Info', 'Folder not found, creating a new one')
        os.mkdir(folder)


def generate(master,placeholders,data,folder):
    if folder == "":
        mb.showerror('Destination error', 'Please select a destination folder')
        return
    if master.system_variables['filepath'] == "":
        mb.showerror('Error', 'Please select an image first')
        return
    if master.system_variables['datafilepath'] == "":
        mb.showerror('Error', 'Please load data first')
        return
    if len(master.placeholders) == 0:
        mb.showerror('Error', 'Invalid Data')
        return
    if len(data) == 0:
        mb.showerror('Error', 'No data found')
        return
    if master.RightUpperFrame.export_entry.get() == "":
        mb.showerror('Error', 'Please select an export format')
        return
    if master.RightUpperFrame.export_quality_entry.get() == "":
        mb.showerror('Error', 'Please select an export quality')
        return
    if os.path.isdir(folder) == False:
        mb.showinfo('Info', 'Export Folder not found')
        return
    

    name_index = master.RightUpperFrame.name_entry.get()
    file = master.RightUpperFrame.export_entry.get()
    quality_dict = {
        'Low': 30,
        'Medium': 50,
        'High': 95
    }
    quality = quality_dict[master.RightUpperFrame.export_quality_entry.get()]
    i =  0
    for record in data:
        i = i + 1
        img = Image.open(master.system_variables['filepath'])  # loading the selected certificate template
        draw = ImageDraw.Draw(img)
        for placeholder in placeholders:
            draw.text((placeholder.x-103, placeholder.y), record[placeholder.header], font=placeholder.font,
                  fill="black")  # setting the co-ordinates to draw the names
        if name_index != "S. No.":
            img.save(f'{folder}/{record[name_index]}.{file}',quality=quality)
        else:
            img.save(f'{folder}/{i}.{file}',quality=quality)

    mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
    open_folder(folder)