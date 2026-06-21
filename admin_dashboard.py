import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AdminDashboard:

    def __init__(self, root,db):

        self.root = root
        self.db = db

        self.create_dashboard()

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def create_dashboard(self):
        total_users = self.db.get_total_users()
        total_games = self.db.get_total_games_played()
        average_score = self.db.get_average_score()

        self.clear_window()

        self.root.title("Admin Dashboard")
        self.root.geometry("800x600")

        # ==========================
        # Menu Bar
        # ==========================

        menu_bar = tk.Menu(self.root)

        menu_bar.add_command(
            label="Scores",
            command=self.open_scores
        )

        menu_bar.add_command(
            label="About",
            command=self.open_about
        )

        menu_bar.add_command(
            label="Logout",
            command=self.logout
        )

        self.root.config(menu=menu_bar)

        # ==========================
        # Statistics
        # ==========================

        tk.Label(
            self.root,
            text="ADMIN DASHBOARD",
            font=("Arial",20,"bold")
        ).pack(pady=10)

        tk.Label(
            self.root,
            text=f"Total Users : {total_users}"
        ).pack()

        tk.Label(
            self.root,
            text=f"Total Games : {total_games}"
        ).pack()

        tk.Label(
            self.root,
            text=f"Average Score : {average_score}"
        ).pack()

        # ==========================
        # Bar Chart
        # ==========================

        data = self.db.get_game_high_scores()

        games = []
        scores = []

        for game, score in data:
            games.append(game)
            scores.append(score)

        plt.close('all') # 👈 ADD THIS LINE HERE to release old charts from memory!

        fig, ax = plt.subplots(figsize=(5,3))

        bars = ax.bar(games, scores)

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom"
            )

        ax.set_title(
            "Highest Score Achieved By Users"
        )

        ax.set_ylabel("Score")

        chart = FigureCanvasTkAgg(
            fig,
            self.root
        )

        chart.draw()
        chart.width=600

        chart.get_tk_widget().pack(pady=20)

    def open_scores(self):
        from admin_scores import AdminScoresPage

        AdminScoresPage(
            self.root,
            self
        )

    def open_about(self):
        from about import AboutPage
        AboutPage(self.root,self)


    def logout(self):

        from login_register import LoginRegisterSystem

        self.root.config(menu="")

        LoginRegisterSystem(
            self.root,self.db)