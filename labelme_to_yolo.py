import json
import os

def labelme_to_yolo(json_file, output_dir, class_mapping):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    img_width = data['imageWidth']
    img_height = data['imageHeight']
    
    txt_filename = os.path.splitext(os.path.basename(json_file))[0] + '.txt'
    txt_path = os.path.join(output_dir, txt_filename)
    
    with open(txt_path, 'w') as f:
        for shape in data['shapes']:
            class_name = shape['label']
            class_id = class_mapping[class_name]
            points = shape['points']
            x_min = min(p[0] for p in points)
            x_max = max(p[0] for p in points)
            y_min = min(p[1] for p in points)
            y_max = max(p[1] for p in points)
            x_center = ((x_min + x_max) / 2) / img_width
            y_center = ((y_min + y_max) / 2) / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# Exemplo de uso (execute no terminal do VS Code):
class_mapping = {"classe1": 0, "classe2": 1}  # Substitua com suas classes
output_dir = "dataset\\labels"
os.makedirs(output_dir, exist_ok=True)

for json_file in os.listdir("dataset\\images"):
    if json_file.endswith(".json"):
        labelme_to_yolo(os.path.join("dataset\\images", json_file), output_dir, class_mapping)