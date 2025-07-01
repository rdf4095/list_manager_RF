"""
program: main.py

purpose: main module for project list_manager_RF: implement a list manager

comments: There are two toplevel windows, one to create the list and 
          one to display it, formatted.

author: Russell Folks

history:
-------
09-20-2024  creation
09-30-2024  Add second toplevel window, top2.
10-04-2024  Refine top2. Rename sort_cat to move_text. Add line separator in
            the output. Remove old comments and print()s.
10-10-2024  Add option buttons for top2, the text output window.
            Remove debug print statements and unused variables (already 
            commented out).
10-11-2024  Add function sort_category to resort output text by item category.
10-18-2024  Remove counter from enumerate in sort_category(). Test functions
            passed to the msel module. Remove inactive code.
10-19-2024  Add flag 'use_pandas' for the UI code. Update the associated 
            README.md file.
11-02-2024  Add arguments when calling msel.create_selection_row. i.e. don't 
            depend on those values being found by msel.
11-19-2024  Update the README file. Remove a few print statements.
11-29-2024  Use ThemedTk. Change some variable names for clarity and
            consistency. Add set_window_offset() to position top2.
11-29-2024  Recommit.
05-26-2025  Use code in ui_RF to handle the widget ui setup and interaction.
06-03-2025  Add get_list() to compile list of widget values from all rows.
            Remove a lot of print statements.
06-12-2025  Use utilities/tool_classes.py for widget classes.
"""
"""
TODO: 
    1. Put common pack() spacing into a cnf dict.
    2. Use LabelFrame in the root window, like it's used for the top2 window.
"""

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk

# msel = SourceFileLoader("msel", "../ui_RF/ui_multi_select.py").load_module()
msel = SourceFileLoader("msel", "../utilities/tool_classes.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()


def get_list(source: list, wid: str) -> list:
    """Get contents for a list of widgets of class wid."""
    list_item = 0
    for index, item in enumerate(source):
        if type(item.winfo_children()[index]).__name__ == wid:
            list_item = index

    the_list = [item.winfo_children()[list_item].get() for item in source]

    return the_list


def move_text() -> None:
    """Get text from widgets and move it to another toplevel window."""
    global main_list_fr
    global top2

    source = main_list_fr.winfo_children()

    category_list = get_list(source, 'Combobox')
    text_list = get_list(source, 'Entry')

    text_main = top2.winfo_children()[0].winfo_children()[0]
    text_main.delete('1.0', 'end')

    linenum = 1
    for n, i in enumerate(category_list):
        separator = '--'

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


def sort_category() -> None:
    """Sort a list of text lines.

     Lines are of the format '1-category: text'
     where
        1 is the line number
        - is a separator
        category is probably from a Combobox or Listbox
        : is a separator
        text is user-entered contents of an Entry
    """
    global text_main

    alltext = text_main.get('1.0', 'end-1c')
    line_list = alltext.split('\n')

    # may use a list of categories in the future
    # regex may be a better tool, but trades off complexity.
    # category_list = [line.split('-')[1].split(':')[0] for line in line_list[:-1]]

    line_list_unnum = [line.split('-')[1] for line in line_list[:-1]]
    sort_cat_list = sorted(line_list_unnum)
    text_main.delete('1.0', 'end')

    linenum = 1
    for i in enumerate(sort_cat_list):
        st = str(linenum) + "-" + i[1]
        text_main.insert('end', st)
        text_main.insert('end', '\n')
        linenum += 1


def option2():
    # future
    print('in option2')


def set_window_offset(reference):
    """Calculate window position, as x-y offset from a reference window."""
    top2_width = reference[0]
    top2_height = reference[1].split('+')[0]
    h_offset = reference[1].split('+')[1]
    # v_offset = reference[1].split('+')[2]

    top2_h_offset = str(int(top2_width) + int(h_offset) + 40)
    top2_v_offset = top2_height

    # offset_string = "+" + top2_h_offset + "+" + top2_v_offset

    return "+" + top2_h_offset + "+" + top2_v_offset


# Module scope objects
# ====================
root = ThemedTk()
root.title('list manager')

sttk.create_styles()

# for how this flag might be used, see the project pandas_data_RF
use_pandas = False

data_columns = ['home', 'work', 'hobby']

# test passing of functions to the imported module msel
# my_fxn = None
# def opt_fxn():
#      print('in opt_fxn')

main_lab = ttk.Label(root, foreground='blue', border=2, text='Create List')
main_lab.pack(anchor='w', padx=5)

category_label = ttk.Label(root, background='#ff0', text='category')
category_label.pack(anchor='w', padx=15)

main_list_fr = ttk.Frame(root, border=2)
main_list_fr.pack(padx=10, ipadx=5, ipady=5)

rowframe = msel.init_selection_row(main_list_fr, data_columns)#, label='entry')

btn_sort = ttk.Button(root,
                      text='Move Text',
                      command=move_text)
btn_sort.configure(style='MyButton1.TButton')
btn_sort.pack(anchor='s', pady=10)

btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.configure(style='MyButton1.TButton')
btnq.pack(anchor='s', pady=10)

root.update()

root_geometry = root.geometry().split('x')

# Toplevel window 2
# =================
top2 = tk.Toplevel()
top2.title('list viewer')

win2_offset = set_window_offset(root_geometry)
top2.geometry(win2_offset)

lab2 = ttk.Label(top2, text="Formatted List", style="LabelFrameText.TLabel")
main_fr = ttk.LabelFrame(top2, labelwidget=lab2)
main_fr.pack(padx=5, pady=5)

options_fr = ttk.Frame(top2, relief='groove')
options_fr.pack(padx=5, pady=5)

opt1_but = ttk.Button(options_fr, text="sort category", command=sort_category)
opt1_but.pack(side='left', padx=5, pady=5)

opt2_but = ttk.Button(options_fr, text="option 2", command=option2)
opt2_but.pack(side='left', padx=5, pady=5)

text_main = tk.Text(main_fr, width=40, height=10, background='#ffa')
text_main.pack(padx=5, pady=5)

# print(f'item_rows[0] child 0 is {type(item_rows[0].winfo_children()[0])}')

# optional: report function signatures.
# import inspect

# print('move_text:')
# sig = (inspect.signature(move_text))
# print(f'   signature: {sig}')

if __name__ == "__main__":
    root.mainloop()
