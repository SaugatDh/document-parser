# Document Parser AI

## Description
The Document Parser AI is a powerful tool designed to automatically detect and extract key elements from PDF documents and images using a fine-tuned YOLO (You Only Look Once) object detection model. It provides an intuitive web interface built with Streamlit, allowing users to upload documents and visualize the parsed results, including cropped regions of identified elements like text, tables, figures, titles, and lists.

## How it Works
The project operates in several key stages:

1.  **Data Preparation & Model Training:**
    *   The `script.py` utility converts raw annotation data (e.g., from datasets like PubLayNet) from JSON format into the YOLO-compatible `.txt` label format. This involves normalizing bounding box coordinates and mapping semantic categories (like "text", "table", "figure") to numerical class IDs.
    *   The `data.yaml` file configures the dataset, specifying paths for training and validation images, the total number of classes, and their corresponding names.
    *   A YOLOv8 model is trained or fine-tuned on this prepared dataset to learn to identify document elements. The `yolov8n.pt` and `best.pt` files represent the trained model weights.

2.  **Document Processing (Web Application):**
    *   The core functionality is exposed through a Streamlit web application (`app.py`).
    *   Users upload PDF or image files via the web interface.
    *   For PDF inputs, each page is automatically converted into an image.
    *   The trained YOLO model then processes each image, performing real-time object detection to identify and localize various document components.
    *   Detected elements are highlighted with bounding boxes and confidence scores on the displayed images.
    *   Crucially, the application automatically crops each identified element (e.g., a table, a figure, a text block) and saves it as a separate PNG image file in a temporary directory, categorized by element type (e.g., `table_1_1.png`, `figure_2_3.png`).
    *   The web interface provides a visual summary of the processed pages and an interactive gallery of the extracted cropped elements.

3.  **Annotation Verification (Utility):**
    *   The `check.py` script serves as a standalone utility for dataset verification. It allows developers to visualize the bounding box annotations from YOLO `.txt` label files overlaid on their corresponding images. This is invaluable for ensuring the accuracy and quality of the training data.
