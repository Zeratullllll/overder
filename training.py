import os
from ultralytics import YOLO

data_yaml = 'img1/data.yaml'

output_dir = 'runs/trains'
os.makedirs(output_dir, exist_ok=True)

model = YOLO('weights/best.pt')

results = model.train(data=data_yaml, imgsz=400, batch=16, epochs=20, project=output_dir)

model.save('cool.pt')




















