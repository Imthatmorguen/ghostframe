import os
import shutil
from ghostframe.i18n import t


SUPPORTED = (".jpg", ".jpeg", ".png", ".webp")


# -------------------------
# SCAN PATH (LANG-AWARE)
# -------------------------

def scan_path(path, lang="en"):
    if not os.path.exists(path):
        print(t(lang, "path_not_found"), path)
        return

    files = []

    # single file
    if os.path.isfile(path):
        files = [path]

    # folder scan
    else:
        for root, _, fs in os.walk(path):
            for f in fs:
                if f.lower().endswith(SUPPORTED):
                    files.append(os.path.join(root, f))

    print(f"[+] Found {len(files)} file(s)")

    if len(files) == 0:
        return

    # process each file
    for f in files:
        try:
            scan_file(f)   # your existing forensic UI function
        except Exception as e:
            print("[ERROR]", e)

    print(t(lang, "scan_done"))

import shutil
from PIL import Image


# -------------------------
# SAFE METADATA WIPE (V2)
# -------------------------

def wipe_metadata(path, lang="en"):
    from ghostframe.i18n import t

    if not os.path.exists(path):
        print(t(lang, "path_not_found"), path)
        return

    # backup first (CRITICAL FOR FORENSICS)
    backup = path + ".bak"

    try:
        shutil.copy2(path, backup)

        confirm = input(t(lang, "wipe_confirm")).lower()

        if confirm != "y":
            print(t(lang, "abort"))
            return

        # reopen and re-save without metadata
        img = Image.open(path)
        data = list(img.getdata())
        img2 = Image.new(img.mode, img.size)
        img2.putdata(data)
        img2.save(path)

        print(t(lang, "wipe_done"))
        print("[i] Backup saved:", backup)

    except Exception as e:
        print("[ERROR]", e)
