import customtkinter as ctk
import customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageDraw, ImageFont
import PIL.Image as Resampling
import pandas as pd
from components.app.utils import open_folder, generate









class RightUpperFrame(ctk.CTkFrame):
    def __init__(self, master, system_variables):
        super().__init__(master)
        self.system_variables = system_variables
        self.master = master

        self.dark_mode_img = ctk.CTkImage(Image.open('components/images/dark_mode.png'), size=(30, 30))
        self.light_mode_img = ctk.CTkImage(Image.open('components/images/light_mode.png'), size=(30, 30))
        self.mode_switch_button = ctk.CTkButton(self, image=self.light_mode_img, text="", height=20, width=20,
                                                corner_radius=50, fg_color="transparent", command=self.mode_switcher)
        self.mode_switch_button.pack(padx=30,pady=20)
        self.reset_button = ctk.CTkButton(self, text="Reset", font=self.system_variables['normalFont'], corner_radius=40,
                                            command=self.reset)
        self.reset_button.pack(padx=30, pady=20)

        self.button = ctk.CTkButton(self, text="Enter Names", font=self.system_variables['normalFont'], corner_radius=40,
                                    command=self.enter_names)
        self.button.pack(padx=30, pady=10)


    def mode_switcher(self):
        self.system_variables['mode'] = not self.system_variables['mode']
        self.system_variables['mode'] = not self.system_variables['mode']  # toggle the value of self.system_variables['mode']
        if self.system_variables['mode']:
            ctk.set_appearance_mode("light")
            self.mode_switch_button.configure(image=self.dark_mode_img)
            self.master.canvas.configure(bg='#dbdbdb')
        else:
            ctk.set_appearance_mode("dark")  # Modes: system, light, dark
            self.mode_switch_button.configure(image=self.light_mode_img)

    def reset(self):
        self.master.LeftUpperFrame.data_headers.configure(state="normal")
        self.master.LeftUpperFrame.data_headers.delete("1.0", "end")
        self.master.canvas.delete("all")
        self.master.placeholders = []

    def enter_names(self):
        if self.non_empty_textbox():
            global name_list
            names = self.name_entry.get("1.0", "end").upper()  # getting all texts from textbox & changing to uppercase
            name_list = names.splitlines()  # splitting texts by line
            self.info_label.configure(text='Names Entered')
            self.after(3000, self.clear_label)

    def non_empty_textbox(self):
        if len(self.name_entry.get("1.0",
                                   "end")) == 1:  # checking if text box is empty, 1 denotes a (end-of-line(EOL), newline character, invisible character)
            mb.showerror('Name error', 'Please add some names')
        else:
            return True








class RightBottomFrame(ctk.CTkFrame):
    def __init__(self, master, system_variables):
        super().__init__(master)
        self.system_variables = system_variables
        self.master = master
        self.gen_sample_button = ctk.CTkButton(self, text="Generate Sample", font=self.system_variables['normalFont'],
                                               corner_radius=40,
                                               command=self.generate_sample)  # button to open an image file
        self.gen_all_button = ctk.CTkButton(self, text="Generate All", font=self.system_variables['normalFont'], corner_radius=40,
                                            command=self.generate_all)  # button to open an image file

        self.mail_all_button = ctk.CTkButton(self, text="Mail All", font=self.system_variables['normalFont'], corner_radius=40,
                                            command=self.generate_all)
        
        self.gen_sample_button.pack(padx=30, pady=10, anchor='center')
        self.gen_all_button.pack(padx=30, pady=10, anchor='center')
        self.mail_all_button.pack(padx=30, pady=10, anchor='center')

    def gen_err_check(self):
        if len(name_list) == 0:
            mb.showerror('Name error', 'Please add some names')
        elif "x" is None:  # no check for 'y' as it is selected with 'x'
            mb.showerror('Coordinates error', "Drag & place 'Sample Name' to set coordinates")
        else:
            return True

    def generate_sample(self):
        try:
            data = []
            record = {}
            for placeholder in self.master.placeholders:
                record[placeholder.header] = placeholder.header

            data.append(record)

            generate(self,self.master.placeholders, data)
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
            open_folder()
        except:
            mb.showerror('Error', 'Unknown error occured')

    def generate_all(self):
        try:
            data = pd.read_csv(self.master.system_variables['datafilepath']).to_dict('records')

            generate(self,self.master.placeholders, data)
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
            open_folder()
        except:
            mb.showerror('Error', 'Unknown error occured')
