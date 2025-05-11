#Streamlit YOLO Document Parser UI (PDF & Image)

import streamlit as st
from ultralytics import YOLO
from pdf2image import convert_from_bytes
import cv2
import numpy as np
import os
from PIL import Image
import tempfile

# --- CONFIG ---
st.set_page_config(page_title="Document Parser AI", layout="wide")
st.title("YOLO Document Parser (PDF/Image)")

# Load model
@st.cache_resource
def load_model():
    return YOLO("/home/saugat/yolo/runs/detect/train5/weights/best.pt")  # Replace with your model path

model = load_model()

# Create output folder
def make_output_dir():
    output_dir = tempfile.mkdtemp()
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

output_dir = make_output_dir()

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "jpeg", "png"])

# --- HELPERS ---
def convert_pdf_to_images(uploaded_pdf, dpi=300):
    return convert_from_bytes(uploaded_pdf.read(), dpi=dpi)

def run_yolo_on_image(image_pil, page_num):
    image_np = np.array(image_pil.convert("RGB"))
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    results = model.predict(source=image_bgr, conf=0.25, save=False)
    
    crops = {"table": [], "figure": [], "text": []}
    
    for box_idx, box in enumerate(results[0].boxes):
        cls_id = int(box.cls[0])
        label = model.names[cls_id].lower()
        conf = float(box.conf[0])
        xyxy = list(map(int, box.xyxy[0]))

        x1, y1, x2, y2 = xyxy
        # Clamp coordinates
        h, w = image_np.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        crop = image_np[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        if label in crops:
            crops[label].append(crop)

        # Draw box on original
        cv2.rectangle(image_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_np, f"{label} ({conf:.2f})", (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Save crops
    for label, crop_list in crops.items():
        for i, crop in enumerate(crop_list, start=1):
            file_name = f"{label}_{page_num}_{i}.png"
            file_path = os.path.join(output_dir, file_name)
            Image.fromarray(crop).save(file_path)

    return image_np

# --- MAIN LOGIC ---
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    if uploaded_file.type == "application/pdf":
        st.info("Converting PDF to images...")
        images = convert_from_bytes(file_bytes, dpi=300)
    else:
        images = [Image.open(uploaded_file)]

    st.success(f"{len(images)} page(s)/image(s) to process")

    for idx, img in enumerate(images, start=1):
        st.subheader(f"Page/Image {idx}")
        processed_img = run_yolo_on_image(img, idx)
        st.image(processed_img, caption=f"Parsed Page/Image {idx}", use_column_width=True)

    st.success(f"Finished processing. Cropped regions saved to: {output_dir}")
    st.write("Check the output folder in your environment to view `table_x_x.png`, `figure_x_x.png`, `text_x_x.png`.")

    # --- SHOW OUTPUT FILES IN GRID WITH ACCORDIONS ---
    st.header("Output Cropped Files")

    # List all PNG files in output_dir
    output_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
    if output_files:
        # Group by label
        from collections import defaultdict
        grouped = defaultdict(list)
        for f in output_files:
            label = f.split("_")[0]
            grouped[label].append(f)

        for label in ["table", "figure", "text"]:
            files = grouped.get(label, [])
            if files:
                with st.expander(f"{label.capitalize()} Crops ({len(files)})", expanded=False):
                    cols = st.columns(3)
                    for i, file in enumerate(files):
                        img_path = os.path.join(output_dir, file)
                        with cols[i % 3]:
                            st.image(img_path, caption=file, use_column_width=True)
    else:
        st.info("No crops found to display.")
