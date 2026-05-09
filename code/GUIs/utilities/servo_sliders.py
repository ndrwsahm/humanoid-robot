import tkinter as tk
from tkinter import ttk

class ServoSliderGroup(tk.Frame):
    def __init__(self, parent, names, rows=None):
        """
        parent = parent widget
        names  = list of servo names (strings)
        rows   = number of rows before wrapping (default = len(names))
        """
        super().__init__(parent)

        self.names = names
        self.count = len(names)
        self.rows = rows if rows is not None else len(names)

        self.labels = []
        self.sliders = []

        self._build()

    def _build(self):
        for i, name in enumerate(self.names):
            r = i % self.rows
            c = (i // self.rows) * 2  # label/slider pairs

            lbl = tk.Label(self, text=f"{name}0", width=30)
            lbl.grid(row=r, column=c, padx=10, pady=3, sticky="w")
            self.labels.append(lbl)

            sld = ttk.Scale(
                self,
                from_=0,
                to=180,
                orient="horizontal",
                command=lambda x, idx=i: self._update_label(idx)
            )
            sld.grid(row=r, column=c+1, padx=10, pady=3, sticky="we")
            self.sliders.append(sld)

        # allow sliders to stretch
        for col in range(0, (self.count // self.rows + 1) * 2):
            self.grid_columnconfigure(col, weight=1)

    def _update_label(self, idx):
        val = round(self.sliders[idx].get())
        self.labels[idx].config(text=f"{self.names[idx]}{val}")

    def set_all(self, values):
        for i, v in enumerate(values):
            v = round(v)
            self.sliders[i].set(v)
            self.labels[i].config(text=f"{self.names[i]}{v}")

    def get_all(self):
        return [round(s.get()) for s in self.sliders]

    def reset_all(self):
        for i in range(self.count):
            self.sliders[i].set(90)
            self.labels[i].config(text=f"{self.names[i]}{90}")

    def hide(self):
        self.grid_remove()

    def show(self):
        self.grid()
