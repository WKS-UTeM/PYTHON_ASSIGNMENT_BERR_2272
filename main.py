import tkinter as tk
from login_register import LoginRegisterSystem
from database import Database

db = Database()
root = tk.Tk()

app = LoginRegisterSystem(root,db)

root.mainloop()