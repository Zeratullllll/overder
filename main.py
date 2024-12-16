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
def save_n(num):
    with open('now_num.txt', 'w') as file:
        file.write(str(num))

def load_n():
    try:
        with open('now_num.txt', 'r') as file:
            num = file.read()
            return int(num)  # Преобразуем строку в целое число
    except FileNotFoundError:
        print("Файл не найден.")
        return None
    except ValueError:
        print("Ошибка при преобразовании строки в число.")
        return None

def inc_n():
    global num
    num+=1




def take_screenshot():
    # Убедимся, что директория существует
    directory = "img"
    if not os.path.exists(directory):
        os.makedirs(directory)  # Создаем директорию, если её нет
    # Делаем скриншот и сохраняем его
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    left = (width - 600) // 2  # 300 пикселей влево от центра
    top = (height - 600) // 2  # 300 пикселей вверх от центра
    right = left + 600  # 600 пикселей по ширине
    bottom = top + 600  # 600 пикселей по высоте
    # Обрезать изображение
    screenshot = screenshot.crop((left, top, right, bottom))
    """
    screenshot.save(file_path)
    inc_n()
    save_n(num)
    print(f"Скриншот сохранён как {file_path}")
    """
    return screenshot



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
        fl=True
        x1, y1, x2, y2 = map(int, bbox.xyxy[0])
        check_boxes([x1,y1,x2,y2])
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

    img_path="img/teeest.png"
    # Сохраняем изображение с наложенными bbox
    #cv2.imwrite(img_path, image)

    return image
    #

def check_boxes(bbox_pos):
    width, height=1920,1080
    left = (width - 600) // 2  # 300 пикселей влево от центра
    top = (height - 600) // 2  # 300 пикселей вверх от центра
    # Прибавляем left и top к координатам bbox_pos
    x1, y1, x2, y2 = bbox_pos
    x1 += left
    x2 += left
    y1 += top
    y2 += top

    # Получаем текущие координаты курсора
    cursor_x, cursor_y = pyautogui.position()

    # Проверяем, находится ли курсор внутри bbox
    if x1 <= cursor_x <= x2 and y1 <= cursor_y <= y2:
        pyautogui.click()  # Нажимаем ЛКМ



from functools import partial
from multiprocessing import Process
import tkinter as tk
from window import DraggableWindow
from time import sleep
def thread_f():
    while(1):
        try:
            img = take_screenshot()
            img = m_pred(img, model)
            root.update_bg(img)
        except Exception as e:
            sleep(0.4)
            print(e)




model = YOLO('weights/best.pt')

root=DraggableWindow()


t=Thread(target=thread_f)
t.start()
root.mainloop()



"""
# Настраиваем слушателя
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
"""

"""
# Укажите путь к изображению
img_path = 'test.png'
image = cv2.imread(img_path)  # Загружаем изображение

# Выполняем предсказание
results = model(img_path)

# Извлечение предположенных bbox и их наложение на изображение
for bbox in results[0].boxes:
    x1, y1, x2, y2 = map(int, bbox.xyxy[0])
    conf = bbox.conf[0]  # Уверенность
    label = int(bbox.cls[0])  # Метка класса

    # Наносим bbox на изображение
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(image, f'Class: {label}, Conf: {conf:.2f}', (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Сохраняем изображение с наложенными bbox
cv2.imwrite("_" + img_path, image)
print(f"Изображение сохранено как _{img_path}")
"""


"""
import torch
# Проверка доступности GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Используемое устройство: {device}")
"""