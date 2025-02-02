from PIL import Image, ImageTk, ImageFont, ImageDraw









class Placeholder:
    def __init__(self, master,text, canvas, header, x, y, i):
        self.canvas = canvas
        self.header = header
        self.master = master
        self.x = x
        self.y = y
        self.color = "black"
        self.align = "center"
        self.size = 30
        self.font = ImageFont.truetype('components/fonts/Poppins-Medium.ttf', self.size)
        self.width = int(self.font.getlength(self.header))
        self.height = int(self.size*1.1)
        img = Image.new("RGBA", (self.width,self.height))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=self.font, fill=self.color)
        text_window = img.getbbox()
        img = img.crop(text_window)
        self.placeholder_image = ImageTk.PhotoImage(img)
        self.drag_image = self.canvas.create_image(100, 100, image=self.placeholder_image, anchor="nw")
        self.canvas.configure(scrollregion=self.canvas.bbox(self.drag_image))
        self.canvas.tag_bind(self.drag_image, "<Button1-Motion>", self.move, add="+")  ####### ↓↓↓ key binds ↓↓↓ #######
        self.canvas.bind("<Button-3>", self.scan)
        self.canvas.bind("<Button3-Motion>", self.drag)
        self.canvas.tag_bind(self.drag_image, "<Button1-Motion>", self.update_coordinates, add="+")  ####### ↓↓↓ key binds ↓↓↓ #######
        self.canvas.tag_bind(self.drag_image, "<Button-1>", self.select_placeholder) ####### ↓↓↓ key binds ↓↓↓ #######


    def select_placeholder(self, event):
        if self.master.selected_placeholder == self:
            self.master.selected_placeholder = None
            self.master.LeftBottomFrame.placeholder_label.configure(text="Select Placeholder")
            self.master.LeftBottomFrame.font_size.set(30)
            self.master.LeftBottomFrame.font_size.configure(state="disabled")
        else:
            self.master.selected_placeholder = self
            self.master.LeftBottomFrame.placeholder_label.configure(text=f"{self.header} selected")
            self.master.LeftBottomFrame.font_size.set(self.size)
            self.master.LeftBottomFrame.font_size.configure(state="normal")


    def move(self, event):
        self.canvas.moveto(self.drag_image,event.x-self.width,event.y)

    def update_coordinates(self,event):
        self.x = event.x / self.master.LeftUpperFrame.ratio
        self.y = event.y / self.master.LeftUpperFrame.ratio

    def scan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=2)

    def change_size(self,value):
        self.size = int(value)
        self.font = ImageFont.truetype('components/fonts/Poppins-Medium.ttf', self.size)
        self.width = int(self.font.getlength(self.header))
        self.height = int(self.size * 1.1)
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), self.header, font=self.font, fill=self.color)
        text_window = img.getbbox()
        img = img.crop(text_window)
        self.placeholder_image = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.drag_image, image=self.placeholder_image)
        self.canvas.configure(scrollregion=self.canvas.bbox(self.drag_image))
