from components.app import App
import os, subprocess, random, customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageDraw, ImageFont
import PIL.Image as Resampling
import pandas as pd

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark. ### Window theme
ctk.set_default_color_theme(
    "green")  # Themes: blue (default), dark-blue, green. ### Used for default button colors & other

normalFont = ('components/fonts/Montserrat-Regular.ttf', 17)  # used many times for buttons, small headings etc...



System_Variables = {
    "normalFont" : ('components/fonts/Montserrat-Regular.ttf', 17)


}

app = App(System_Variables)
app.mainloop()