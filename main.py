"""
program: main.py

purpose: main module for project list_manager_RF: implement a list manager

comments: There are two toplevel windows, one to create the list and 
          one to display it, formatted.

          No Artificial Intelligence was used in production of this code.

author: Russell Folks

history:
-------
09-20-2024  creation
...         (see history.txt)
01-14-2026  Code a method to sort text lines by category.
01-15-2026  Remove old function versions.
01-27-2026  Implement cnf (configuration dict) for some pack() steps.
02-02-2026  Implement subsort category / text item.
02-05-2026  Combine sort and subsort functions into one.
07-01-2026  Remove some old assignment syntax.
07-04-2026  Move some example code to notes.txt.
08-01-2026  Refactor set_window_offset().
08-07-2026  Use loal item_rows to keep track of MultiSelectFrame objects in UI.
"""
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk

msel = SourceFileLoader("msel", "../utilities/tool_classes.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def get_list(source: list) -> list | None:
    """Get contents for a list of widgets."""
    if len(source) == 0:
        return

    # This syntax depends on knowing that we need to skip the last 2 widgets.
    # To generalize this function, the '2' would be a value passed in.
    rows = [item.winfo_children()[:-2] for item in source]

    # works: direct assignment to the type
    the_list = []
    for row in rows:
        l = Lineitem(row[0].get(), row[1].get())
        the_list.append(l)

    return the_list


def move_text() -> None:
    """Move text from one toplevel window to another."""

    # In this app, these could be module vars:
    #     'indicator', 'separator', 'top2', 'text_main'

    global main_list_fr
    global top2

    source_wid_list = main_list_fr.winfo_children()

    raw_list = get_list(source_wid_list)

    if len(raw_list) == 1 and raw_list[0].text == '':
        # no input
        return

    # get the Text widget in the first Frame widget
    # method 1: if there is one frame with one text widget:
    text_main = top2.winfo_children()[0].winfo_children()[0]
    # method 2: >= 1 frame, >= 1 text widget
    frames = [w for w in top2.winfo_children() if w.__class__ == ttk.Frame]

    # print(f'    {frames=}')
    textw = [w for w in frames[0].winfo_children() if w.__class__ == tk.Text]
    # print(f'    {textw=}')

    text_main.delete('1.0', 'end')

    write_text(raw_list, indicator, separator, text_main)


def write_text(the_list: list,
               indicator: str,
               separator: str,
               text_main: 'tk.Text') -> None:
    """Write a list of text lines into a Text object.

    Args:
        the_list: list of text strings
        indicator: character at the beginning of each line
        separator: 1+ characters between the category and the text content
        text_main: the write target
    """
    linenum = 1
    # print(f'{type(text_main)=}')
    for n, i in enumerate(the_list):
        if i == '':
            if the_list[n].text == '-':
                text_main.insert('end', indicator)
        else:
            if the_list[n].category != '':
                output_line = str(n + 1) + indicator + i.category + separator + i.text

                text_main.insert('end', output_line)
                linenum += 1
        text_main.insert('end', '\n')


def sort_by_category(subsort=False) -> None:
    """Sort a list of text lines, of the format 'linenumber-category: text'

    Args:
        subsort: flag to sort by text content in addition to category.
                 This responds to the `subsort` button.
    """

    # This could also be passed in via a lambda callback.
    global main_list_fr

    # After the first line, remove category text
    trim_cat = True

    source_wid_list = main_list_fr.winfo_children()
    raw_list = get_list(source_wid_list)
    if len(raw_list) == 1 and raw_list[0].text == '':
        # no input
        return

    sorted_list = []
    categories_sorted = sorted(categories)
    for c in categories_sorted:
        items = [i for i in raw_list if i.category == c]
        if len(items) == 0:
            continue

        if subsort:
            items_sorted = sorted(items, key=lambda item: item.text)
        else:
            items_sorted = items

        sorted_list.append(items_sorted[0])
        for n, line in enumerate(items_sorted[1:]):
            if trim_cat:
                line.category = ' ' * len(line.category)
            sorted_list.append(line)

    text_main = top2.winfo_children()[0].winfo_children()[0]
    text_main.delete('1.0', 'end')

    write_text(sorted_list, indicator, separator, text_main)


def set_window_offset_old(reference):
    """Calculate window position, as offset from the `reference` window ."""
    top2_width = reference[0]
    top2_height = reference[1].split('+')[0]
    h_offset = reference[1].split('+')[1]
    v_offset = reference[1].split('+')[2]      # not currently used

    top2_h_offset = str(int(top2_width) + int(h_offset) + 20)
    top2_v_offset = top2_height
    # print(f'{top2_h_offset=}, {top2_v_offset=}')

    return "+" + top2_h_offset + "+" + top2_v_offset


def set_window_offset(reference):
    """Calculate window position, as offset from the `reference` window ."""

    # this version defines its own geometry string

    the_string = reference.geometry().split('x')

    ref_width = the_string[0]
    ref_height = the_string[1].split('+')[0]
    h_offset = the_string[1].split('+')[1]
    v_offset = the_string[1].split('+')[2]      # not currently used

    print(f'{ref_width}, {ref_height}, {h_offset}, {v_offset}')

    top2_h_offset = str(int(ref_width) + int(h_offset) + 20)
    top2_v_offset = ref_height

    print(f'{top2_h_offset=}, {top2_v_offset=}')

    return "+" + top2_h_offset + "+" + top2_v_offset


# Module scope objects
# ====================
root = ThemedTk()
root.title('Create List')
root.geometry('+20+20')

sttk.create_styles()

cnf1 = {'padx':5, 'pady':5}
cnf2 = {'anchor': 'w', 'padx': 15}

# See the project pandas_data_RF
use_pandas = False
item_rows = []

# example type
# def point_init(thispoint, xval: int, yval: int):
#     thispoint.xval = xval
#     thispoint.yval = yval
#
# Point = type('Point', (), {"__init__": point_init})

def lineitem_init(i,
                  cat: str,
                  item: str):
    i.category = cat
    i.text = item

categories = ['home', 'work', 'hobby']
Lineitem = type('Lineitem', (), {"__init__": lineitem_init})

# test type:
# ii_one = Lineitem('home', 'item 1 home')
# print(f'{ii_one.category=}, {ii_one.text}')

indicator = "--"
separator = ": "

# test passing of functions to the imported module msel
# my_fxn = None
# def opt_fxn():
#      print('in opt_fxn')

main_fr_label = ttk.Frame(root)
main_fr_label.pack(cnf1)
# ? do we need this
category_label = ttk.Label(main_fr_label, background='#ff0', text='category')
category_label.pack(cnf=cnf2)

main_list_fr = ttk.Frame(main_fr_label, border=2)
main_list_fr.pack(padx=10, ipadx=5, ipady=5)

setattr(msel.MultiSelectFrame, 'padding', 0)    # class default is 5

rowframe = msel.MultiSelectFrame(main_list_fr,
                                 cb_values=categories,
                                 name='row1',
                                 posn=[0,0],
                                 )
item_rows.append(rowframe)

btn_sort = ttk.Button(root,
                      text='Move Text',
                      command=move_text)
btn_sort.configure(style='MyButton1.TButton')
btn_sort.pack(anchor='s', pady=10)

btnq = ttk.Button(root,
                  text='Quit',
                  command=root.destroy)
btnq.configure(style='MyButton1.TButton')
btnq.pack(anchor='s', pady=10)

root.update()
root_geometry = root.geometry().split('x')

# Toplevel window 2
# =================
top2 = tk.Toplevel()
top2.title('Format List')

# win2_offset = set_window_offset(root_geometry)
win2_offset = set_window_offset(root)
top2.geometry(win2_offset)
top2.update()

format_list_fr = ttk.Frame(top2)#, name="format_frame")
format_list_fr.pack(cnf1, fill='y', expand=True)

options_fr = ttk.Frame(top2, relief='groove')
options_fr.pack(cnf1)

opt1_but = ttk.Button(options_fr, text="sort category", command=sort_by_category)
opt1_but.pack(cnf1, side='left')

opt2_but = ttk.Button(options_fr, text="subsort", command=lambda s=True: sort_by_category(s))
opt2_but.pack(cnf1, side='left')

text_main = tk.Text(format_list_fr, width=40, height=10, background='#ffa')#, name="formatted_text")
text_main.pack(cnf1)

# report function signatures. ----------
# import inspect

# print('move_text:')
# sig = (inspect.signature(move_text))
# print(f'   signature: {sig}')
# ---------- END report

if __name__ == "__main__":
    root.mainloop()
