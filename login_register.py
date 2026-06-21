import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginRegisterSystem:

    def __init__(self,root,db):

        self.root = root
        self.root.title("Game Collection System")
        self.root.geometry("500x600")
        #self.root.resizable(False, False)

        self.db = db

        self.login_page()

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================================
    # LOGIN PAGE
    # ==================================

    def login_page(self):

        self.clear_window()

        # Logo
        image = Image.open("images/logo.png")
        image = image.resize((400, 150))
        self.logo = ImageTk.PhotoImage(image)
        tk.Label(self.root,image=self.logo).pack(pady=20)

        tk.Label(
            self.root,
            text="Username:"
        ).pack(pady=5)

        self.username_entry = tk.Entry(
            self.root,
            width=30
        )
        self.username_entry.pack()

        tk.Label(
            self.root,
            text="Password:"
        ).pack(pady=5)

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            show="*"
        )
        self.password_entry.pack()

        tk.Button(
            self.root,
            text="LOGIN",
            width=15,
            command=self.login
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="REGISTER",
            width=15,
            command=self.register_page
        ).pack(pady=20)

        tk.Button(self.root,
            text="EXIT",
            width=15,
            command=self.root.destroy
        ).pack(pady=20)

    # ==================================
    # REGISTER PAGE
    # ==================================

    def register_page(self):

        self.clear_window()

        #Logo
        image = Image.open("logo.png")
        image = image.resize((400, 150))
        self.logo = ImageTk.PhotoImage(image)
        tk.Label(self.root,image=self.logo).pack(pady=20)

        tk.Label(
            self.root,
            text="Username:"
        ).pack(pady=5)

        self.reg_username = tk.Entry(
            self.root,
            width=30
        )
        self.reg_username.pack()

        tk.Label(
            self.root,
            text="Password:"
        ).pack(pady=5)

        self.reg_password = tk.Entry(
            self.root,
            width=30,
            show="*"
        )
        self.reg_password.pack()

        tk.Label(self.root,text="Age:").pack(pady=5)
        self.age_entry = tk.Entry(self.root,width=30)
        self.age_entry.pack()

        tk.Label(self.root,text="Favourite Game:").pack(pady=5)
        self.game_entry = ttk.Combobox(self.root, width = 30, textvariable = tk.StringVar(), takefocus = False)
        self.game_entry['values'] = ('Snake','2048','Tetris','Rapid Roll')
        self.game_entry.pack()

        tk.Button(
            self.root,
            text="REGISTER",
            width=15,
            command=self.register
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="BACK",
            width=15,
            command=self.login_page
        ).pack(pady=20)

        tk.Button(self.root,
            text="EXIT",
            width=15,
            command=self.root.destroy
        ).pack(pady=20)

    # ==================================
    # LOGIN FUNCTION
    # ==================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "" or password == "":

            messagebox.showerror(
                "Error",
                "Please enter username and password."
            )
            return

        user = self.db.login_user(
            username,
            password,
        )

        if user:
            # Open dashboard here
            user_id = user[0]
            username = user[1]
            role = user[5]
            if role == "admin":
                from admin_dashboard import AdminDashboard
                AdminDashboard(self.root,self.db)

            else:
                from dashboard import Dashboard
                Dashboard(self.root,user_id,username,self.db)

        else:

            messagebox.showerror(
                "Error",
                "Invalid username or password."
            )

    # ==================================
    # REGISTER FUNCTION
    # ==================================

    def register(self):

        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        age = self.age_entry.get().strip()
        favourite_game = self.game_entry.get().strip()

        if username == "" or password == "":

            messagebox.showerror(
                "Error",
                "All fields are required."
            )
            return

        if self.db.user_exists(username):

            messagebox.showerror(
                "Error",
                "Username already exists."
            )
            return

        if not age.isdigit():
            messagebox.showerror("Error","Age must be a number.")
            return
        age = int(age)

        success = self.db.register_user(username,password,age,favourite_game)

        if success:

            messagebox.showinfo(
                "Success",
                "Account created successfully."
            )

            self.login_page()

        else:

            messagebox.showerror(
                "Error",
                "Registration failed."
            )

