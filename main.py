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
window.geometry('400x300')

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
    checkbox_set['state'] = 'disabled'
    checkbox_name['state'] = 'disabled'
    checkbox_type['state'] = 'disabled'

def enable_widg():
    
    button_update_DB['state'] = 'normal'
    button_export['state'] = 'normal'
    expansion_text['state'] = 'normal'
    name_text['state'] = 'normal'
    type_text['state'] = 'normal'
    checkbox_set['state'] = 'normal'
    checkbox_name['state'] = 'normal'
    checkbox_type['state'] = 'normal'

def on_closing():
        #mtg_db.close()
        window.destroy()

def export():

    cards = mtg_db.root.scryfall_cards
    progress_bar.pack()
    set_str = expansion_text.get()
    name_str = name_text.get()
    type_str = type_text.get()
    set_value_bool = set_value.get()
    name_value_bool = name_value.get()
    type_value_bool = type_value.get()


    args = {'name' : name_str, 'set' : set_str, 'type_line' : type_str}
    condition = {'name' : name_value_bool, 'set' : set_value_bool, 'type_line' : type_value_bool}
    where_set = {}
    where_exactly_set = {}

    for (key, val) in args.items():
        if (val!='') :
            if (condition[key] == False) :
                where_set[key] = val
            else :
                where_exactly_set[key] = val    
    progress_bar.start()
    mtg_set = cards.where_exactly(**where_exactly_set)
    mtg_set = mtg_set.where(**where_set)
    with open(directory_name + '\\estrazione.txt', 'w', encoding="utf-8") as f:
        f.write(mtg_set.pretty_print_str())        
    progress_bar.stop()
    progress_bar.pack_forget()

    enable_widg()

progress_bar = Progressbar(orient = HORIZONTAL, length = 100, mode ='indeterminate')

expansion_text = Entry()
name_text = Entry()
type_text = Entry()

set_value = BooleanVar()
name_value = BooleanVar()
type_value = BooleanVar()

checkbox_set = Checkbutton(text = 'exact match', variable=set_value, onvalue=True, offvalue=False)
checkbox_name = Checkbutton(text = 'exact match', variable=name_value, onvalue=True, offvalue=False)
checkbox_type = Checkbutton(text = 'exact match', variable=type_value, onvalue=True, offvalue=False)

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
checkbox_name.pack()
type_label.pack()
type_text.pack()
checkbox_type.pack()
expansion_label.pack()
expansion_text.pack()
checkbox_set.pack()
button_update_DB.pack()
button_export.pack()

name_text.lift()
type_text.lift()
expansion_text.lift()
button_update_DB.lift()
button_export.lift()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()