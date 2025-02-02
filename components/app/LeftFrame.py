import customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk
import PIL.Image as Resampling
import pandas as pd


from components.app.placeholder import Placeholder



class LeftUpperFrame(ctk.CTkFrame):
    def __init__(self, master, system_variables):
        super().__init__(master)
        self.system_variables = system_variables
        self.master = master
        self.menu_panel_title = ctk.CTkLabel(self, text='Menu Panel',
                                             font=self.system_variables['normalFont'])  ####### ↓↓↓ making widgets ↓↓↓ #######
        self.open_button = ctk.CTkButton(self, text="Open Image", font=self.system_variables['normalFont'], corner_radius=40,
                                         command=self.open_image)  # button to open an image file

        self.data_button = ctk.CTkButton(self, text="Load Data", font=self.system_variables['normalFont'], corner_radius=40,
                                         command=self.load_data)
        self.data_headers = ctk.CTkTextbox(self, width=170, height=120, font=self.system_variables['normalFont'],
                                         wrap='word')
        self.data_headers.configure(state="disabled")
        self.info_label = ctk.CTkLabel(self, text='', font=self.system_variables['normalFont'],
                                       text_color='green')  # label to show info about button clicks & all
        

        self.menu_panel_title.pack(padx=30, pady=10, anchor='center')  ####### ↓↓↓ placing widgets ↓↓↓ #######
        self.open_button.pack(padx=30, pady=10, anchor='center')
        self.data_button.pack(padx=30, pady=10, anchor='center')
        self.data_headers.pack(padx=30, pady=5, anchor='center')
        self.info_label.pack(padx=30, pady=20, anchor='center')

    def load_data(self):
        self.master.system_variables['datafilepath']= filedialog.askopenfilename()
        df = pd.read_csv(self.master.system_variables['datafilepath'])
        self.data_headers.configure(state="normal")
        global headers
        headers = list(df.columns)
        i = 1
        for x in headers:
            if x != "email":
                self.master.placeholders.append(Placeholder(self.master,x,self.master.canvas,x,100,100,i))
                print(x)
                i += 1
                self.data_headers.insert("end", x+"\n")
        self.data_headers.configure(state="disabled")

    def open_image(self):
        if True:
            try:
                self.master.system_variables['filepath'] = filedialog.askopenfilename()
                self.image = Image.open(self.master.system_variables['filepath'])
                width, height = 1200, 857
                self.ratio = min(width / self.image.width, height / self.image.height)
                self.image = self.image.resize(
                    (int(self.image.width * self.ratio), int(self.image.height * self.ratio)), Resampling.BILINEAR)
                self.photo = ImageTk.PhotoImage(self.image)
                self.master.img_on_canvas = self.master.canvas.create_image(0, 0, image=self.photo, anchor="nw")

            except:
                mb.showerror('Error', 'Please select an image')
        
        


class LeftBottomFrame(ctk.CTkFrame):
    def __init__(self, master, system_variables):
        super().__init__(master)
        self.system_variables = system_variables
        self.master = master

        self.placeholder_label = ctk.CTkLabel(self, text='Select a Placeholder', font=self.system_variables['normalFont'])
        self.placeholder_label.pack(padx=30, pady=10, anchor='center')

        self.font_label = ctk.CTkLabel(self, text='Font Size', font=self.system_variables['normalFont'])
        self.font_label.pack(padx=30, pady=10, anchor='center')
        self.font_size = ctk.CTkSlider(self, from_=10, to=100, command=self.change_font_size)
        self.font_size.pack(padx=30, pady=10, anchor='center')
        

    def change_font_size(self,value):
        self.master.selected_placeholder.change_size(value)