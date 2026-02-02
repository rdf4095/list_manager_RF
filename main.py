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
12-19-2025  Refactor get_list() to directly get text from all list widgets, as
            list of dicts; refactor move_text() to handle this list.
01-14-2026  Code a method to sort text lines by category.
01-15-2026  Remove old function versions.
01-27-2026  Implement cnf (configuration dict) for some pack() steps.
02-02-2026  Implement subsort category / text item.
"""

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk

msel = SourceFileLoader("msel", "../utilities/tool_classes.py").load_module()
sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def get_list(source: list) -> list | None:
    """Get contents for a list of widgets of class wid."""
    if len(source) == 0:
        return

    # print(f'in get_list...')

    # This syntax depends on knowing that we need to skip the last 2 widgets.
    # To generalize this function, the '2' would be a value passed in.
    rows = [item.winfo_children()[:-2] for item in source]

    # A model of the form for using a comprehension to flatten a list.
    # output = [i for subrow in rows for i in subrow]
    # works:
    # test_list = [i.get() for row in rows for i in row]

    # works: direct assignment to the type
    the_list = []
    for row in rows:
        l = Lineitem(row[0].get(), row[1].get())
        the_list.append(l)

    return the_list


def move_text() -> None:
    """Get text from widgets and move it to another toplevel window."""
    # NOTES:
    # Don't need the global keyword unless the module-level variable is being assigned.
    # Nevertheless, it is an indicator that another scope is being used.
    # consider the following alternate form, defined outside of any function:
    # use 'this' as a pointer to the module object instance itself. 'this' is an arbitrary name.
    #     this = sys.modules[__name__]
    #
    # can explicitly make assignments on it
    #     this.my_var = "default"
    #
    # ...whether 'this' or 'global', these could be module vars:
    #     'indicator', 'separator', 'top2', 'text_main'

    global main_list_fr
    global top2

    source_wid_list = main_list_fr.winfo_children()

    # module variables
    # indicator = "--"
    # separator = ": "
    raw_list = get_list(source_wid_list)

    if len(raw_list) == 1 and raw_list[0].text == '':
        # no input
        return

    # get the Text widget in the first Frame widget
    text_main = top2.winfo_children()[0].winfo_children()[0]
    # alt method:
    # frames = [w for w in top2.winfo_children() if w.__class__ == ttk.LabelFrame]
    frames = [w for w in top2.winfo_children() if w.__class__ == ttk.Frame]


    # print(f'    {frames=}')
    textw = [w for w in frames[0].winfo_children() if w.__class__ == tk.Text]
    # print(f'    {textw=}')

    text_main.delete('1.0', 'end')

    write_text(raw_list, indicator, separator, text_main)


# def write_text(raw_list, indicator, separator, text_main):
def write_text(the_list: list,
               indicator: str,
               separator: str,
               text_main: 'tk.Text'):
    linenum = 1
    # print(f'{type(text_main)=}')
    # print(f'{text_main.__class__=}')
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


def sort_by_category() -> None:
    """Sort a list of text lines.

    Lines are of the format 'linenumber-category: text'
    Text is user-entered contents of an Entry
    """
    # See note above on 'global'.
    # This one could also be passed in via a lambda callback.
    global main_list_fr

    # After the first line, remove category text
    trim_cat = True

    source_wid_list = main_list_fr.winfo_children()
    raw_list = get_list(source_wid_list)
    if len(raw_list) == 1 and raw_list[0].text == '':
        # no input
        return
    # print(f'{len(raw_list)=}')

    # raw_sort = sorted(raw_list, key=lambda item: item.category)
    sorted_list = []
    categories_sorted = sorted(categories)
    for c in categories_sorted:
        items = [i for i in raw_list if i.category == c]
        # TODO: exit enum if no items for this category
        print(f'items in category {c}: {len(items)}')
        if len(items) == 0:
            continue
        sorted_list.append(items[0])
        print(f'{items[0]}')
        for n, line in enumerate(items[1:]):
            if trim_cat:
                line.category = ' ' * len(line.category)
                print(f'    {line.category=}, {line.text=}')
            sorted_list.append(line)

    text_main = top2.winfo_children()[0].winfo_children()[0]
    text_main.delete('1.0', 'end')

    write_text(sorted_list, indicator, separator, text_main)


def option2():
    source_wid_list = main_list_fr.winfo_children()
    raw_list = get_list(source_wid_list)

    sorted_list = []
    categories_sorted = sorted(categories)
    for c in categories_sorted:
        items = [i for i in raw_list if i.category == c]
        items_sorted = sorted(items, key=lambda item: item.text)
        for n, line in enumerate(items_sorted):
            # print(f'    {line.category}, {line.text}')
            sorted_list.append(line)

    text_main = top2.winfo_children()[0].winfo_children()[0]
    text_main.delete('1.0', 'end')

    write_text(sorted_list, indicator, separator, text_main)


def set_window_offset(reference):
    """Calculate window position, as offset from a reference window."""
    top2_width = reference[0]
    top2_height = reference[1].split('+')[0]
    h_offset = reference[1].split('+')[1]
    v_offset = reference[1].split('+')[2]      # not currently used

    top2_h_offset = str(int(top2_width) + int(h_offset) + 40)
    top2_v_offset = top2_height

    return "+" + top2_h_offset + "+" + top2_v_offset


# Module scope objects
# ====================
root = ThemedTk()
# root.title('list manager')
root.title('Create List')

sttk.create_styles()

cnf1 = {'padx':5, 'pady':5}
cnf2 = {'anchor': 'w', 'padx': 15}

# for how this flag might be used, see the project pandas_data_RF
use_pandas = False

# example type
# def point_init(thispoint, xval: int, yval: int):
#     thispoint.xval = xval
#     thispoint.yval = yval
#
# Point = type('Point', (), {"__init__": point_init})

def lineitem_init(i, cat: str, item: str):
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

# main_lab = ttk.Label(root, foreground='blue', border=2, text='Create List')
# main_lab.pack(anchor='w', padx=5)

# needed?
# main_lab = ttk.Label(root, text="Create List", style="LabelFrameText.TLabel")

# main_fr_label = ttk.LabelFrame(root, labelwidget=main_lab)
main_fr_label = ttk.Frame(root)#, name="entry_frame")


# main_fr_label.pack(padx=5, pady=5)
main_fr_label.pack(cnf1)

# ? do we need this
# category_label = ttk.Label(root, background='#ff0', text='category')
category_label = ttk.Label(main_fr_label, background='#ff0', text='category')
# category_label.pack(anchor='w', padx=15)
category_label.pack(cnf=cnf2)

# main_list_fr = ttk.Frame(root, border=2)
main_list_fr = ttk.Frame(main_fr_label, border=2)
main_list_fr.pack(padx=10, ipadx=5, ipady=5)

# Set class attribute (for all row (MultiSelectFrame) objects):
setattr(msel.MultiSelectFrame, 'padding', 0)

rowframe = msel.MultiSelectFrame(main_list_fr,
                                 cb_values=categories,
                                 name='row1',
                                 posn=[0,0],
                                 )

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
# top2.title('list viewer')
top2.title('Format List')

win2_offset = set_window_offset(root_geometry)
top2.geometry(win2_offset)

# lab2 = ttk.Label(top2, text="Format List", style="LabelFrameText.TLabel")
# format_list_fr = ttk.LabelFrame(top2, labelwidget=lab2)#, name="format_frame")
format_list_fr = ttk.Frame(top2)#, name="format_frame")


# format_list_fr.pack(padx=5, pady=5)
format_list_fr.pack(cnf1)

options_fr = ttk.Frame(top2, relief='groove')
# options_fr.pack(padx=5, pady=5)
options_fr.pack(cnf1)

opt1_but = ttk.Button(options_fr, text="sort category", command=sort_by_category)
# opt1_but.pack(side='left', padx=5, pady=5)
opt1_but.pack(cnf1, side='left')

opt2_but = ttk.Button(options_fr, text="subsort", command=option2)
# opt2_but.pack(side='left', padx=5, pady=5)
opt2_but.pack(cnf1, side='left')

text_main = tk.Text(format_list_fr, width=40, height=10, background='#ffa')#, name="formatted_text")
# text_main.pack(padx=5, pady=5)
text_main.pack(cnf1)

# report function signatures. ----------
# import inspect

# print('move_text:')
# sig = (inspect.signature(move_text))
# print(f'   signature: {sig}')
# ---------- END report

if __name__ == "__main__":
    root.mainloop()
