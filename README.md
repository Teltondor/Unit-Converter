# Unit-Converter
Converts units (length, volume, time, weight, and storage)

### External Dependencies ###

Requires PINT https://pint.readthedocs.io/en/stable/index.html
Requires PYPERCLIP https://pypi.org/project/pyperclip/

############

Uses tkinter to create the GUI.


############

OPTIONS

Functionality can be modified by adding or removing units in the options_dict dictionary (line 16)
Any added units must be ones that PINT can handle, because PINT is responsible for the actual conversion process

If you want to add a dimension (i.e speed or mass) you must:
1. Update options_dict (line 16) with a new key for the dimension, and the units for that dimmension as a list of values for the key.
2. Go to line 188 and add a new menu option in whichever order you desire (using filemenu.add_command. Label it whatever you need, and pass the key for the dimension you just created in options_dict to the 'set_to' function.

Built-In Settings
The program allows you to select the number of decimal places you wish to round. This is done via pythons defualt 'round' (line 98)
This could be changed to some other method of rounding if necessary
