import tkinter as tk


class ProfilePage:

    def __init__(self, root, user_id, db, dashboard):

        self.root = root
        self.user_id = user_id
        self.db = db
        self.dashboard = dashboard

        self.create_page()

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def create_page(self):

        self.clear_window()

        profile = self.db.get_user_profile(self.user_id)

        username = profile[0]
        age = profile[1]
        favourite_game = profile[2]

        games_played = self.db.get_games_played(self.user_id)

        user = {
        "username": username,
        "age": age,
        "favourite_game": favourite_game,
        "games_played": games_played}

        tk.Label(
            self.root,
            text="PROFILE",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text=f"Username : {user['username']}"
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Age : {user['age']}"
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Favourite Game : {user['favourite_game']}"
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Total Games Played : {user['games_played']}"
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Back",
            width=20,
            command=self.go_back
        ).pack(pady=20)

    def go_back(self):
        self.root.config(menu="")
        self.dashboard.create_dashboard()
