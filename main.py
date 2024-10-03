"""
program: main.py

purpose: Implement a to-do list

comments: 

author: Russell Folks

history:
-------
09-20-2024  creation
09-30-2024  Add second toplevel window.
"""
"""
TODO: - put spacing rules for Tk widgets into a cnf dict.
"""
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

msel = SourceFileLoader("ui_multi_select", "../ui_RF/ui_multi_select.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def sort_cat():
    print(f'in sort_cat')

    # get data
    # --------
    category_list = [item.winfo_children()[0].get() for item in item_rows]
    text_list = [item.winfo_children()[1].get() for item in item_rows]

    # report data found
    # -----------
    print(f'cbox values: {category_list}')
    print(f'entry items: {text_list}')
    print(f'    items: {len(text_list)}')

    # i1 = item_rows[0]
    # print(f'i1[0] is {type(i1.winfo_children()[0])}')
    # the Combobox:
    # print(f'item_rows[0] is {type(item_rows[0].winfo_children()[0])}')

    # print(f'    .winfo_children()[0] holds {i1.winfo_children()[0].get()}')
    # print(f'i1[1] is {type(i1.winfo_children()[1])}')
    # print(f'    .winfo_children()[1] holds {i1.winfo_children()[1].get()}')

    # put data in output window
    # --------
    text_main.delete('1.0', 'end')
    for n, i in enumerate(text_list):
        # sanity check
        # print(f'n: {n}, i: {i}')

        st = str(n) + ": " + i
        # end_point = text_main.index('end')
        # insert_point = end_point + ' + 1c'

        text_main.insert('end', st)
        text_main.insert('end', '\n')
                         

# Module scope objects
# ====================
root = tk.Tk()
root.title('list manager')
# root.geometry('400x300')

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

main_lab = ttk.Label(root, foreground='blue', border=2, text='Create List')
main_lab.pack(anchor='w')

main_list_fr = ttk.Frame(root, border=2)

text1 = ttk.Label(root, background='#ff0', text='build list')
text1.pack(anchor='n')



rowframe = msel.create_selection_row(windows)
rowframe.grid(row=0, column=0, sticky='nw')


filt_cboxes.append(rowframe.winfo_children()[0])
filt_entries.append(rowframe.winfo_children()[1])
filt_buttons_subt.append(rowframe.winfo_children()[2])
filt_buttons_add.append(rowframe.winfo_children()[3])

item_rows.append(rowframe)

main_list_fr.pack(padx=10, pady=10, ipadx=5, ipady=5)

btn_sort = ttk.Button(root, text='Sort Category', command=sort_cat)
btn_sort.configure(style='MyButton1.TButton')
btn_sort.pack(anchor='s', pady=10)

btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.configure(style='MyButton1.TButton')
btnq.pack(anchor='s', pady=10)

root.update()
print(f'root geometry: {root.geometry()}')

# Toplevel window 2
# -----------------
top2 = tk.Toplevel(root)
top2.geometry("+200+200")

frm1_2 = ttk.LabelFrame(top2, text="Formatted List")
frm1_2.pack(padx=5, pady=5)

win_label = ttk.Label(frm1_2, text="label frame",
                     style="EntryLabel.TLabel")
win_label.pack(padx=5, pady=5)

output_1_fr = ttk.Frame(frm1_2)
output_1_fr.pack(padx=5, pady=5)

st_entry = ttk.Entry(output_1_fr, name="studio")
st_entry.pack(padx=5, pady=5)

text_main = tk.Text(output_1_fr, width=40, height=10, background='#ffa')
text_main.pack(padx=5, pady=5)


root.mainloop()
