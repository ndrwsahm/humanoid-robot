import tkinter as tk
from tkinter import ttk

class StatusBar(tk.Frame):
    def __init__(self, parent, height=20, width=40, font=("Courier", 10)):
        super().__init__(parent)

        # --- Scrollbars ---
        self.scroll_y = tk.Scrollbar(self, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

        self.scroll_x = tk.Scrollbar(self, orient="horizontal")
        self.scroll_x.pack(side="bottom", fill="x")

        # --- Text Widget ---
        self.text = tk.Text(
            self,
            height=height,
            width=width,
            font=font,
            wrap="none",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
            state="disabled"
        )
        self.text.pack(side="left", fill="both", expand=True)

        # Link scrollbars
        self.scroll_y.config(command=self.text.yview)
        self.scroll_x.config(command=self.text.xview)

    # --- Public API ---
    def print(self, msg):
        self.text.config(state="normal")
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)
        self.text.config(state="disabled")

    def clear(self):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.config(state="disabled")
