import tkinter as tk

class StatisticsPage:

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
            text="MY STATISTICS",
            font=("Arial",20,"bold")
        ).pack(pady=20)

        data = self.dashboard.db.get_user_high_scores(
            self.dashboard.user_id
        )

        highest = 0

        for game, score in data:

            tk.Label(
                self.root,
                text=f"{game} : {score}",
                font=("Arial",12)
            ).pack()

            if score > highest:
                highest = score

        tk.Label(
            self.root,
            text=f"Highest Overall : {highest}",
            font=("Arial",14,"bold")
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Back",
            width=20,
            command=self.go_back  # 👈 Change this from self.dashboard.create_dashboard
        ).pack(pady=10)

    # Add this clean transition helper method to the class
    def go_back(self):
        self.root.config(menu="")  # Clear the menu configuration completely
        self.dashboard.create_dashboard()  # Safely rebuild the main dashboard & menu