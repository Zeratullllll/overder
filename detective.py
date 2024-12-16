import keyboard
import pyautogui
from threading import Thread
import os
import numpy as np

from pynput import mouse
from ultralytics import YOLO
from PIL import Image
import cv2
from threading import Thread
def m_pred(img_path,model):
    # Укажите путь к изображению
    #img_path = 'test.png'
    image = img_path  # Загружаем изображение

    # Выполняем предсказание
    results = model(img_path)


    image_np = np.array(image)



    # Преобразование из RGB (Pillow) в BGR (OpenCV)
    image= cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    
    fl=True
    # Извлечение предположенных bbox и их наложение на изображение
    for bbox in results[0].boxes:
        fl=False
        x1, y1, x2, y2 = map(int, bbox.xyxy[0])
        conf = bbox.conf[0]  # Уверенность
        label = int(bbox.cls[0])  # Метка класса

        # Наносим bbox на изображение
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, f'Class: {label}, Conf: {conf:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    if fl==True:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Создание объекта Pillow
        image = Image.fromarray(image_rgb)

    img_path="1/gol21.png"
    # Сохраняем изображение с наложенными bbox
    cv2.imwrite(img_path,image)
    print("!@#")


    return image
def take_screenshot():


    # Убедимся, что директория существует

    # Делаем скриншот и сохраняем его
    screenshot = Image.open("1/gol.jpg")

    width, height = screenshot.size


    """
    screenshot.save(file_path)
    inc_n()
    save_n(num)
    print(f"Скриншот сохранён как {file_path}")
    """
    return screenshot


from functools import partial
from multiprocessing import Process
import tkinter as tk
from window import DraggableWindow
from time import sleep
import keyboard

def key_f(k):
    if k.name=="k":

        t = Thread(target=thread_f)
        t.start()
keyboard.on_press(key_f)
model = YOLO('weights/best.pt')
def thread_f():
    while(1):
        try:
            img = pyautogui.screenshot()
            img = m_pred(img, model)
            break
        except Exception as e:
            sleep(0.4)
            print(e)

keyboard.wait()