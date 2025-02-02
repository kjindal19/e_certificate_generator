from components.app import App
import os, subprocess, random, customtkinter as ctk
from tkinter import filedialog, messagebox as mb



ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark. ### Window theme
ctk.set_default_color_theme(
    "green")  # Themes: blue (default), dark-blue, green. ### Used for default button colors & other

normalFont = ('components/fonts/Montserrat-Regular.ttf', 17)  # used many times for buttons, small headings etc...



System_Variables = {
    "normalFont" : ('components/fonts/Montserrat-Regular.ttf', 17),
    "mode": False, # False for light mode, True for dark mode


}

app = App(System_Variables)
app.mainloop()