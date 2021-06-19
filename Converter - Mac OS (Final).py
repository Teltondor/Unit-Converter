# built in modules
from tkinter import *
import tkinter as tk
# third party modules
from pint import UnitRegistry  # necessary for unit conversion
import pyperclip  # handles the copy functions


# This is the main logic that occurs when CONVERT is pressed. It uses PINT to handle the conversions by creating a PINT
# unit registry object, which can then be converted to any unit that pint is capable of handling.
def generate_answer():
    ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
    try:
        user_num = float(input_entry_box.get())  # pulls the entry in the entry box, will not work if not a number
    except ValueError:
        input_entry_box.delete(0, END)  # deletes the users invalid entry
        input_entry_box.focus_set()  # sets the focus back on the entry box

    output_box.delete(0, END)  # clears the results box in case there was a previous calculation

    input = inputUnit.get().lower()  # pulls input unit from first option menu and changes to lowercase
    output = outputUnit.get().lower()  # pulls output unit from second option menu and changes to lowercase

    measurement_to_convert = user_num * ureg(input)  # creates a unit registry object using the Class from Pint
    converted_measurement_obj = measurement_to_convert.to(output)  # converts the unit object to the output unit
    short_unit = f'{converted_measurement_obj:~}'.split()[1]  # isolates the abbreviated output unit as a string
    converted_measurement = f'{measurement_to_convert.to(output)}'  # creates a string variation of the unit object
    long_unit = converted_measurement.split()[1]  # isolates the long output unit as a string
    num_only = (converted_measurement.split()[0])  # this splits result from the unit, leaving just the number
    rounded = round(float(num_only), significant_digits) # rounds the number to amount defined by significant digits
    if float(rounded) == int(rounded):  # checks if it necessary for the num to be a float
        rounded = int(rounded)
    if insert_commas == 1:
        if full_unit_names == 1:
            output_box.insert(0, f'{rounded:,} {long_unit}')
        elif full_unit_names == 0:
            output_box.insert(0, f'{rounded:,} {short_unit}')
    elif insert_commas == 0:
        if full_unit_names == 1:
            output_box.insert(0, f'{rounded} {long_unit}')
        elif full_unit_names == 0:
            output_box.insert(0, f'{rounded} {short_unit}')

def switch_units():
    old_input = inputUnit.get()
    old_output = outputUnit.get()
    inputUnit.set(old_output)
    outputUnit.set(old_input)

def copy_num_only_button():  # this function takes the result, splits off the unit and copies the number to clipboard
    result = f'{output_box.get()}'
    result_list = result.split()
    pyperclip.copy(result_list[0])

def copy_button():  # this copies the unit and number from the result to the clipboard
    pyperclip.copy(output_box.get())

def change_sig_digits(num):
    global significant_digits
    significant_digits = int(num)
    generate_answer()

def commas():  # this function 'toggles' the insert_commas variable, dependent on the checkbox getting clicked
    global insert_commas
    if insert_commas == 1:
        insert_commas = 0
    elif insert_commas == 0:
        insert_commas = 1
    generate_answer()

def abbreviated_units():  # this toggles whether or not to use abbreviated units
    global full_unit_names
    if full_unit_names == 1:
        full_unit_names = 0
    elif full_unit_names == 0:
        full_unit_names = 1
    generate_answer()

def set_to(dimension):  # this functions changes the options presented in the unit selections
    new_options_list = options_dict.get(dimension)
    unit_selector1['menu'].delete(0, END)
    unit_selector2['menu'].delete(0, END)

    inputUnit.set(new_options_list[0])
    outputUnit.set(new_options_list[0])

    for option in new_options_list:
        unit_selector1['menu'].add_command(label=option, command=tk._setit(inputUnit, option))

    for option in new_options_list:
        unit_selector2['menu'].add_command(label=option, command=tk._setit(outputUnit, option))


# options_dict are the input units and output units that will be presented to user. You can add and remove units, and
# the code will account for it. Note that you must add units as the full word and singular (case does not
# matter). List can also be re-ordered. Since Pint handles the conversion, the unit must be one that Pint supports.
# The default conversion is length, but the other options will be used if the user wants to do those conversions
# For pint conversion options visit: https://github.com/hgrecco/pint/blob/master/pint/default_en.txt
options_dict = {'length':
                    ["Nanometer", "Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot", "Yard", "Mile",
                     "League", "Fathom", "Furlong", "Rod", "Lightyear"],
                'volume':
                    ["Teaspoon", "Tablespoon", "Cup", "Pint", "Quart", "Gallon", "Liter", "Milliliter"],
                'weight':
                    ["Pound", "Kilogram", "Gram", "Ounce", "Ton", "Carat"],
                'time':
                    ["Second", "Minute", "Hour", "Day", "Week", "Month", "Year", "Century", "Millennium", "Eon"],
                'storage':
                    ["Bit", "Megabit", "Gigabit", "Kilobit", "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte", "Petabyte"],
                'speed':
                    ["MPH", "KPH", "Knot", "Meter per second", "Feet per second"],
                'temperature':
                    ["Celsius", "Kelvin", "Fahrenheit", "Rankine"]}
options_list = options_dict.get('length')


root = Tk()
root.title("Unit Converter")
root.geometry("+200+200")  # positions window 200 pixels down and to the right from the upper left corner
root.resizable(False, False)  # prevents window resizing
root.wait_visibility(root)

significant_digits = 15  # this is the default rounding behavior of the program, allows up to 15 decimal places
insert_commas = 0  # determines whether commas are used as separators, 0 is false, 1 is true
full_unit_names = 1  # determines default whether full unit names will be displayed (1), or abbreviations (0)

# Defines the Frames #####################################################################################
leftFrame = Frame(root, bg="white")
rightFrame = Frame(root, bg="white")
middleFrame = Frame(root, bg="white")
bottomLeftFrame = Frame(root, bg="white")
bottomRightFrame = Frame(root, bg="white")

# places the frames
leftFrame.grid(row=0, column=0)
rightFrame.grid(row=0, column=1)
middleFrame.grid(row=1, column=0, columnspan=2)
bottomLeftFrame.grid(row=2, column=0, sticky=W)
bottomRightFrame.grid(row=2, column=1, sticky=E)

# Top - Left - Frame ###############################################################################################

# Label - LEFT
label_left = Label(leftFrame, text="From:", bg="white", fg='black')

# option menu - LEFT
inputUnit = StringVar(leftFrame)
inputUnit.set(options_list[0])
unit_selector1 = OptionMenu(leftFrame, inputUnit, *options_list)
unit_selector1.configure(relief=FLAT,
                         bg='white',
                         fg='black',
                         activebackground="ghostwhite",
                         activeforeground='black',
                         highlightbackground='cadetblue')

# Entry Box - LEFT
input_entry_box = Entry(leftFrame, width=34, bg="white", highlightbackground="light blue")
input_entry_box.focus_set()  # sets the entry box as first focus in window

# Generate button- LEFT
generate_button = Button(leftFrame, text="Convert",
                         width=35,
                         command=generate_answer,
                         relief=FLAT,
                         bg="whitesmoke",
                         activebackground='dodger blue',
                         activeforeground='white')

label_left.grid(row=0, column=0, padx=10, pady=10, sticky=W)
unit_selector1.grid(row=0, column=1, padx=10, pady=10, sticky=E)
input_entry_box.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=W)
generate_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky=W)

# Top - right - Frame ################################################################################################

# Option Menu - right
outputUnit = StringVar(rightFrame)
outputUnit.set(options_list[0])
unit_selector2 = OptionMenu(rightFrame, outputUnit, *options_list)
unit_selector2.configure(relief=FLAT,
                         bg='white',
                         fg='black',
                         activebackground="ghostwhite",
                         activeforeground='black',
                         highlightbackground='cadetblue')

# Entry Box - right
output_box = Entry(rightFrame,
                   width=37,
                   bg="white",
                   highlightbackground='white',
                   fg='black',
                   relief=FLAT)

# swap button _ RIGHT
swap_units = Button(rightFrame, text="Swap Units",
                    relief=FLAT,
                    bg="whitesmoke",
                    activebackground='dodger blue',
                    activeforeground='white',
                    command=switch_units)

# Copy number Button - RIGHT
copy_num_button = Button(rightFrame,
                         text="Copy Number Only",
                         command=copy_num_only_button,
                         width=15,
                         relief=FLAT,
                         bg="whitesmoke",
                         activebackground='dodger blue',
                         activeforeground='white')

# copy results button - RIGHT
copy_button = Button(rightFrame,
                     text="Copy All",
                     width=12,
                     command=copy_button,
                     relief=FLAT,
                     bg="whitesmoke",
                     activebackground='dodger blue',
                     activeforeground='white')

unit_selector2.grid(row=0, column=1, padx=10, pady=10, sticky=E)
output_box.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=W)
swap_units.grid(row=0, column=0, padx=10, pady=10, sticky=W)
copy_num_button.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky=E)
copy_button.grid(row=2, column=0, padx=10, pady=10, sticky=W)

# Separator Label == Middle Frame ###############################################################################
separator_label = Label(middleFrame, text=str('-' * 260),
                        fg='light gray',
                        bg='white',
                        font=('arial', 8))
separator_label.grid(row=0, column=0)

# Bottom - Right - Frame  #####################################################################################
scale = Scale(bottomRightFrame, variable=significant_digits, command=change_sig_digits,
              orient=HORIZONTAL,
              from_=1, to=20,
              sliderlength=20,
              activebackground='#0073FF',
              troughcolor="white",
              length=200,
              width=6,
              bg='white',
              highlightbackground='white')
scale.set(significant_digits)
scale_label = Label(bottomRightFrame, text="Number of decimal places to round",
                    width=35,
                    bg='white',
                    activebackground='white')

scale_label.grid(row=1, column=0, padx=10, pady=5)
scale.grid(row=0, column=0, padx=10, pady=0,)

# Bottom - Left - Frame ############################################################################################
comma_checkbox = Checkbutton(bottomLeftFrame, text="Include commas as separators",
                             relief=FLAT,
                             bg='white',
                             command=commas)
full_names_checkbox = Checkbutton(bottomLeftFrame, text="Use abbreviated units in result",
                                  relief=FLAT,
                                  bg='white',
                                  command=abbreviated_units)

full_names_checkbox.grid(row=1, column=0, padx=10, pady=10, sticky=W)
comma_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky=W)


# this section creates the menu options ############################################################################
menubar = Menu(root)  # creates menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Length Converter", command=lambda: set_to('length'))
filemenu.add_command(label="Volume Converter", command=lambda: set_to('volume'))
filemenu.add_command(label="Weight Converter", command=lambda: set_to('weight'))
filemenu.add_command(label="Time Converter", command=lambda: set_to('time'))
filemenu.add_command(label="Storage Converter", command=lambda: set_to('storage'))
filemenu.add_command(label="Speed Converter", command=lambda: set_to('speed'))
filemenu.add_command(label="Temperature Converter", command=lambda: set_to('temperature'))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="All Conversions", menu=filemenu)


root.config(menu=menubar)  # sets the menu bars above to be the menu for the window

root.mainloop()  # mainloop that runs until window is closed
