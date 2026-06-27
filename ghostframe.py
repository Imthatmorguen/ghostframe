#!/usr/bin/env python3
"""
Forensic EXIF Metadata & GPS Extractor
Disclaimer: For educational and authorized administrative auditing purposes only.
"""

import argparse
import os
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import GPSTAGS, TAGS

BANNER = r"""
 _   _  _____ ______  _____ ______ __   __

| \ | ||  _  || ___ \|  _  ||  _  \\ \ / /
|  \| || | | || |_/ /| | | || | | | \ V / 
| . ` || | | || ___ \| | | || | | |  \ /  
| |\  |\ \_/ /| |_/ /\ \_/ /| |/ /   | |  
\_| \_/ \___/ \____/  \___/ |___/    \_/  
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
        # Handle unpacked sequences safely regardless of tuple variations
        dec_lat = convert_to_decimal(lat[0], lat[1], lat[2], lat_ref)
        dec_lon = convert_to_decimal(lon[0], lon[1], lon[2], lon_ref)
        if dec_lat is not None and dec_lon is not None:
            return f"https://google.com{dec_lat},{dec_lon}"
    return None


def process_image(file_path, output_stream):
    """Opens a target image path, parses EXIF frames, and logs metrics."""
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
                    gps_raw = value  # Defer parsing to ensure clear structural grouping
                else:
                    output_stream.write(f"  {tag_name}: {value}\n")

            if gps_raw:
                output_stream.write("\n  --- GPS Tracking Metrics ---\n")
                # Print explicit items inside the nested dictionary
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


def main():
    print(BANNER)
    
    # Setup robust Argument Parser flag bindings
    parser = argparse.ArgumentParser(description="Forensic Image EXIF & Coordinates Tracking Analysis Utility.")
    parser.add_argument("-p", "--path", default="images", help="Target filename or workspace folder path (Default: ./images)")
    args = parser.parse_args()

    target_path = args.path

    if not os.path.exists(target_path):
        print(f"[-] Execution Halt: The specified path '{target_path}' does not exist on this environment.")
        return

    # Prompt delivery layout configuration choice
    print("Select Analysis Delivery Target:")
    print("  1 - Text File Export (exif_analysis.txt)")
    print("  2 - Standard Interactive Terminal Screen Output")
    
    while True:
        choice = input("Select Execution Mode (1 or 2): ").strip()
        if choice in ('1', '2'):
            break
        print("[!] Input validation fault. Enter 1 or 2.")

    # Determine runtime files distribution matrix
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

    print(f"\n[+] Processing Sequence Initiated over {len(files_to_process)} discovered files...")

    # Redirect and evaluate runtime streams safely
    if choice == '1':
        export_filename = "exif_analysis.txt"
        with open(export_filename, "w", encoding="utf-8") as out_file:
            for file in files_to_process:
                process_image(file, out_file)
        print(f"[✓] Structural processing finalized. Report available at: {export_filename}")
    else:
        for file in files_to_process:
            process_image(file, sys.stdout)
        print("\n[✓] Interactive data pipeline finalized successfully.")


if __name__ == "__main__":
    main()
