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
"""
"""
TODO: - put common pack() spacing into a cnf dict.
"""
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

msel = SourceFileLoader("ui_multi_select", "../ui_RF/ui_multi_select.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def move_text(source: list) -> None:
    """Get text from widgets and move it to another toplevel window."""

    category_list = [item.winfo_children()[0].get() for item in item_rows]
    text_list = [item.winfo_children()[1].get() for item in item_rows]

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
    # print(f'alltext:\n{alltext}')

    line_list = alltext.split('\n')
    # print(f'line 1:\n{line_list[0]}')

    # test    
    # regex is a better tool, but trades off complexity.
    category_list = [line.split('-')[1].split(':')[0] for line in line_list[:-1]]
    print(f'category_list: {category_list}')
    # print(f'first line category:\n{category_list[0]}')

    line_list_unnum = [line.split('-')[1] for line in line_list[:-1]]
    print(f'lines, unnumbered:\n{line_list_unnum}')
    print()

    sort_cat_list = sorted(line_list_unnum)
    print(f'lines, sorted:\n{sort_cat_list}')

    # replace output with sorted list
    text_main.delete('1.0', 'end')
    linenum = 1

    for i in enumerate(sort_cat_list):
        st = str(linenum) + "-" + i[1]
        text_main.insert('end', st)
        text_main.insert('end', '\n')
        linenum += 1


def option2():
    print('in option2')


# Module scope objects
# ====================
root = tk.Tk()
root.title('list manager')

sttk.CreateStyles()

# flags
use_pandas = False

item_rows = []
filt_cboxes = []
filt_entries = []
filt_buttons_add = []
filt_buttons_subt = []

data_columns = ['home', 'work', 'hobby']

# test functions passed to the imported module msel
# my_fxn = None
# def opt_fxn():
#      print('in opt_fxn')


main_lab = ttk.Label(root, foreground='blue', border=2, text='Create List')
main_lab.pack(anchor='w', padx=5)

main_list_fr = ttk.Frame(root, border=2)

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

geom_str = root.geometry().split('x')
win_wd = geom_str[0]
win_ht = geom_str[1].split('+')[0]

win_hoff = geom_str[1].split('+')[1]
win_voff = geom_str[1].split('+')[2]

# Toplevel window 2
# =================
top2 = tk.Toplevel()
top2.title('list viewer')

top2_h_offset = str(int(win_wd) + int(win_hoff))
top2_v_offset = win_ht
offset_string = "+" + top2_h_offset + "+" + top2_v_offset

top2.geometry(offset_string)

lab2 = ttk.Label(top2, text="Formatted List", style="LabelFrameText.TLabel")
main_fr = ttk.LabelFrame(top2, labelwidget=lab2)
main_fr.pack(padx=5, pady=5)

options_fr = ttk.Frame(top2, relief='groove')
options_fr.pack(padx=5, pady=5, ipadx=5, ipady=5)

opt1_but = ttk.Button(options_fr, text="sort category", command=sort_category)
opt1_but.pack(side='left', padx=5, pady=5)

opt2_but = ttk.Button(options_fr, text="option 2", command=option2)
opt2_but.pack(side='left', padx=5, pady=5)

text_main = tk.Text(main_fr, width=40, height=10, background='#ffa')
text_main.pack(padx=5, pady=5)

# print(f'item_rows[0] child 0 is {type(item_rows[0].winfo_children()[0])}')

if __name__ == "__main__":
    root.mainloop()
