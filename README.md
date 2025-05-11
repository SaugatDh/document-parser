# 🧾 YOLO Document Parser

An AI-powered tool that uses a fine-tuned YOLOv8 model to detect layout components in documents (e.g., titles, paragraphs, tables). Converts PDFs into structured data.

---

## 🌟 Features

- 🔍 Detects structural elements in multi-page PDFs
- 🖼 Converts PDF pages to images (Poppler + `pdf2image`)
- 🤖 YOLOv8-based layout detection
- 🎯 Bounding box visualization (optional)
- 📤 Outputs structured JSON per page

---

## ⚙️ Requirements

- **Python 3.8+**
- **Poppler** (required for `pdf2image`):
  - **Ubuntu:** `sudo apt install poppler-utils`
  - **macOS:** `brew install poppler`
  - **Windows:** [Download & add to PATH](https://github.com/oschwartz10612/poppler-windows/releases/)

---

## 🚀 Setup

```bash
git clone <repo-url>
cd yolo-document-parser
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

🔁 Place your best.pt model file in the root directory.

🤝 Acknowledgements

Built using:

    Ultralytics YOLOv8

    pdf2image, OpenCV, Matplotlib


---

### 📦 `requirements.txt`

```txt
ultralytics==8.0.198
opencv-python==4.9.0.80
matplotlib==3.8.4
pdf2image==1.16.3
numpy==1.26.4
