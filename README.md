# list_manager_RF

PURPOSE
-------
This application is for interactive creation and formatting of small lists.
It is more formal than necessary for the purpose, but demonstrates python funcionality
such as communication between toplevel windows, and moving text from one
type of widget to another.


DEPENDENCIES
------------
ui_RF           - custom user interface elements
styles_ttk      - custom ttk widget styles
tkinter         - may need to install, on linux


OPERATION
---------
Two toplevel windows are created. In the first, list items are created in
a structured way, using Combobox and Entry widgets. Rows can be added or removed from
the interface (UI) as necessary.

Upon a button click, text is collected from the UI, consisting of:
    - item category, selected from a the Combobox
    - item text, entered by the user
Collected text is written to the output window, each UI row providing a line of output.
Lines are numbered, and within each line, category values are separated from text.

In the second window, there is a button for sorting lines by category.
