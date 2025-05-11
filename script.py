import os
import json

# Root of your dataset
root_dir = "/home/saugat/small-publaynet-wds"

# Category mapping (adjust as needed)
category_map = {
    "text": 0,
    "title": 1,
    "list": 2,
    "table": 3,
    "figure": 4
}

# Walk through all subfolders
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".json"):
            json_path = os.path.join(subdir, file)
            with open(json_path, "r") as f:
                data = json.load(f)

            width = data["width"]
            height = data["height"]
            annotations = data.get("annotations", [])

            # Output .txt path in same folder as .json
            yolo_label_path = os.path.join(subdir, file.replace(".json", ".txt"))

            with open(yolo_label_path, "w") as out_file:
                for ann in annotations:
                    x, y, w, h = ann["bbox"]
                    x_center = (x + w / 2) / width
                    y_center = (y + h / 2) / height
                    norm_w = w / width
                    norm_h = h / height

                    category_name = ann["category_name"]
                    class_id = category_map.get(category_name, 0)  # default to 0

                    out_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}\n")

print("✅ All JSON files converted to YOLO format.")
