from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

MAGIC = b"HUF1"


def _normalize_frequency_dict(freqs: Dict[str, int]) -> Dict[str, int]:
    return {str(k): int(v) for k, v in freqs.items()}


def write_compressed_file(path: str | Path, frequencies: Dict[str, int], payload: bytes, padding: int) -> Path:
    target = Path(path)
    header = {
        "frequencies": _normalize_frequency_dict(frequencies),
        "padding": int(padding),
    }
    header_bytes = json.dumps(header, ensure_ascii=False).encode("utf-8")

    with target.open("wb") as f:
        f.write(MAGIC)
        f.write(len(header_bytes).to_bytes(4, "big"))
        f.write(header_bytes)
        f.write(payload)

    return target


def read_compressed_file(path: str | Path) -> Tuple[Dict[str, int], bytes, int]:
    target = Path(path)
    with target.open("rb") as f:
        magic = f.read(4)
        if magic != MAGIC:
            raise ValueError("El archivo no es un archivo comprimido válido (.huf).")

        header_len = int.from_bytes(f.read(4), "big")
        header = json.loads(f.read(header_len).decode("utf-8"))
        payload = f.read()

    freqs = _normalize_frequency_dict(header.get("frequencies", {}))
    padding = int(header.get("padding", 0))
    return freqs, payload, padding


def human_char(char: str) -> str:
    special = {
        " ": "[ESPACIO]",
        "\n": "[SALTO_LINEA]",
        "\t": "[TAB]",
    }
    return special.get(char, char)
