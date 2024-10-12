# list_manager_RF

This application is for interactive creation and formatting of small lists.
It is more formal than necessary for the purppose, but demonstrates communication between
toplevel windows, and moving textual information from one kind of widget to another.

There are no program dependencies except, on linux you may need to install tkinter.

Two toplevel windows are created. In the first, list items are created in
a structured way, using Combobox and Entry widgets. Rows can be added or removed from
the interface (UI) as necessary.
Spacers can be defined to separate rows in the formatted output.

Upon a button click, text is collected from the UI:
    - item category, selected from a the Combobox list
    - item text, entered by the user
Collected text is written to the output window, each UI row providing a line of output.
Lines are numbered, and within each line, category values are separated from text.