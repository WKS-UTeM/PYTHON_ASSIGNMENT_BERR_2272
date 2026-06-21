import tkinter as tk
from login_register import LoginRegisterSystem
import os
from PIL import Image, ImageTk

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Dashboard:

    def __init__(self,root,user_id,username,db):

        self.root = root

        self.user_id = user_id

        self.username = username

        self.db = db

        self.create_dashboard()

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def create_dashboard(self):

        self.clear_window()

        self.root.title("Game Collection Dashboard")
        self.root.geometry("800x600")

        # ===============================
        # LOAD GAME IMAGES
        # ===============================

        self.snake_img = ImageTk.PhotoImage(Image.open("images/snake.png").resize((100, 100)))
        self.game2048_img = ImageTk.PhotoImage(Image.open("images/2048.png").resize((100, 100)))
        self.tetris_img = ImageTk.PhotoImage(Image.open("images/tetris.png").resize((100, 100)))
        self.rapidroll_img = ImageTk.PhotoImage(Image.open("images/rapid_roll.png").resize((100, 100)))

        # ===============================
        # MENU BAR
        # ===============================

        menu_bar = tk.Menu(self.root)

        menu_bar.add_command(
            label="Profile",
            command=self.open_profile
        )

        menu_bar.add_command(
            label="Statistics",
            command=self.open_statistics
        )

        menu_bar.add_command(
            label="About",
            command=self.open_about
        )

        menu_bar.add_command(
            label="Logout",
            command=self.exit_system
        )

        self.root.config(menu=menu_bar)

        # ===============================
        # WELCOME MESSAGE
        # ===============================

        tk.Label(
            self.root,
            text=f"Welcome, {self.username}",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        # ===============================
        # GAME BUTTONS
        # ===============================

        game_frame = tk.Frame(self.root)
        game_frame.pack(pady=30)

        tk.Button(
            game_frame,
            text="SNAKE",
            image=self.snake_img,
            compound="top",
            width=200,
            height=150,
            command=self.open_snake
        ).grid(row=0, column=0, padx=20, pady=20)

        tk.Button(
            game_frame,
            text="2048",
            image=self.game2048_img,
            compound="top",
            width=200,
            height=150,
            command=self.open_2048
        ).grid(row=0, column=1, padx=20, pady=20)

        tk.Button(
            game_frame,
            text="TETRIS",
            image=self.tetris_img,
            compound="top",
            width=200,
            height=150,
            command=self.open_tetris
        ).grid(row=1, column=0, padx=20, pady=20)

        tk.Button(
            game_frame,
            text="RAPID ROLL",
            image=self.rapidroll_img,
            compound="top",
            width=200,
            height=150,
            command=self.open_rapid_roll
        ).grid(row=1, column=1, padx=20, pady=20)

    # ======================================
    # GAME FUNCTIONS
    # ======================================

    def open_snake(self):
        from snake import SnakeGame
        game = SnakeGame(self.user_id,self.username,self.db)
        game.run()

    def open_2048(self):
        from game_2048 import Game2048
        game = Game2048(self.user_id,self.username,self.db)
        game.run()

    def open_tetris(self):

        from tetris import TetrisGame
        game = TetrisGame(self.user_id,self.username,self.db)
        game.run()

    def open_rapid_roll(self):

        from rapid_roll import RapidRoll
        game = RapidRoll(self.user_id,self.username,self.db)
        game.run()

    # ======================================
    # MENU FUNCTIONS
    # ======================================

    def open_profile(self):

        from profile_page import ProfilePage
        ProfilePage(self.root,self.user_id,self.db,self)

    def open_statistics(self):

        from statistics import StatisticsPage
        StatisticsPage(self.root,self)

    def open_about(self):

        from about import AboutPage
        AboutPage(self.root,self)

    def exit_system(self):
        self.root.config(menu="")
        LoginRegisterSystem(self.root,self.db)