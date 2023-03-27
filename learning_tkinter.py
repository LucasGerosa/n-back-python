import tkinter as tk
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from utils.defaults import *

root = tk.Tk()
root.title(PROJECT_NAME)
root.geometry("800x500")

label = tk.Label(root, text="hello world", font=('Arial', 18))
label.pack(pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10)

myentry = tk.Entry(root)
myentry.pack()


root.mainloop()