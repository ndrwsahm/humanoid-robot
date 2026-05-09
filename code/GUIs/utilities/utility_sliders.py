import tkinter as tk
from tkinter import ttk

class LabeledSliderGroup(tk.Frame):
    def __init__(self, parent, names, mins, maxs, orients=None,
                 defaults=None, commands=None, rows=None, label_width=35):
        """
        names:    list of label strings
        mins:     list of min values
        maxs:     list of max values
        orients:  list of "horizontal" or "vertical" (optional)
        defaults: list of default slider values (optional)
        commands: list of callback functions (optional)
        rows:     number of rows before wrapping (optional)
        """

        super().__init__(parent)

        self.names = names
        self.count = len(names)
        self.mins = mins
        self.maxs = maxs
        self.orients = orients or ["horizontal"] * self.count
        self.defaults = defaults or [None] * self.count
        self.commands = commands or [None] * self.count
        self.rows = rows if rows is not None else self.count

        self.labels = []
        self.sliders = []

        self._build(label_width)

    def _build(self, label_width):
        for i in range(self.count):
            r = i % self.rows
            c = (i // self.rows) * 2  # label/slider pairs

            # Label
            lbl = tk.Label(self, text=f"{self.names[i]}", width=label_width)
            lbl.grid(row=r, column=c, padx=10, pady=5, sticky="w")
            self.labels.append(lbl)

            # Slider
            sld = ttk.Scale(
                self,
                from_=self.mins[i],
                to=self.maxs[i],
                orient=self.orients[i],
                command=lambda val, idx=i: self._callback_wrapper(idx, val)
            )
            sld.grid(row=r, column=c+1, padx=10, pady=5, sticky="we")
            self.sliders.append(sld)

            # Default value
            if self.defaults[i] is not None:
                sld.set(self.defaults[i])
                self._update_label(i, self.defaults[i])

        # Allow sliders to stretch
        for col in range((self.count // self.rows + 1) * 2):
            self.grid_columnconfigure(col, weight=1)

    def _callback_wrapper(self, idx, val):
        """Update label + call user callback."""
        self._update_label(idx, val)
        if self.commands[idx]:
            return self.commands[idx](val)

    def _update_label(self, idx, val):
        rounded = round(float(val), 2)
        self.labels[idx].config(text=f"{self.names[idx]}{rounded}")

    def get_all(self):
        return [float(s.get()) for s in self.sliders]

    def set_all(self, values):
        for i, v in enumerate(values):
            self.sliders[i].set(v)
            self._update_label(i, v)

    def reset_all(self, value=0):
        for i in range(self.count):
            self.sliders[i].set(value)
            self._update_label(i, value)
