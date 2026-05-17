from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import heapq
from typing import Dict, Optional


@dataclass(order=True)
class HuffmanNode:
    frequency: int
    symbol: Optional[str] = field(default=None, compare=False)
    left: Optional["HuffmanNode"] = field(default=None, compare=False)
    right: Optional["HuffmanNode"] = field(default=None, compare=False)

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_frequency_table(text: str) -> Dict[str, int]:
    return dict(Counter(text))


def build_huffman_tree(frequencies: Dict[str, int]) -> Optional[HuffmanNode]:
    if not frequencies:
        return None

    heap = [HuffmanNode(freq, symbol) for symbol, freq in frequencies.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        only = heapq.heappop(heap)
        return HuffmanNode(only.frequency, None, only, None)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.frequency + right.frequency, None, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


def build_huffman_codes(root: Optional[HuffmanNode]) -> Dict[str, str]:
    if root is None:
        return {}

    codes: Dict[str, str] = {}

    def _walk(node: HuffmanNode, prefix: str) -> None:
        if node.is_leaf and node.symbol is not None:
            codes[node.symbol] = prefix or "0"
            return
        if node.left:
            _walk(node.left, prefix + "0")
        if node.right:
            _walk(node.right, prefix + "1")

    _walk(root, "")
    return codes


def encode_text(text: str, codes: Dict[str, str]) -> str:
    return "".join(codes[ch] for ch in text)


def decode_bits(encoded_bits: str, root: Optional[HuffmanNode]) -> str:
    if not encoded_bits or root is None:
        return ""

    result = []
    node = root
    for bit in encoded_bits:
        node = node.left if bit == "0" else node.right
        if node and node.is_leaf:
            result.append(node.symbol or "")
            node = root

    return "".join(result)


def bits_to_bytes(bits: str) -> tuple[bytes, int]:
    if not bits:
        return b"", 0

    padding = (8 - (len(bits) % 8)) % 8
    padded_bits = bits + ("0" * padding)
    chunks = [padded_bits[i : i + 8] for i in range(0, len(padded_bits), 8)]
    return bytes(int(chunk, 2) for chunk in chunks), padding


def bytes_to_bits(data: bytes, padding: int) -> str:
    if not data:
        return ""
    bits = "".join(f"{byte:08b}" for byte in data)
    return bits[:-padding] if padding else bits


def format_huffman_tree(root: Optional[HuffmanNode]) -> str:
    if root is None:
        return "(árbol vacío)"

    lines: list[str] = []

    def _render(node: HuffmanNode, prefix: str, edge: str) -> None:
        if node.is_leaf and node.symbol is not None:
            symbol = repr(node.symbol)
            lines.append(f"{prefix}{edge} {symbol} ({node.frequency})")
            return

        lines.append(f"{prefix}{edge} * ({node.frequency})")
        if node.left:
            _render(node.left, prefix + "   ", "0→")
        if node.right:
            _render(node.right, prefix + "   ", "1→")

    _render(root, "", "•")
    return "\n".join(lines)
