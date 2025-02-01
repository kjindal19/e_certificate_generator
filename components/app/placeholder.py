from PIL import Image, ImageTk









class Placeholder:
    def __init__(self, master, canvas, header, x, y, i):
        self.canvas = canvas
        self.header = header
        self.master = master
        self.x = x
        self.y = y
        self.placeholder_image = ImageTk.PhotoImage(Image.open(f"components/images/text{i}.png"))
        self.drag_image = self.canvas.create_image(100, 100, image=self.placeholder_image, anchor="nw")
        self.canvas.configure(scrollregion=self.canvas.bbox(self.drag_image))
        self.canvas.tag_bind(self.drag_image, "<Button1-Motion>", self.move, add="+")  ####### ↓↓↓ key binds ↓↓↓ #######
        self.canvas.bind("<Button-3>", self.scan)
        self.canvas.bind("<Button3-Motion>", self.drag)
        self.canvas.tag_bind(self.drag_image, "<Button1-Motion>", self.update_coordinates, add="+")  ####### ↓↓↓ key binds ↓↓↓ #######

    def move(self, event):
        self.canvas.moveto(self.drag_image,event.x-103,event.y)

    def update_coordinates(self,event):
        self.x = event.x / self.master.ratio
        self.y = event.y / self.master.ratio

    def scan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=2)
