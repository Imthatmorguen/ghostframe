STRINGS = {
    "en": {
        "case_created": "[+] Case created:",
        "scan_start": "[+] Scanning...",
        "scan_done": "[✓] Scan complete",
        "path_not_found": "[!] Path not found",
        "wipe_confirm": "Confirm wipe (y/n): ",
        "wipe_done": "[✓] Metadata wiped",
        "abort": "[-] Cancelled",
        "usage": "Usage: ghostframe <scan|wipe|config>"
    },
    "es": {
        "case_created": "[+] Caso creado:",
        "scan_start": "[+] Escaneando...",
        "scan_done": "[✓] Escaneo completo",
        "path_not_found": "[!] Ruta no encontrada",
        "wipe_confirm": "Confirmar borrado (s/n): ",
        "wipe_done": "[✓] Metadatos eliminados",
        "abort": "[-] Cancelado",
        "usage": "Uso: ghostframe <scan|wipe|config>"
    }
}


def t(lang, key):
    return STRINGS.get(lang, STRINGS["en"]).get(key, key)
