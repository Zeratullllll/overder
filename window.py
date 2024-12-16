import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
import keyboard
import cv2
import numpy as np
wisible=True
glob_x=0
glob_y=0
def on_shift(root,event):
    if event.name=="shift":
        global wisible,glob_y,glob_x
        if wisible:
            glob_x=root.winfo_x()
            glob_y=root.winfo_y()
            x=2000
            y=-1000
            root.geometry("+{x}+{y}".format(x=x, y=y))
            wisible=False
        else:
            wisible=True
            root.geometry("+{x}+{y}".format(x=glob_x, y=glob_y))
class DraggableWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        keyboard.on_press(partial(on_shift,self))
        self.wm_attributes("-topmost", 1)
        self.size=400
        self.geometry(f"{str(self.size)}x{str(self.size)}")
        self.overrideredirect(True)  # Убираем рамку окна
        self.attributes('-alpha', 1)  # Устанавливаем прозрачность 50%
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<Shift_L>", partial(on_shift,self))
        self.bind("<Shift_R>", partial(on_shift,self))
        self.offset_x = 0
        self.offset_y = 0
        self.create_bg()
    def create_bg(self):
        #self.canvas = tk.Canvas(self, width=300, height=300)
        #self.canvas.pack()
        self.original_image = Image.open("test.png")
        self.original_image = self.original_image.resize((self.size, self.size) )
        #self.canvas_bg= ImageTk.PhotoImage(self.original_image)
        #self.canvas_bg=tk.PhotoImage(file="test.png")
        #self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_bg)
        self.image= ImageTk.PhotoImage(self.original_image)
        self.label = tk.Label(self, image=self.image)
        self.label.place(x=-2,y=-2)
    def update_bg(self, pil_image):
        try:
            # Изменение размера изображения
            pil_image = pil_image.resize((self.size, self.size))

            # Обновление изображения на метке
            self.image = ImageTk.PhotoImage(pil_image)
            self.label.config(image=self.image)
            self.label.image = self.image
        except Exception as e:
            print(f"Ошибка при обновлении фона: {e}")
    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
    def stop_move(self, event):
        self.offset_x = 0
        self.offset_y = 0
    def on_motion(self, event):
        x = self.winfo_pointerx() - self.offset_x
        y = self.winfo_pointery() - self.offset_y
        self.geometry("+{x}+{y}".format(x=x, y=y))
