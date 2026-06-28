import argparse

from ghostframe.core.extract import scan_path, wipe_metadata
from ghostframe.config import load_config, save_config
from ghostframe.i18n import t


def main():
    cfg = load_config()
    lang = cfg.get("language", "en")

    parser = argparse.ArgumentParser(prog="ghostframe")

    sub = parser.add_subparsers(dest="cmd")

    # scan
    scan = sub.add_parser("scan")
    scan.add_argument("path")

    # wipe
    wipe = sub.add_parser("wipe")
    wipe.add_argument("file")

    # config
    config = sub.add_parser("config")
    config.add_argument("--lang", choices=["en", "es"])

    args = parser.parse_args()

    # -----------------------
    # SCAN
    # -----------------------
    if args.cmd == "scan":
        print(t(lang, "scan_start"))
        scan_path(args.path, lang)
        print(t(lang, "scan_done"))

    # -----------------------
    # WIPE
    # -----------------------
    elif args.cmd == "wipe":
        wipe_metadata(args.file, lang)

    # -----------------------
    # CONFIG
    # -----------------------
    elif args.cmd == "config":
        if args.lang:
            cfg["language"] = args.lang
            save_config(cfg)
            print("Language set:", args.lang)
        else:
            print("Current language:", lang)

    else:
        print(t(lang, "usage"))
