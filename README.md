# 👁️ ghostframe

> Images talk. This listens. A clean, zero-bloat image forensics utility.

A minimalist command-line forensic utility designed to recursively scan files, extract embedded EXIF metadata matrices, isolate tracking tags, and generate instant Google Maps hyperlinks from geographical coordinates.

---

## 🛠️ Installation

Open your terminal and run the following commands to clone the tool and install the necessary dependencies:

```bash
# 1. Clone the repository
git clone https://github.com/Imthatmorguen/ghostframe.git

# 2. Move into the project directory
cd ghostframe

# 3. Install the required image library (Pillow)
pip install -r requirements.txt
```

---

## 📖 Complete Tutorial & Usage Guide

When you launch `ghostframe.py`, it will ask you if you want to output the results directly to your **Terminal Screen** (best for a quick look) or save them into a **Text File** named `exif_analysis.txt` (best for large batches of images).

### 1. The Default Method (Bulk Scan)
By default, the script automatically looks for a folder named `images` in the exact same directory as the script.

* **Step 1:** Inside your `ghostframe` folder, make sure a directory named `images` exists. If it doesn't, create it:
  ```bash
  mkdir images
  ```
* **Step 2:** Drop your target photos (`.jpg`, `.jpeg`, `.tiff`) directly inside that `images` folder. You can use your file explorer or move them via terminal:
  ```bash
  cp ~/Downloads/sample.jpg ~/ghostframe/images/
  ```
* **Step 3:** Run the script without any arguments:
  ```bash
  python3 ghostframe.py
  ```

### 2. Scanning a Single Specific Image File
If you don't want to move your photos into the local directory, you can use the `-p` (or `--path`) flag to point directly to any individual file on your system:

```bash
python3 ghostframe.py -p ~/Downloads/evidence_photo.jpg
```

### 3. Scanning a Completely Different Folder
If you have an entire folder of pictures elsewhere (like an external drive or your main documents vault), pass the directory path using the `-p` flag. The tool will automatically dig through that folder and any subfolders inside it:

```bash
python3 ghostframe.py -p /path/to/target_directory/
```

---

## 📄 Core Specifications
* **Supported Formats:** `.jpg`, `.jpeg`, `.tiff`, `.tif` (Note: Social media platforms like WhatsApp, X/Twitter, and Instagram automatically wipe this data upon upload).
* **Geotargeting:** Extracts GPS components (`GPSLatitude`, `GPSLongitude`, and their Cardinal References) to calculate standard decimal coordinates.

## ⚖️ Disclaimer
This tool is strictly for educational, administrative auditing, and authorized digital forensics research. The author assumes zero liability for unauthorized deployment. See accompanying `LICENSE` file.
# ghostframe
See what your pictures are hiding. A clean, zero-bloat image forensics utility.
