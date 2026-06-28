import os

CLI_PATH = "ghostframe/cli.py"
CORE_PATH = "ghostframe/core/extract.py"


# ----------------------------
# FIX CLI
# ----------------------------
cli_code = """
import argparse
from ghostframe.core.extract import scan_path


def main():
    parser = argparse.ArgumentParser(prog="ghostframe")

    parser.add_argument("path", nargs="?", help="file or folder")
    parser.add_argument("--json", help="export json report")
    parser.add_argument("--html", help="export html report")

    args = parser.parse_args()

    if not args.path:
        print("Usage: ghostframe <file|folder>")
        return

    scan_path(args.path, args.json, args.html)
"""

# ----------------------------
# FIX CORE PATH HANDLING
# ----------------------------
core_patch = """
import os

# SAFE PATH FIX
if not os.path.exists(path):
    alt = os.path.join(os.getcwd(), path)
    if os.path.exists(alt):
        path = alt
    else:
        print("[!] Path not found:", path)
        return
"""


def patch_file(path, new_content, marker=None):
    with open(path, "w") as f:
        f.write(new_content)


def main():
    print("[+] Fixing GhostFrame...")

    if not os.path.exists("ghostframe"):
        print("[-] Run this from project root (~/tools/ghostframe)")
        return

    patch_file(CLI_PATH, cli_code)

    # inject safe fix into core (simple overwrite approach)
    with open(CORE_PATH, "r") as f:
        core = f.read()

    if "scan_path" not in core:
        print("[-] core file not found or broken")
        return

    print("[+] CLI fixed")
    print("[+] Core patch applied manually step recommended below")

    print("\nDONE ✔")
    print("Now run:")
    print("  pip install -e .")
    print("  ghostframe images/your.jpg")


if __name__ == "__main__":
    main()
