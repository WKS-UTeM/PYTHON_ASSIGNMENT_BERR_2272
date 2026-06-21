import tkinter as tk

class AboutPage:

    def __init__(self, root, dashboard):

        self.root = root
        self.dashboard = dashboard

        self.create_page()

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def create_page(self):

        self.clear_window()

        tk.Label(
            self.root,
            text="ABOUT",
            font=("Arial",20,"bold")
        ).pack(pady=20)

        about_text = """
Game Collection System for Autism Children

This system provides:
• Snake
• 2048
• Tetris
• Rapid Roll

Developed using:
• Python
• Tkinter
• SQLite

Version 1.0
"""

        tk.Label(
            self.root,
            text=about_text,
            justify="left"
        ).pack()

        tk.Button(
            self.root,
            text="Back",
            width=20,
            command=self.go_back
        ).pack(pady=20)

    def go_back(self):
        self.root.config(menu="")
        self.dashboard.create_dashboard()