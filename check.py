import cv2
import os

def draw_yolo_boxes(image_path, label_path, class_names):
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    if not os.path.exists(label_path):
        print(f"Label file not found: {label_path}")
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center_norm = float(parts[1])
            y_center_norm = float(parts[2])
            width_norm = float(parts[3])
            height_norm = float(parts[4])

            # Denormalize
            x_center = x_center_norm * w
            y_center = y_center_norm * h
            box_width = width_norm * w
            box_height = height_norm * h

            x_min = int(x_center - box_width / 2)
            y_min = int(y_center - box_height / 2)
            x_max = int(x_center + box_width / 2)
            y_max = int(y_center + box_height / 2)

            label_name = class_names[class_id]
            color = (0, 255, 0) # Green for example

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(image, label_name, (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Annotations", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # --- Configuration ---
    dataset_root = "/home/saugat/yolo/dataset_root" # Change to your dataset path
    image_folder = os.path.join(dataset_root, "images", "train") # or val/test
    label_folder = os.path.join(dataset_root, "labels", "train") # or val/test

    # Load class names from your data.yaml (or define manually)
    # For simplicity here, let's define manually:
    class_names_from_yaml = ['title', 'paragraph', 'figure'] # MAKE SURE THIS MATCHES YOUR data.yaml

    # --- Iterate and display a few ---
    num_images_to_check = 5
    for i, img_name in enumerate(os.listdir(image_folder)):
        if i >= num_images_to_check:
            break
        if img_name.endswith(".png"):
            base_name = os.path.splitext(img_name)[0]
            image_path = os.path.join(image_folder, img_name)
            label_path = os.path.join(label_folder, base_name + ".txt")
            print(f"Checking: {image_path}")
            draw_yolo_boxes(image_path, label_path, class_names_from_yaml)