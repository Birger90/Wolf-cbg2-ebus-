#!/usr/bin/env python3
"""Prüfbyte (CRC8) des Wolf/Kromschröder-Parameterprotokolls (PBSB 5022 lesen / 5023 schreiben).

Aufbau der Telegramme (Nutzdaten nach PBSB und Längenbyte):

    lesen:     <CRC8> <TN lo> <TN hi>
    lesen x5:  <CRC8> <TN1 lo> <TN1 hi> ... <TN5 lo> <TN5 hi>          (Blocklesen des ISM7)
    schreiben: <CRC8> <TN lo> <TN hi> <Wert lo> <Wert hi> [<Anhang 4 Byte>]

Der CRC8 läuft über ALLE Bytes nach dem Prüfbyte:
    Polynom 0x5C, Startwert 0x00, keine Spiegelung, kein End-XOR,
    pro Byte: c = shift8(c) XOR byte   (shift8 = 8 Schiebeschritte mit XOR 0x5C bei gesetztem Bit 7)

Verifiziert am 19.10.2026 an 21 mitgeschnittenen Telegrammen (ISM7, BM-2) einer
Wolf CGB-2-24 mit BM-2, siehe verify() unten. Unabhängig dokumentiert von
dktzde/ebusd-configuration-wolf (tools/ebus_crc8.js), Ergebnis identisch.

Beobachtet an dieser Anlage:
  - Die Therme (08) antwortet auf Lesetelegramme mit beliebigem Prüfbyte (00, cc, CRC).
  - Das BM-2 (35) nimmt Schreibtelegramme mit falschem Prüfbyte an.
  - Ein korrektes Prüfbyte funktioniert überall, deshalb wird es hier immer berechnet.
"""
import sys


def shift8(c: int) -> int:
    for _ in range(8):
        c = ((c << 1) & 0xFF) ^ 0x5C if c & 0x80 else (c << 1) & 0xFF
    return c


def wolf_crc(data: bytes) -> int:
    c = 0
    for b in data:
        c = shift8(c) ^ b
    return c


def tn_le(tn: int) -> bytes:
    return bytes([tn & 0xFF, (tn >> 8) & 0xFF])


def read_id(tn: int) -> str:
    """ebusd-ID (hex) für eine Lesenachricht: CRC + TN little endian."""
    d = tn_le(tn)
    return f"{wolf_crc(d):02x}{d.hex()}"


def write_payload(tn: int, value: int, suffix: bytes = b"") -> bytes:
    """Komplette Nutzdaten einer Schreibnachricht inkl. Prüfbyte (value als Rohwert, z.B. 50.0 °C -> 500)."""
    d = tn_le(tn) + bytes([value & 0xFF, (value >> 8) & 0xFF]) + suffix
    return bytes([wolf_crc(d)]) + d


# Mitschnitte vom 19.10.2026 (ebusd-Log, Wolf CGB-2-24 + BM-2 + MM + ISM7): Prüfbyte, Nutzdaten danach
CAPTURED = {
    # ISM7 -> Therme, Einzel-Lesen
    "5b": "b027", "a6": "6a02", "82": "882a", "27": "5727", "90": "0f00", "00": "5700", "5c": "5600", "77": "1a27",
    # ISM7 -> Therme/BM-2, Blocklesen 5 TNs
    "71": "160048016f0172017301", "54": "020003000c000d000e00", "5b_": "ae27af27b427b527c327",
    "87": "a127a627ab27ac27ad27", "db": "2a021a271d2753275427", "bf": "13008114821492147427",
    # BM-2 -> Therme / Broadcast, Schreiben (TN + Wert)
    "84": "4e2a0000", "44": "23000000", "28": "000a1400", "4f": "f4020003",
    # ISM7 -> BM-2, Schreiben WW-Soll (TN 19) + Anhang 5d010000
    "b0": "1300f4015d010000", "6c": "13008a025d010000", "cc": "13001c025d010000", "c4": "1300d6015d010000",
    "14": "13007201"+"5d010000", "98": "130054015d010000", "00_": "130022015d010000", "48": "13005e015d010000",
    "28_": "13002c015d010000",
}


def verify() -> bool:
    ok = True
    for crc, data in CAPTURED.items():
        exp = int(crc.rstrip("_"), 16)
        got = wolf_crc(bytes.fromhex(data))
        flag = "OK " if got == exp else "FEHLER"
        if got != exp:
            ok = False
        print(f"{flag} erwartet {exp:02x} berechnet {got:02x}  Daten {data}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--verify":
        sys.exit(0 if verify() else 1)
    if sys.argv[1] == "--read":
        for a in sys.argv[2:]:
            print(f"TN {int(a):>6} -> Lese-ID {read_id(int(a))}")
    elif sys.argv[1] == "--write":
        tn, val = int(sys.argv[2]), int(sys.argv[3])
        suffix = bytes.fromhex(sys.argv[4]) if len(sys.argv) > 4 else b""
        print(" ".join(f"{b:02x}" for b in write_payload(tn, val, suffix)))
    else:
        print(__doc__)
