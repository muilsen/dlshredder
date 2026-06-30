import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import json
import os
import shutil

VERSION = "1.0.0"
CONFIG_DATA = None

def init():
    try:
        with open("config.json") as f:
            global CONFIG_DATA
            CONFIG_DATA = json.loads(f.read())
            if CONFIG_DATA["project_filepath"] == "":
                CONFIG_DATA["project_filepath"] = os.getcwd()
            if CONFIG_DATA["download_folder_filepath"] == "":
                show_files_button.config(state="disabled")
            if CONFIG_DATA["quarantine_folder_filepath"] != "":
                quarantine_file_button.config(state="normal")
            if CONFIG_DATA["download_folder_filepath"] != "":
                shred_file_button.config(state="normal")
    except FileNotFoundError:
        messagebox.showwarning("dlshredder", "config file not found!")
        root.quit()
        exit()
    except Exception:
        messagebox.showerror("dlshredder", "something went wrong!")
        root.quit()
        exit()

def set_download_folder():
    new_filepath = filedialog.askdirectory()
    CONFIG_DATA["download_folder_filepath"] = new_filepath
    if CONFIG_DATA["download_folder_filepath"] != "":
        with open(fr"{CONFIG_DATA["project_filepath"]}\config.json", "w") as f:
            f.write(json.dumps(CONFIG_DATA))
        show_files_button.config(state="normal")
        shred_file_button.config(state="normal")
    else:
        messagebox.showwarning("dlshredder", "no valid folder was chosen.")

def set_quarantine_folder():
    new_filepath = filedialog.askdirectory()
    CONFIG_DATA["quarantine_folder_filepath"] = new_filepath
    if CONFIG_DATA["quarantine_folder_filepath"] != "":
        with open(fr"{CONFIG_DATA["project_filepath"]}\config.json", "w") as f:
            f.write(json.dumps(CONFIG_DATA))
        quarantine_file_button.config(state="normal")
    else:
        messagebox.showwarning("dlshredder", "no valid folder was chosen.")

def show_files():
    if CONFIG_DATA["download_folder_filepath"] != "":
        os.chdir(CONFIG_DATA["download_folder_filepath"])
        files = os.listdir()
        scrollable_text.config(state="normal")
        scrollable_text.delete("1.0", "end")
        for f in files:
            scrollable_text.insert("end", f"{f}\n")
        scrollable_text.config(state="disabled")
        file_entry.config(state="normal")
        shred_file_button.config(state="normal")
    else:
        messagebox.showerror("dlshredder", "incorrect file name.")
        root.quit()
        exit()

def shred():
    f = file_entry.get()
    files = os.listdir() 
    if f in files and f != "":
        try:
            os.remove(f)
            show_files()
        except PermissionError:
            messagebox.showwarning("dlshredder", "no permissions.")
    elif f == "":
        messagebox.showwarning("dlshredder", "file name cannot be empty.")
    else:
        messagebox.showinfo("dlshredder", f"couldn't find {f} in {os.getcwd()}")

def quarantine():
    f = file_entry.get()
    files = os.listdir()
    if f in files and f != "":
        try:
            shutil.move(f, CONFIG_DATA["quarantine_folder_filepath"])
            show_files()
        except PermissionError:
            messagebox.showwarning("dlshredder", "no permissions.")
    elif f == "":
        messagebox.showwarning("dlshredder", "file name cannot be empty.")
    else:
        messagebox.showinfo("dlshredder", f"couldn't find {f} in {os.getcwd()}")


def show_config():
    scrollable_text.config(state="normal")
    scrollable_text.delete("1.0", "end")
    for i in CONFIG_DATA:
        if CONFIG_DATA[i] == "":
            scrollable_text.insert("end", f"{i}:\nnot specified\n\n")
        else:
            scrollable_text.insert("end", f"{i}:\n{CONFIG_DATA[i]}\n\n")
    scrollable_text.config(state="disabled")

def clear_folder_data():    
    CONFIG_DATA["download_folder_filepath"] = ""
    CONFIG_DATA["quarantine_folder_filepath"] = ""
    show_files_button.config(state="disabled")
    file_entry.config(state="disabled")
    shred_file_button.config(state="disabled")
    quarantine_file_button.config(state="disabled")
    scrollable_text.config(state="normal")
    show_config()
    scrollable_text.config(state="disabled")
    with open(fr"{CONFIG_DATA["project_filepath"]}\config.json", "w") as f:
        f.write(json.dumps(CONFIG_DATA))

# ROOT
root = tk.Tk()
root.title(f"dlshredder (v{VERSION})")
root.geometry("900x400")
root.resizable(False, False)
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(True, icon)

# MENUBAR
menubar = tk.Menu(root)

set_menu = tk.Menu(menubar, tearoff=0)
set_menu.add_command(label=f"Set Downloads Folder", command=set_download_folder)
set_menu.add_command(label=f"Set Quarantine Folder", command=set_quarantine_folder)
set_menu.add_command(label="Clear Folder Data", command=clear_folder_data)

menubar.add_cascade(label="Folder", menu=set_menu)

# VIEW
view_frame = tk.Frame(root, bg="#CCCCCC")
view_frame.place(relwidth=0.65, relheight=0.9, relx=0.015, rely=0.5, anchor="w")
view_frame.pack_propagate(False)
scrollable_text = scrolledtext.ScrolledText(view_frame)
scrollable_text.pack(fill="both", side="left")
scrollable_text.config(state="disabled")

# CONTROL
control_frame = tk.Frame(root, bg="#CCCCCC")
control_frame.place(relwidth=0.3, relheight=0.9, relx=0.985, rely=0.5, anchor="e")

show_files_button = tk.Button(control_frame, text="Show Files", command=show_files)
show_files_button.place(relwidth=0.92, relheight=0.065, relx=0.5, rely=0.03, anchor="n")
file_entry = tk.Entry(control_frame, state="disabled")
file_entry.place(relwidth=0.92, relheight=0.06, relx=0.5, rely=0.12, anchor="n")
shred_file_button = tk.Button(control_frame, text="Shred File", state="disabled", command=shred)
shred_file_button.place(relwidth=0.92, relheight=0.065, relx=0.5, rely=0.2, anchor="n")
quarantine_file_button = tk.Button(control_frame, text="Quarantine File", state="disabled", command=quarantine)
quarantine_file_button.place(relwidth=0.92, relheight=0.065, relx=0.5, rely=0.28, anchor="n")
show_config_button = tk.Button(control_frame, text="Show config", command=show_config)
show_config_button.place(relwidth=0.92, relheight=0.065, relx=0.5, rely=0.9, anchor="n")

init()
root.config(menu=menubar)
root.mainloop()