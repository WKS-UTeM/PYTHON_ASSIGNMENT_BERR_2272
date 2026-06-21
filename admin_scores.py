import tkinter as tk
from tkinter import ttk

class AdminScoresPage:

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
            text="ALL USER HIGH SCORES",
            font=("Arial",20,"bold")
        ).pack()

        table = ttk.Treeview(
            self.root,
            columns=(
                "Username",
                "Game",
                "Score"
            ),
            show="headings"
        )

        table.heading(
            "Username",
            text="Username"
        )

        table.heading(
            "Game",
            text="Game"
        )

        table.heading(
            "Score",
            text="Score"
        )

        table.pack(
            fill="both",
            expand=True
        )

        scores = self.dashboard.db.get_all_high_scores()

        for username, game, score in scores:

            table.insert(
                "",
                "end",
                values=(username, game, score)
            )

        # Update the button configuration to handle a clean window transition
        tk.Button(
            self.root,
            text="Back",
            width = 20,
            command=self.go_back  # 👈 Change this from self.dashboard.create_dashboard
        ).pack(pady=10)

    # Add this clean transition helper method to the class
    def go_back(self):
        self.root.config(menu="")  # Clear the menu configuration completely
        self.dashboard.create_dashboard()  # Safely rebuild the main dashboard & menu