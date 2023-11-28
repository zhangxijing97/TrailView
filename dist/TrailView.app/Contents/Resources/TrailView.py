import tkinter as tk
from tkinter import messagebox

def show_message():
    messagebox.showinfo("Message", "Hello, macOS!")

# Create the main application window
root = tk.Tk()
root.title("My macOS App")

# Create a button and associate it with the show_message function
button = tk.Button(root, text="Click Me", command=show_message)
button.pack(padx=20, pady=20)  # Add some padding around the button

# Run the Tkinter event loop
root.mainloop()