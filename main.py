"""
program: main.py

purpose: Implement a to-do list

comments: 

author: Russell Folks

history:
-------
09-20-2024  creation
"""
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

msel = SourceFileLoader("ui_multi_select", "../ui_RF/ui_multi_select.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

# Module scope objects
# ====================
root = tk.Tk()
root.title = 'list manager'
root.geometry('400x300')
sttk.CreateStyles()

item_rows = []

filt_cboxes = []
filt_entries = []
filt_buttons_add = []
filt_buttons_subt = []

# in the current version, this isn't used
windows = {'one': None, 'two': None}

data_columns = ['home', 'work', 'hobby']
my_fxn = None
data_1 = None

main_lab = ttk.Label(root, foreground='blue', border=2, text='Manage List')
main_lab.pack(anchor='w')

main_list_fr = ttk.Frame(root, border=2)

# text1 = ttk.Label(main_list_fr, background='#ff0', text='item 1 ')
# text1.grid(row=0, column=0, sticky='nw')
text1 = ttk.Label(root, background='#ff0', text='build list')
text1.pack(anchor='n')



rowframe = msel.create_selection_row(windows)
rowframe.grid(row=0, column=0, sticky='nw')


filt_cboxes.append(rowframe.winfo_children()[0])
filt_entries.append(rowframe.winfo_children()[1])
filt_buttons_subt.append(rowframe.winfo_children()[2])
filt_buttons_add.append(rowframe.winfo_children()[3])



item_rows.append(rowframe)
# print(f'rowframe type: {type(rowframe)}')

main_list_fr.pack(padx=10, pady=10, ipadx=5, ipady=5)

btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.configure(style='MyButton1.TButton')
btnq.pack(anchor='s', pady=10)


root.mainloop()
