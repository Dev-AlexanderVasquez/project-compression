from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from controller import HuffmanController


class HuffmanApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Compresor Huffman - Proyecto TXT")
        self.geometry("1180x760")
        self.minsize(980, 650)

        self.controller = HuffmanController()
        self.loaded_file: Path | None = None

        self._configure_theme()
        self._build_ui()

    def _configure_theme(self) -> None:
        self.configure(bg="#101426")
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Root.TFrame", background="#101426")
        style.configure("Card.TFrame", background="#18203a", relief="flat")
        style.configure("Title.TLabel", background="#101426", foreground="#f0f4ff", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background="#101426", foreground="#aab6dd", font=("Segoe UI", 10))
        style.configure("PanelTitle.TLabel", background="#18203a", foreground="#ffffff", font=("Segoe UI", 11, "bold"))
        style.configure("Info.TLabel", background="#18203a", foreground="#d5ddfb", font=("Segoe UI", 10))
        style.configure("Accent.TButton", background="#4b7cff", foreground="white", padding=8, font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#5f8bff")])

    def _build_ui(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame", padding=18)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Compresión de Texto con Huffman", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            root,
            text="Carga un .txt o escribe texto, comprime, guarda archivo .huf y descomprímelo con trazabilidad completa.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 12))

        container = ttk.Frame(root, style="Root.TFrame")
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=2)
        container.columnconfigure(1, weight=3)

        left = ttk.Frame(container, style="Card.TFrame", padding=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = ttk.Frame(container, style="Card.TFrame", padding=14)
        right.grid(row=0, column=1, sticky="nsew")

        self._build_left(left)
        self._build_right(right)

    def _build_left(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Entrada", style="PanelTitle.TLabel").pack(anchor="w")

        self.file_label = ttk.Label(parent, text="Archivo: (ninguno)", style="Info.TLabel")
        self.file_label.pack(anchor="w", pady=(4, 8))

        btn_row = ttk.Frame(parent, style="Card.TFrame")
        btn_row.pack(fill="x", pady=(0, 10))
        ttk.Button(btn_row, text="📂 Cargar TXT", style="Accent.TButton", command=self.load_text_file).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="🧹 Limpiar", command=self.clear_input).pack(side="left")

        self.input_text = tk.Text(
            parent,
            wrap="word",
            font=("Consolas", 11),
            bg="#0f1630",
            fg="#ecf2ff",
            insertbackground="#ecf2ff",
            relief="flat",
            height=13,
        )
        self.input_text.pack(fill="both", expand=False)

        action_row = ttk.Frame(parent, style="Card.TFrame")
        action_row.pack(fill="x", pady=(10, 0))
        ttk.Button(action_row, text="⚙️ Comprimir", style="Accent.TButton", command=self.compress).pack(side="left", padx=(0, 8))
        ttk.Button(action_row, text="💾 Guardar .huf", command=self.save_compressed).pack(side="left", padx=(0, 8))
        ttk.Button(action_row, text="📥 Descomprimir .huf", command=self.decompress_file).pack(side="left")

        metric_card = ttk.Frame(parent, style="Card.TFrame")
        metric_card.pack(fill="x", pady=(12, 0))
        ttk.Label(metric_card, text="Métrica solicitada", style="PanelTitle.TLabel").pack(anchor="w")

        self.metric_var = tk.StringVar(value="original")
        options = [
            ("Bits originales", "original"),
            ("Bits con Huffman", "compressed"),
            ("% reducción", "reduction"),
        ]
        for text, value in options:
            ttk.Radiobutton(metric_card, text=text, value=value, variable=self.metric_var, command=self.update_metric_output).pack(anchor="w")

        self.metric_output = ttk.Label(metric_card, text="Aún no se ha comprimido contenido.", style="Info.TLabel")
        self.metric_output.pack(anchor="w", pady=(8, 0))

    def _build_right(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Desarrollo paso a paso", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 8))

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        self.freq_text = self._create_tab("Tabla de frecuencias")
        self.tree_text = self._create_tab("Árbol y códigos")
        self.binary_text = self._create_tab("Archivo comprimido")
        self.output_text = self._create_tab("Texto recuperado")

    def _create_tab(self, title: str) -> tk.Text:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        text_widget = tk.Text(
            frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#0e1733",
            fg="#f3f6ff",
            relief="flat",
            padx=10,
            pady=10,
        )
        text_widget.pack(fill="both", expand=True)
        return text_widget

    def load_text_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return

        file_path = Path(path)
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            messagebox.showerror("Error", "No se pudo leer el archivo en UTF-8.")
            return

        self.loaded_file = file_path
        self.file_label.config(text=f"Archivo: {file_path.name}")
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", content)

    def clear_input(self) -> None:
        self.input_text.delete("1.0", tk.END)
        self.file_label.config(text="Archivo: (ninguno)")
        self.loaded_file = None

    def compress(self) -> None:
        text = self.input_text.get("1.0", tk.END).rstrip("\n")
        if not text:
            messagebox.showwarning("Atención", "Ingresa o carga texto para comprimir.")
            return

        result = self.controller.compress_text(text)

        self._set_text(self.freq_text, self.controller.frequencies_table_text(result.frequencies, relative=False))

        tree_info = (
            "ÁRBOL DE HUFFMAN\n"
            f"{result.tree_text}\n\n"
            "CÓDIGOS\n"
            f"{self.controller.codes_table_text(result.codes)}"
        )
        self._set_text(self.tree_text, tree_info)

        binary_preview = result.encoded_bits[:300] + ("..." if len(result.encoded_bits) > 300 else "")
        compressed_info = (
            f"Bits codificados (preview):\n{binary_preview}\n\n"
            f"Total bits codificados: {result.compressed_bits}\n"
            f"Bytes almacenados: {len(result.compressed_bytes)}\n"
            f"Padding aplicado: {result.padding} bits"
        )
        self._set_text(self.binary_text, compressed_info)
        self._set_text(self.output_text, "(aún no se ha descomprimido un archivo)")

        self.update_metric_output()
        messagebox.showinfo("Listo", "Compresión completada con éxito.")

    def save_compressed(self) -> None:
        if self.controller.last_result is None:
            messagebox.showwarning("Atención", "Primero comprime un texto.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".huf", filetypes=[("Huffman file", "*.huf")])
        if not path:
            return

        saved = self.controller.save_compressed(path)
        messagebox.showinfo("Archivo guardado", f"Se guardó el archivo comprimido:\n{saved}")

    def decompress_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Huffman file", "*.huf")])
        if not path:
            return

        try:
            recovered = self.controller.decompress_file(path)
        except Exception as exc:
            messagebox.showerror("Error", f"No fue posible descomprimir:\n{exc}")
            return

        self._set_text(self.output_text, recovered)
        messagebox.showinfo("Descompresión", "Archivo descomprimido correctamente.")

    def update_metric_output(self) -> None:
        result = self.controller.last_result
        if result is None:
            self.metric_output.config(text="Aún no se ha comprimido contenido.")
            return

        metric = self.metric_var.get()
        if metric == "original":
            text = f"Bits empleados por la cadena original: {result.original_bits}"
        elif metric == "compressed":
            text = f"Bits empleados con codificación Huffman: {result.compressed_bits}"
        else:
            text = f"Reducción de bits lograda: {result.reduction_percent:.2f}%"

        self.metric_output.config(text=text)

    @staticmethod
    def _set_text(widget: tk.Text, value: str) -> None:
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
