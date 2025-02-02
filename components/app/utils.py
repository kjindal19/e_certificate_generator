import os
from PIL import Image, ImageDraw, ImageFont


def open_folder():
    if os.path.isdir("generated_certificates"):
        os.startfile('generated_certificates')


def folder_check():  # Creates a new 'generated_certificates' folder if not already present
    if os.path.isdir("generated_certificates"):
        os.system("rmdir /s /q generated_certificates")  # not recommended to use
        os.mkdir("generated_certificates")
    else:
        os.mkdir("generated_certificates")


def generate(master,placeholders,data):
    folder_check()
    for record in data:
        img = Image.open(master.system_variables['filepath'])  # loading the selected certificate template
        draw = ImageDraw.Draw(img)
        for placeholder in placeholders:
            draw.text((placeholder.x-103, placeholder.y), record[placeholder.header], font=ImageFont.truetype('components/fonts/Poppins-Medium.ttf', 30),
                  fill="black")  # setting the co-ordinates to draw the names
        img.save(
            r'generated_certificates/' + record['name'] + ".png")

