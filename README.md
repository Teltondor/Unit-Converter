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
2. Add a new function modeled after set_to_volume (line 167). You can copy and paste the whole function (renaming it of course), the only line you need to modify 
   is the first line in the function. Modify the options_dict.get to point to whichever key you added into the dictionary.
3. Go to line 241 and add a new menu option in whichever order you desire. Label it whatever you need, and point the command to the function you just created.

Built-In Settings
The program allows you to select the number of decimal places you wish to round. This is done via pythons defualt 'round' (line 98)
This could be changed to some other method of rounding if necessary
