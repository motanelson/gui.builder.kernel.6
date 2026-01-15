
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

PROGMAN_FILE = """[programs]
notepad = echo notepad; notepad.exe
calc = echo calc; calc.exe

[paint]
paint = echo paint; pbrush.exe
"""
BUTTONS_PER_ROW = 4


class ProgManGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ProgMan")
        self.root.configure(bg="black")
        self.root.geometry("700x500")

        self.create_scroll_area()
        self.load_programs()

    # ---------------- SCROLL AREA ----------------

    def create_scroll_area(self):
        self.canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------------- LOAD FILE ----------------

    def load_programs(self):
        if PROGMAN_FILE=="":
            messagebox.showerror("Erro", "progman.dat não encontrado")
            return

        current_group = None
        row = 0
        col = 0
        f=PROGMAN_FILE.split("\n")
        if 0==0:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                # Grupo
                if line.startswith("[") and line.endswith("]"):
                    group_name = line[1:-1].strip()

                    label = tk.Label(
                        self.frame,
                        text=f"[ {group_name.upper()} ]",
                        fg="cyan",
                        bg="black",
                        font=("Courier", 12, "bold")
                    )
                    label.pack(anchor="w", pady=(15, 5), padx=10)

                    current_group = tk.Frame(self.frame, bg="black")
                    current_group.pack(anchor="w", padx=20)

                    row = 0
                    col = 0
                    continue

                # Item
                if "=" in line and current_group:
                    text, commands = line.split("=", 1)
                    text = text.strip()
                    commands = commands.strip()

                    btn = tk.Button(
                        current_group,
                        text=text,
                        width=16,
                        bg="#202020",
                        fg="white",
                        activebackground="#404040",
                        activeforeground="lime",
                        relief="raised",
                        command=lambda c=commands: self.execute_commands(c)
                    )

                    btn.grid(row=row, column=col, padx=5, pady=5)

                    col += 1
                    if col >= BUTTONS_PER_ROW:
                        col = 0
                        row += 1

    # ---------------- EXEC ----------------

    def execute_commands(self, command_string):
        commands = [
            c.strip() for c in command_string.split(";") if c.strip()
        ]

        for cmd in commands:
            try:
                subprocess.Popen(cmd, shell=True)
            except Exception as e:
                messagebox.showerror("Erro", str(e))


# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgManGUI(root)
    root.mainloop()