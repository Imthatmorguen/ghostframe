# 👁️ ghostframe
> Images talk. This listens. A clean, zero-bloat image forensics utility.

A minimalist, cross-platform command-line tool for scanning, analyzing (via `ghostframe.py`), and sanitizing metadata in `.jpg`, `.jpeg`, `.png`, `.webp`, and `.tiff` files.

---

## 🚀 Features (v1.2.0)
*   **Dual Mode Engine:** Switch between Metadata Extraction (Geo-location) or Permanent Metadata Wiping.
*   **Cross-Platform:** Native support for **Linux, macOS, and Windows**.

---

## 🛠️ Installation & Usage
```bash
git clone https://github.com/Imthatmorguen/ghostframe.git
cd ghostframe
pip install -r requirements.txt
```

Run with `python3 ghostframe.py` and choose from the interactive menu:
1.  **Read:** Analyze metadata and generate `exif_analysis.txt`.
2.  **Wipe:** Permanently clear EXIF data.

**Targeting Files:** Run `python3 ghostframe.py [path/to/image_or_folder]` to analyze specific files outside the default `images` folder.

---

## 🕵️‍♂️ Preserving Metadata (App Bypasses)
To keep metadata intact when sharing, send as **Documents/Files** (not Photos) on WhatsApp, Telegram, and Signal.

---

## ⚖️ Disclaimer
This tool is for educational and authorized forensic use only. See `LICENSE` for details.
