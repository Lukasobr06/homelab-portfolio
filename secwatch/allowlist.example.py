"""Beispiel: Erlaubnisliste für Update-Pläne (Platzhalter, nicht die echte Liste).

Jeder Befehl im Plan muss vollständig auf ein Muster passen. Ausgeführt wird
später ohne Shell (argv), deshalb ist nur ein kleiner Zeichensatz erlaubt.
"""
import re

SAFE_CHARS = re.compile(r"[A-Za-z0-9 ._:/=+~-]+")

PKG = r"[a-z0-9][a-z0-9+.-]{0,62}"
PKGS = rf"{PKG}( {PKG}){{0,29}}"
SNAP = r"secwatch_[A-Za-z0-9_]{1,40}"

RULES = {
    "host": {
        "commands": [r"apt-get update", rf"apt-get install --only-upgrade -y {PKGS}"],
        "checks": [r"uname -r", rf"dpkg-query -W {PKGS}"],
    },
    "dns-container": {
        "snapshot": [rf"pct snapshot <CT-ID> {SNAP}"],
        "commands": [r"pct exec <CT-ID> -- <DNS-DIENST> --update"],
        "rollback": [rf"pct rollback <CT-ID> {SNAP}"],
    },
    "firewall-vm": {
        "snapshot": [rf"qm snapshot <VM-ID> {SNAP}"],
        "commands": [r"qm guest exec <VM-ID> -- configctl firmware update"],
        "rollback": [rf"qm rollback <VM-ID> {SNAP}"],
    },
}


def allowed(system: str, kind: str, cmd: str) -> bool:
    if not SAFE_CHARS.fullmatch(cmd) or "  " in cmd:
        return False
    return any(re.fullmatch(p, cmd) for p in RULES.get(system, {}).get(kind, []))
