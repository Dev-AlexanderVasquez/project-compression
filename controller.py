from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from huffman import (
    bits_to_bytes,
    build_frequency_table,
    build_huffman_codes,
    build_huffman_tree,
    bytes_to_bits,
    decode_bits,
    encode_text,
    format_huffman_tree,
)
from utils import human_char, read_compressed_file, write_compressed_file


@dataclass
class CompressionResult:
    input_text: str
    frequencies: Dict[str, int]
    codes: Dict[str, str]
    tree_text: str
    encoded_bits: str
    compressed_bytes: bytes
    padding: int

    @property
    def original_bits(self) -> int:
        return len(self.input_text) * 8

    @property
    def compressed_bits(self) -> int:
        return len(self.encoded_bits)

    @property
    def reduction_percent(self) -> float:
        if self.original_bits == 0:
            return 0.0
        return (1 - (self.compressed_bits / self.original_bits)) * 100


class HuffmanController:
    def __init__(self) -> None:
        self.last_result: Optional[CompressionResult] = None

    def compress_text(self, text: str) -> CompressionResult:
        frequencies = build_frequency_table(text)
        tree = build_huffman_tree(frequencies)
        codes = build_huffman_codes(tree)
        encoded_bits = encode_text(text, codes) if text else ""
        compressed_bytes, padding = bits_to_bytes(encoded_bits)

        result = CompressionResult(
            input_text=text,
            frequencies=frequencies,
            codes=codes,
            tree_text=format_huffman_tree(tree),
            encoded_bits=encoded_bits,
            compressed_bytes=compressed_bytes,
            padding=padding,
        )
        self.last_result = result
        return result

    def save_compressed(self, output_path: str | Path) -> Path:
        if self.last_result is None:
            raise ValueError("Primero debes comprimir un texto.")

        return write_compressed_file(
            output_path,
            self.last_result.frequencies,
            self.last_result.compressed_bytes,
            self.last_result.padding,
        )

    def decompress_file(self, input_path: str | Path) -> str:
        frequencies, payload, padding = read_compressed_file(input_path)
        tree = build_huffman_tree(frequencies)
        bits = bytes_to_bits(payload, padding)
        return decode_bits(bits, tree)

    @staticmethod
    def frequencies_table_text(freqs: Dict[str, int], relative: bool = False) -> str:
        if not freqs:
            return "(sin datos)"

        total = sum(freqs.values())
        lines = ["Símbolo\tFrecuencia"]
        for ch, count in sorted(freqs.items(), key=lambda item: (-item[1], item[0])):
            value = f"{(count / total) * 100:.2f}%" if relative else str(count)
            lines.append(f"{human_char(ch)}\t{value}")

        return "\n".join(lines)

    @staticmethod
    def codes_table_text(codes: Dict[str, str]) -> str:
        if not codes:
            return "(sin datos)"

        lines = ["Símbolo\tCódigo Huffman"]
        for ch, code in sorted(codes.items(), key=lambda item: (len(item[1]), item[1])):
            lines.append(f"{human_char(ch)}\t{code}")
        return "\n".join(lines)
