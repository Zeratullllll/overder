from ultralytics import YOLO
from PIL import Image
import cv2
import os
model = YOLO('weights/best.pt')

def make_pred(name):
    img_path = Image.open(name)
    image = img_path  # Загружаем изображение

    results = model(img_path)
    return results


def save_yolo_results(results, filename, output_folder):
  """
  Сохраняет результаты предсказания в формате YOLO.

  Args:
    results: Результаты предсказания.
    filename: Имя файла.
    output_folder: Путь к папке для сохранения.
  """

  # Сохранение изображения в папку test/images
  image_path = os.path.join(output_folder, "images", filename)
  #Image.fromarray(results[0]).save(image_path)

  # Сохранение меток в папку test/labels
  label_path = os.path.join(output_folder, "labels", filename[:-4] + ".txt")

  with open(label_path, "w") as f:
    for box in results[0].boxes :
     x1, y1, x2, y2 = map(int, box.xyxy[0])
     x_center=int(x1+x2)//2
     y_center=int(y1+y2)//2
     width=x2-x1
     height=y2-y1
     class_id = 0 # Замените на нужный ID класса

     f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")



# Загрузите вашу модель для предсказания


# Путь к папке с изображениями
screens_folder = "screens"
# Путь к папке для сохранения результатов
output_folder = "test"

# Создание папок для изображений и меток
os.makedirs(os.path.join(output_folder, "images"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "labels"), exist_ok=True)


def thr_f(file_path):
    results = make_pred(file_path)
    save_yolo_results(results, filename, output_folder)

from threading import Thread
from functools import partial
# Перебор файлов в папке screens
for pos,filename in enumerate(os.listdir(screens_folder)):
  if filename.endswith((".png", ".jpg", ".jpeg")):
    file_path = os.path.join(screens_folder, filename)
    thr_f(file_path)
    print(pos,"/")
  
