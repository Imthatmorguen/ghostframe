#!/usr/bin/env python3
"""
ghostframe - Forensic Image Analysis & Remediation Toolkit
Disclaimer: For educational and authorized administrative auditing purposes only.
"""

import argparse
import os
import sys
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import GPSTAGS, TAGS

BANNER = r"""
 _____              _   _           _                                                        

|_   _|            | | | |         | |                                                       
  | |  _ __ ___    | |_| |__   __ _| |_ _ __ ___   ___  _ __ __ _ _   _  ___ _ __             
  | | | '_ ` _ \   | __| '_ \ / _` | __| '_ ` _ \ / _ \| '__/ _` | | | |/ _ \ '_ \            
 _| |_| | | | | |  | |_| | | | (_| | |_| | | | | | (_) | | | (_| | |_| |  __/ | | |           
 \___/|_| |_| |_|   \__|_| |_|\__,_|\__|_| |_| |_|\___/|_|  \__, |\__,_|\___|_| |_|           
                                                             __/ |                           
                                                            |___/                            
"""

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.tiff', '.tif')


def convert_to_decimal(degrees, minutes, seconds, reference):
    """Converts Degree/Minutes/Seconds raw EXIF fractions to Decimal Degrees."""
    try:
        deg = float(degrees)
        mn = float(minutes)
        sec = float(seconds)
        decimal = deg + (mn / 60.0) + (sec / 3600.0)
        if reference in ('S', 'W'):
            decimal *= -1
        return round(decimal, 6)
    except (TypeError, ZeroDivisionError, ValueError):
        return None


def parse_gps_info(gps_dict):
    """Extracts, standardizes, and evaluates usable coordinate dictionaries."""
    gps_data = {}
    for key, value in gps_dict.items():
        tag_name = GPSTAGS.get(key, key)
        gps_data[tag_name] = value

    lat = gps_data.get("GPSLatitude")
    lat_ref = gps_data.get("GPSLatitudeRef")
    lon = gps_data.get("GPSLongitude")
    lon_ref = gps_data.get("GPSLongitudeRef")

    if all([lat, lat_ref, lon, lon_ref]):
        dec_lat = convert_to_decimal(lat, lat, lat, lat_ref)
        dec_lon = convert_to_decimal(lon, lon, lon, lon_ref)
        if dec_lat is not None and dec_lon is not None:
            return f"https://google.com{dec_lat},{dec_lon}"
    return None


def extract_metadata(file_path, output_stream):
    """Opens an image path, parses EXIF frames, and prints/logs metrics."""
    output_stream.write("\n" + "=" * 80 + "\n")
    output_stream.write(f" TARGET FILE: {os.path.abspath(file_path)}\n")
    output_stream.write("=" * 80 + "\n")

    try:
        with Image.open(file_path) as img:
            exif_data = img.getexif()
            if not exif_data:
                output_stream.write("[*] This image file contains no embedded EXIF metadata.\n")
                return

            gps_raw = None
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "GPSInfo":
                    gps_raw = value  
                else:
                    output_stream.write(f"  {tag_name}: {value}\n")

            if gps_raw:
                output_stream.write("\n  --- GPS Tracking Metrics ---\n")
                for k, v in gps_raw.items():
                    output_stream.write(f"    {GPSTAGS.get(k, k)}: {v}\n")
                
                maps_url = parse_gps_info(gps_raw)
                if maps_url:
                    output_stream.write(f"\n  [+] Geolocation Hyperlink Identified:\n    {maps_url}\n")
                else:
                    output_stream.write("\n  [-] Incomplete coordinate matrix. Unable to build map URL.\n")

    except UnidentifiedImageError:
        output_stream.write("[-] Processing Exception: File signature invalid or unreadable graphic structure.\n")
    except (IOError, PermissionError) as e:
        output_stream.write(f"[-] OS System Exception reading target file descriptor: {e}\n")


def strip_metadata(file_path):
    """Opens an image and saves it again to wipe out all unrequested EXIF tables."""
    try:
        print(f"[*] Stripping: {os.path.basename(file_path)}... ", end="", flush=True)
        with Image.open(file_path) as img:
            # Safely handle image transparency layers converting to JPEG format structures
            if img.mode in ("RGBA", "P") and file_path.lower().endswith(('.jpg', '.jpeg')):
                img = img.convert("RGB")
            
            # Saving clean drops old unrequested EXIF records completely
            img.save(file_path)
        print("WIPED!")
    except UnidentifiedImageError:
        print("FAILED (Invalid image signature)")
    except (IOError, PermissionError) as e:
        print(f"FAILED (OS Error: {e})")


def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="Forensic Image EXIF Tool - Analysis & Remediation Suite.")
    parser.add_argument("-p", "--path", default="images", help="Target filename or workspace folder path (Default: ./images)")
    args = parser.parse_args()

    target_path = args.path

    if not os.path.exists(target_path):
        print(f"[-] Execution Halt: The specified path '{target_path}' does not exist on this environment.")
        return

    # Phase 1: Operational Core Mode Decision Mapping
    print("Choose Application Function:")
    print("  1 - [Read] Extract Embedded EXIF Metadata & Geolocation")
    print("  2 - [Wipe] Permanent Metadata Removal (Destructive)")
    while True:
        mode_choice = input("Select Action (1 or 2): ").strip()
        if mode_choice in ('1', '2'):
            break
        print("[!] Input validation fault. Enter 1 or 2.")

    # Phase 2: Structural File Gathering Pipeline
    files_to_process = []
    if os.path.isfile(target_path):
        if target_path.lower().endswith(SUPPORTED_EXTENSIONS):
            files_to_process.append(target_path)
    else:
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith(SUPPORTED_EXTENSIONS):
                    files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        print(f"[-] Execution End: No compatible target images found matching format scopes: {SUPPORTED_EXTENSIONS}")
        return

    print(f"\n[+] Discovered {len(files_to_process)} file(s). Starting execution thread...")

    # Phase 3: Action Dispatch Matrix Route Handling
    if mode_choice == '1':
        print("\nSelect Analysis Delivery Target:")
        print("  1 - Text File Export (exif_analysis.txt)")
        print("  2 - Standard Interactive Terminal Screen Output")
        while True:
            delivery_choice = input("Select Output Target (1 or 2): ").strip()
            if delivery_choice in ('1', '2'):
                break
            print("[!] Input validation fault. Enter 1 or 2.")

        if delivery_choice == '1':
            export_filename = "exif_analysis.txt"
            with open(export_filename, "w", encoding="utf-8") as out_file:
                for file in files_to_process:
                    extract_metadata(file, out_file)
            print(f"\n[✓] Metadata analysis exported to: {export_filename}")
        else:
            for file in files_to_process:
                extract_metadata(file, sys.stdout)
            print("\n[✓] Interactive data mapping pipeline completed.")

    elif mode_choice == '2':
        confirm = input("\n⚠️ WARNING: This operation overwrites your files to permanently clear metadata. Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("[-] Operation aborted safely.")
            return
        
        print()
        for file in files_to_process:
            strip_metadata(file)
        print("\n[✓] All target media metadata arrays successfully remediated.")


if __name__ == "__main__":
    main()
