from mtgtools.MtgDB import MtgDB
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tkst
import threading
import os

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
directory_name = desktop + "\\MTGTool_Export\\"
DBPath = "C:\\temp\\"
mtg_db = MtgDB(DBPath + "my_db.fs")
window = Tk()
window.title('MTG Tool Export')
window.geometry('400x250')

try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")

try:
    os.mkdir(DBPath)
    print(f"Directory '{DBPath}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{DBPath}'.")

def Update_DB(event):
    disable_widg()
    mtg_db.scryfall_bulk_update()
    enable_widg()

def Export_exp(event):
    disable_widg()
    threading.Thread(target = export).start()

def disable_widg():
    
    button_update_DB['state'] = 'disabled'
    button_export['state'] = 'disabled'
    expansion_text['state'] = 'disabled'
    name_text['state'] = 'disabled'
    type_text['state'] = 'disabled'

def enable_widg():
    
    button_update_DB['state'] = 'normal'
    button_export['state'] = 'normal'
    expansion_text['state'] = 'normal'
    name_text['state'] = 'normal'
    type_text['state'] = 'normal'

def on_closing():
        #mtg_db.close()
        window.destroy()

def export():
    mtg_db.commit()
    cards = mtg_db.root.scryfall_cards
    progress_bar.pack()
    set_str = expansion_text.get()
    name_str = name_text.get()
    type_str = type_text.get()

    args = {'name' : name_str, 'set' : set_str, 'type_line' : type_str}
    real_args = {}

    for (key, val) in args.items():
        if (val!='') :
            real_args[key] = val
        
    progress_bar.start()
    mtg_set = cards.where_exactly(**real_args)
    with open(directory_name + '\\estrazione.txt', 'w', encoding="utf-8") as f:
        f.write(mtg_set.pretty_print_str())        
    progress_bar.stop()
    progress_bar.pack_forget()

    enable_widg()

progress_bar = Progressbar(orient = HORIZONTAL, length = 100, mode ='indeterminate')

expansion_text = Entry()
name_text = Entry()
type_text = Entry()

button_export = Button(text = "export")
button_export.bind("<Button-1>", Export_exp)
button_update_DB = Button(text = "Update")
button_update_DB.bind("<Button-1>", Update_DB)
button_close_DB = Button(text = "Close")

expansion_label = Label(window, text='Set :')
name_label = Label(window, text='Name :')
type_label = Label(window, text='Type :')

name_label.pack()
name_text.pack()
type_label.pack()
type_text.pack()
expansion_label.pack()
expansion_text.pack()
button_update_DB.pack()
button_export.pack()

name_text.lift()
type_text.lift()
expansion_text.lift()
button_update_DB.lift()
button_export.lift()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()