import customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageDraw, ImageFont
import PIL.Image as Resampling
import pandas as pd

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from components.app.placeholder import Placeholder
from components.app.utils import open_folder, generate







class App(ctk.CTk):  ####### ↓↓↓ Main Window or Root ↓↓↓ #######
    def __init__(self, system_variables):
        super().__init__()

        self.system_variables = system_variables
        self.title("Certifly")
        self.iconbitmap('components/images/icon.ico')  # certifly window icon
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")  # full screen window
        
        self.title = ctk.CTkLabel(self, text='CERTIFLY', font=('components/fonts/Montserrat-Bold.ttf', 50))  # Setting title
        self.tagline = ctk.CTkLabel(self, text='Certificates on the Go', font=self.system_variables['normalFont'])  # Setting tagline
        self.bind("<Escape>", self.exit_window)  # press 'escape' to exit the window
        
        self.title.pack()  ####### ↓↓↓ placing title, tagline & mode switcher ↓↓↓ #######
        self.tagline.pack()
        self.sideFrame = ctk.CTkFrame(self)  ####### ↓↓↓ Frame to hold the name textbox and related buttons ↓↓↓ #######
        self.sideFrame.pack(side='left', anchor = 'nw',padx=20)

        self.rightFrame = ctk.CTkFrame(self)  ####### ↓↓↓ Frame to Add Buttons in the Right ↓↓↓ #######
        self.rightFrame.pack(side='right', anchor='ne', padx=20)

        self.dark_mode_img = ctk.CTkImage(Image.open('components/images/dark_mode.png'), size=(30, 30))
        self.light_mode_img = ctk.CTkImage(Image.open('components/images/light_mode.png'), size=(30, 30))
        self.mode_switch_button = ctk.CTkButton(self.rightFrame, image=self.light_mode_img, text="", height=20, width=20,
                                                corner_radius=50, fg_color="transparent", command=self.mode_switcher)
        self.mode_switch_button.pack(padx=30,pady=20)
        self.reset_button = ctk.CTkButton(self.rightFrame, text="Reset", font=self.system_variables['normalFont'], corner_radius=40,
                                            command=self.reset)
        self.reset_button.pack(padx=30, pady=20)

        self.button = ctk.CTkButton(self.rightFrame, text="Enter Names", font=self.system_variables['normalFont'], corner_radius=40,
                                    command=self.enter_names)
        self.button.pack(padx=30, pady=10)
        
        

        self.menu_panel_title = ctk.CTkLabel(self.sideFrame, text='Menu Panel',
                                             font=self.system_variables['normalFont'])  ####### ↓↓↓ making widgets ↓↓↓ #######
        self.open_button = ctk.CTkButton(self.sideFrame, text="Open Image", font=self.system_variables['normalFont'], corner_radius=40,
                                         command=self.open_image)  # button to open an image file

        self.data_button = ctk.CTkButton(self.sideFrame, text="Load Data", font=self.system_variables['normalFont'], corner_radius=40,
                                         command=self.load_data)
        self.data_headers = ctk.CTkTextbox(self.sideFrame, width=170, height=120, font=self.system_variables['normalFont'],
                                         wrap='word')
        self.data_headers.configure(state="disabled")

        self.gen_sample_button = ctk.CTkButton(self.sideFrame, text="Generate Sample", font=self.system_variables['normalFont'],
                                               corner_radius=40,
                                               command=self.generate_sample)  # button to open an image file
        self.gen_all_button = ctk.CTkButton(self.sideFrame, text="Generate All", font=self.system_variables['normalFont'], corner_radius=40,
                                            command=self.generate_all)  # button to open an image file

        self.mail_all_button = ctk.CTkButton(self.sideFrame, text="Mail All", font=self.system_variables['normalFont'], corner_radius=40,
                                            command=self.generate_all)

        self.info_label = ctk.CTkLabel(self.sideFrame, text='', font=self.system_variables['normalFont'],
                                       text_color='green')  # label to show info about button clicks & all
        self.menu_panel_title.pack(padx=30, pady=10, anchor='center')  ####### ↓↓↓ placing widgets ↓↓↓ #######
        self.open_button.pack(padx=30, pady=10, anchor='center')
        self.data_button.pack(padx=30, pady=10, anchor='center')
        self.data_headers.pack(padx=30, pady=5, anchor='center')
        self.gen_sample_button.pack(padx=30, pady=10, anchor='center')
        self.gen_all_button.pack(padx=30, pady=10, anchor='center')
        self.mail_all_button.pack(padx=30, pady=10, anchor='center')
        self.info_label.pack(padx=30, pady=20, anchor='center')
        self.canvasFrame = ctk.CTkFrame(self)  ####### ↓↓↓ Frame to hold canvas and dragging & opened image ↓↓↓ #######
        self.canvasFrame.pack(side="right", padx=50)
        self.canvas = ctk.CTkCanvas(self.canvasFrame, width=1200,
                                    height=857)  # canvas to display dragging & opened image
        self.canvas.grid(row=0, column=0    , sticky="nsew")

        self.placeholders = []

    def reset(self):
        self.data_headers.configure(state="normal")
        self.data_headers.delete("1.0", "end")
        self.canvas.delete("all")
        self.placeholders = []
        
    def load_data(self):
        self.system_variables['datafilepath']= filedialog.askopenfilename()
        df = pd.read_csv(self.system_variables['datafilepath'])
        self.data_headers.configure(state="normal")
        global headers
        headers = list(df.columns)
        i = 1
        for x in headers:
            if x != "email":
                self.placeholders.append(Placeholder(self,self.canvas,x,100,100,i))
                print(x)
                i += 1
                self.data_headers.insert("end", x+"\n")
        self.data_headers.configure(state="disabled")




    def non_empty_textbox(self):
        if len(self.name_entry.get("1.0",
                                   "end")) == 1:  # checking if text box is empty, 1 denotes a (end-of-line(EOL), newline character, invisible character)
            mb.showerror('Name error', 'Please add some names')
        else:
            return True

    global name_list
    name_list = []

    def enter_names(self):
        if self.non_empty_textbox():
            global name_list
            names = self.name_entry.get("1.0", "end").upper()  # getting all texts from textbox & changing to uppercase
            name_list = names.splitlines()  # splitting texts by line
            self.info_label.configure(text='Names Entered')
            self.after(3000, self.clear_label)

    def open_image(self):
        if True:
            try:
                self.system_variables['filepath'] = filedialog.askopenfilename()
                self.image = Image.open(self.system_variables['filepath'])
                width, height = 1200, 857
                self.ratio = min(width / self.image.width, height / self.image.height)
                self.image = self.image.resize(
                    (int(self.image.width * self.ratio), int(self.image.height * self.ratio)), Resampling.BILINEAR)
                self.photo = ImageTk.PhotoImage(self.image)
                self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

            except:
                mb.showerror('Error', 'Please select an image')

    global x, y  # for checking in generate functions
    x = y = None

    '''
    def show_coordinates(self, event):
        global x, y  # for changing global values of x & y
        x = event.x / self.ratio
        y = event.y / self.ratio
        self.coord_label.configure(text=f"X: {round(x, 2)}, Y: {round(y, 2)}")
    '''

    def gen_err_check(self):
        if len(name_list) == 0:
            mb.showerror('Name error', 'Please add some names')
        elif x is None:  # no check for 'y' as it is selected with 'x'
            mb.showerror('Coordinates error', "Drag & place 'Sample Name' to set coordinates")
        else:
            return True

    def generate_sample(self):
        try:
            data = []
            record = {}
            for placeholder in self.placeholders:
                record[placeholder.header] = placeholder.header

            data.append(record)

            generate(self,self.placeholders, data)
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
            open_folder()
        except:
            mb.showerror('Error', 'Unknown error occured')

    def generate_all(self):
        try:
            data = pd.read_csv(self.system_variables['datafilepath']).to_dict('records')

            generate(self,self.placeholders, data)
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
            open_folder()
        except:
            mb.showerror('Error', 'Unknown error occured')


    global is_dark
    is_dark = False  # initializing the variable


    def email_all(self):
        data = pd.read_csv(self.system_variables['datafilepath']).to_dict('records')
        fromaddr = "EMAIL address of the sender"
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, "Password_of_the_sender")

        for record in data:

            toaddr = record['email']
            # instance of MIMEMultipart
            msg = MIMEMultipart()

            msg['From'] = fromaddr

            # storing the receivers email address
            msg['To'] = toaddr

            msg['Cc'] = ['email1','email2']

            # storing the subject
            msg['Subject'] = "Subject of the Mail"

            # string to store the body of the mail
            body = "Body_of_the_mail"

            img = Image.open(self.system_variables['filepath'])  # loading the selected certificate template
            draw = ImageDraw.Draw(img)
            for placeholder in self.placeholders:
                draw.text((placeholder.x - 103, placeholder.y), record[placeholder.header],
                          font=ImageFont.truetype('components/fonts/Poppins-Medium.ttf', 30),
                          fill="black")  # setting the co-ordinates to draw the names
            img.save(
                r'generated_certificates/' + record['name'] + ".png")

            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))

            # open the file to be sent
            filename = 'generated_certificates/' + record['name'] + ".png"
            attachment = open("Path of the file", "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)

            # Converts the Multipart msg into a string
            text = msg.as_string()

            # sending the mail
            s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()


    def mode_switcher(self):
        global is_dark
        is_dark = not is_dark  # toggle the value of is_dark
        if is_dark:
            ctk.set_appearance_mode("light")
            self.mode_switch_button.configure(image=self.dark_mode_img)
            self.canvas.configure(bg='#dbdbdb')
        else:
            ctk.set_appearance_mode("dark")  # Modes: system, light, dark
            self.mode_switch_button.configure(image=self.light_mode_img)

    def move(self, event):
        self.canvas.moveto(self.drag_image, event.x - 103, event.y)

    def scan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=2)

    def display_coords(self, event):
        self.coord_label.configure(text=f"X: {event.x} Y:{event.y}")

    def clear_label(self):
        self.info_label.configure(text='')  # to remove any text from info label

    def exit_window(self, event=None):
        self.destroy()  # to exit the window