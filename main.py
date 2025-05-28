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
"""
# TODO: put common pack() spacing into a cnf dict.
# TODO: use LabelFrame in the root window, like it's used for the top2 window.

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk

msel = SourceFileLoader("msel", "../ui_RF/ui_multi_select.py").load_module()
toolf = SourceFileLoader("toolf", "../ui_RF/tool_frames.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def move_text_orig(source: list) -> None:
    """Get text from widgets and move it to another toplevel window."""

    # category_list = [item.winfo_children()[0].get() for item in item_rows]
    # text_list = [item.winfo_children()[1].get() for item in item_rows]
    print('in move_text')
    text_main = top2.winfo_children()[0].winfo_children()[0]

    category_list = [item.winfo_children()[0].get() for item in source]
    text_list = [item.winfo_children()[1].get() for item in source]

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


def move_text() -> None:
    """Get text from widgets and move it to another toplevel window."""

    # category_list = [item.winfo_children()[0].get() for item in item_rows]
    # text_list = [item.winfo_children()[1].get() for item in item_rows]
    global main_list_fr
    # source = root.winfo_children()[2]    # == main_list_fr
    source = main_list_fr.winfo_children()
    print(f'{source=}')
    text_main = top2.winfo_children()[0].winfo_children()[0]

    category_list = [item.winfo_children()[0].get() for item in source]
    text_list = [item.winfo_children()[1].get() for item in source]

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


def sort_category():
    """Sort text by item category."""
    print('in option1')
    
    alltext = text_main.get('1.0', 'end-1c')

    line_list = alltext.split('\n')

    # test    
    # regex is a better tool, but trades off complexity.
    # category_list = [line.split('-')[1].split(':')[0] for line in line_list[:-1]]
    # print(f'category_list: {category_list}')
    # print(f'first line category:\n{category_list[0]}')

    line_list_unnum = [line.split('-')[1] for line in line_list[:-1]]
    # print(f'lines, unnumbered:\n{line_list_unnum}')
    # print()

    sort_cat_list = sorted(line_list_unnum)
    # print(f'lines, sorted:\n{sort_cat_list}')

    # replace output with sorted list
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
    """Calculate window position, as an x-y offset from 'reference'  window."""
    top2_width = reference[0]
    top2_height = reference[1].split('+')[0]
    h_offset = reference[1].split('+')[1]
    # v_offset = reference[1].split('+')[2]

    top2_h_offset = str(int(top2_width) + int(h_offset))
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

# item_rows = []

# filt_cboxes = []
# filt_entries = []
# filt_buttons_add = []
# filt_buttons_subt = []

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

rowframe = msel.init_selection_row(main_list_fr, data_columns)

# rowframe.grid(row=0, column=0, sticky='nw')

# test ----------
# rowframe = msel.ToolFrame(main_list_fr, name='row1', posn=[0, 0])

# rowframe = msel.add_selection_row(None, main_list_fr, data_columns, None)

#      debug
# cbox_child1 = rowfr.winfo_children()[0]
# print(f'cbox_child1 is {cbox_child1}')

# cbox_1 = rowfr.cb
# cboxes.append(cbox_1)
# print(f'cbox_1 is {cbox_1}')
# print(f'cbox_1 is {cbox_1.name}')
#     end debug

# ----------  end test

# filt_cboxes.append(rowframe.winfo_children()[0])
# filt_entries.append(rowframe.winfo_children()[1])
# filt_buttons_subt.append(rowframe.winfo_children()[2])
# filt_buttons_add.append(rowframe.winfo_children()[3])

# item_rows.append(rowframe)

# btn_sort = ttk.Button(root,
#                       text='Move Text',
#                       command=lambda srcc=rowframe.item_rows: move_text(srcc))
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
