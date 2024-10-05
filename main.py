"""
program: main.py

purpose: Implement a list manager

comments: There are two toplevel windows, one to create the list and 
          one to display it, formatted.

author: Russell Folks

history:
-------
09-20-2024  creation
09-30-2024  Add second toplevel window, top2.
10-04-2024  Refine top2. Rename sort_cat to move_text. Add line separator in
            the output. Remove old comments and print()s.
"""
"""
TODO: - put spacing rules for Tk widgets into a cnf dict.
"""
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

msel = SourceFileLoader("ui_multi_select", "../ui_RF/ui_multi_select.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def opt_fxn():
    move_text(item_rows)


def move_text(source):
    # get text
    # category_list = [item.winfo_children()[0].get() for item in item_rows]
    # text_list = [item.winfo_children()[1].get() for item in item_rows]
    category_list = [item.winfo_children()[0].get() for item in source]
    text_list = [item.winfo_children()[1].get() for item in source]

    # put text in output window
    text_main.delete('1.0', 'end')
    linenum = 1
    for n, i in enumerate(category_list):
        # st = str(n+1) + "-" + i +  ": " + text_list[n]

        # end_pt = text_main.index('end')
        # insert_pt = end_pt + ' + 1c'
        separator = '--'

        # if i != '' and text_list[n] != '':
        #     text_main.insert('end', st)
        #     text_main.insert('end', '\n')
        # else:
        #     text_main.insert('end', '\n')
        if i == '':
            if text_list[n] == '':
                text_main.insert('end', '\n')
            else:
                if text_list[n] == '-':
                    text_main.insert('end', separator)
                    text_main.insert('end', '\n')
        else:
            if text_list[n] != '':
                st = str(linenum) + "-" + i +  ": " + text_list[n]
                text_main.insert('end', st)
                text_main.insert('end', '\n')
                linenum += 1


# Module scope objects
# ====================
root = tk.Tk()
root.title('list manager')

sttk.CreateStyles()

item_rows = []

filt_cboxes = []
filt_entries = []
filt_buttons_add = []
filt_buttons_subt = []

# used in ui_multi_select functions, but
# not needed for this app
# windows = {'one': None, 'two': None}

data_columns = ['home', 'work', 'hobby']
my_fxn = None

main_lab = ttk.Label(root, foreground='blue', border=2, text='Create List')
main_lab.pack(anchor='w', padx=5)

main_list_fr = ttk.Frame(root, border=2)

# text1 = ttk.Label(root, background='#ff0', text='build list')
# text1.pack(anchor='n')

category_label = ttk.Label(root, background='#ff0', text='category')
category_label.pack(anchor='w', padx=15)

rowframe = msel.create_selection_row()
rowframe.grid(row=0, column=0, sticky='nw')

filt_cboxes.append(rowframe.winfo_children()[0])
filt_entries.append(rowframe.winfo_children()[1])
filt_buttons_subt.append(rowframe.winfo_children()[2])
filt_buttons_add.append(rowframe.winfo_children()[3])

item_rows.append(rowframe)

main_list_fr.pack(padx=10, ipadx=5, ipady=5)

btn_sort = ttk.Button(root,
                      text='Move Text',
                      command=lambda src=item_rows: move_text(src))
btn_sort.configure(style='MyButton1.TButton')
btn_sort.pack(anchor='s', pady=10)

btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.configure(style='MyButton1.TButton')
btnq.pack(anchor='s', pady=10)

root.update()
rgeom = root.geometry()
# print(f'root geometry: {rgeom}')
geom_str = rgeom.split('x')
win_wd = geom_str[0]
win_ht = geom_str[1].split('+')[0]
# print(f'root width/height: {win_wd}, {win_ht}')

win_hoff = geom_str[1].split('+')[1]
win_voff = geom_str[1].split('+')[2]
# print(f'root h,v offsets: {win_hoff}, {win_voff}')

# Toplevel window 2
# -----------------
top2 = tk.Toplevel()
top2.title('list viewer')
# top2.geometry("+300+250")
top2_h_offset = str(int(win_wd) + int(win_hoff))
top2_v_offset = win_ht
top2_offs_str = "+" + top2_h_offset + "+" + top2_v_offset
# print(top2_offs_str)
top2.geometry(top2_offs_str)

# options_fr = ttk.Frame(frm1_2, relief='groove')
# options_fr.pack(padx=5, pady=5, ipadx=5, ipady=5)

# win_label = ttk.Label(options_fr, text="label frame",
#                      style="EntryLabel.TLabel")
# win_label.pack(padx=5, pady=5)

main_fr = ttk.LabelFrame(top2, text="Formatted List")
main_fr.pack(padx=5, pady=5)

text_main = tk.Text(main_fr, width=40, height=10, background='#ffa')
text_main.pack(padx=5, pady=5)

root.mainloop()