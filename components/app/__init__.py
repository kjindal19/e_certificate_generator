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

from components.app.LeftFrame import LeftUpperFrame, LeftBottomFrame
from components.app.RightFrame import RightUpperFrame, RightBottomFrame








class App(ctk.CTk):  ####### ↓↓↓ Main Window or Root ↓↓↓ #######
    def __init__(self, system_variables):
        super().__init__()

        self.system_variables = system_variables
        self.title("Certifly")
        self.iconbitmap('components/images/icon.ico')  # certifly window icon
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")  # full screen window

        self.title = ctk.CTkLabel(self, text='E-Certify', font=('components/fonts/Montserrat-Bold.ttf', 50))  # Setting title
        self.title.grid(row=0,column=1,sticky='new')  ####### ↓↓↓ placing title, tagline & mode switcher ↓↓↓ #######
        
        self.tagline = ctk.CTkLabel(self, text='E-Certificates made easy!', font=self.system_variables['normalFont'])  # Setting tagline
        self.bind("<Escape>", self.exit_window)  # press 'escape' to exit the window
        
        self.tagline.grid(row=1,column=1,sticky='new')
        self.LeftUpperFrame = LeftUpperFrame(self,system_variables)  ####### ↓↓↓ Frame to hold the name textbox and related buttons ↓↓↓ #######
        self.LeftUpperFrame.grid(row=2,column=0,sticky='nwes',padx = 30,pady=10)

        self.LeftBottomFrame = LeftBottomFrame(self,system_variables)  ####### ↓↓↓ Frame to hold Font Settings ↓↓↓ #######
        self.LeftBottomFrame.grid(row=3,column=0,sticky='nwes',padx = 30,pady=20)

        self.RightFrame = RightUpperFrame(self,system_variables)  ####### ↓↓↓ Frame to Add Buttons in the Right ↓↓↓ #######
        self.RightFrame.grid(row=2,column=2,sticky='nwes',padx = 30,pady=20)

        self.RightBottomFrame = RightBottomFrame(self,system_variables) ####### ↓↓↓ Frame to hold Export Buttons ↓↓↓ #######
        self.RightBottomFrame.grid(row=3,column=2,sticky='nwes',padx = 30,pady=20)

        
        self.canvasFrame = ctk.CTkFrame(self)  ####### ↓↓↓ Frame to hold canvas and dragging & opened image ↓↓↓ #######
        self.canvasFrame.grid(row=2,column=1,sticky='nsew',pady=10,rowspan=2)
        self.canvas = ctk.CTkCanvas(self.canvasFrame, width=1200,
                                    height=857)  # canvas to display dragging & opened image
        self.canvas.grid(row=0, column=0    , sticky="nsew")

        self.placeholders = []
        self.selected_placeholder = None

    
        




   
    global name_list
    name_list = []

    
    

    global x, y  # for checking in generate functions
    x = y = None

    '''
    def show_coordinates(self, event):
        global x, y  # for changing global values of x & y
        x = event.x / self.ratio
        y = event.y / self.ratio
        self.coord_label.configure(text=f"X: {round(x, 2)}, Y: {round(y, 2)}")
    '''

    


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