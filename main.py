from components.app import App
import os, subprocess, random, customtkinter as ctk
from tkinter import filedialog, messagebox as mb



ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark. ### Window theme
ctk.set_default_color_theme(
    "green")  # Themes: blue (default), dark-blue, green. ### Used for default button colors & other

normalFont = ('components/fonts/Montserrat-Regular.ttf', 17)  # used many times for buttons, small headings etc...



System_Variables = {
    "H1Font" : ('components/fonts/Montserrat-Bold.ttf', 50),
    "H2Font" : ('components/fonts/Montserrat-Bold.ttf', 30),
    "H3Font" : ('components/fonts/Montserrat-Bold.ttf', 20),
    "H4Font" : ('components/fonts/Montserrat-Bold.ttf', 17),
    "PFont" : ('components/fonts/Montserrat-Regular.ttf', 17),
    "SFont" : ('components/fonts/Montserrat-Regular.ttf', 12),
    "mode": False, # False for light mode, True for dark mode
    "filepath": "",
    "datafilepath": "",


}

app = App(System_Variables)
app.mainloop()