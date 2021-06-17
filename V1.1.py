# built in modules
from tkinter import *
import tkinter.messagebox
import tkinter as tk
# third party modules
from pint import UnitRegistry  # necessary for unit conversion
import pyperclip  # handles the copy functions


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

significant_digits = 15  # this is the default rounding behavior of the program, allows up to 15 decimal places
insert_commas = 0  # determines whether commas are used as separators, 0 is false, 1 is true

# Defines the Frames
leftFrame = Frame(root, bg="#FAFAFA")
rightFrame = Frame(root, bg="#FAFAFA")
bottomFrame = Frame(root, bg="#FAFAFA")
veryBottomFrame = Frame(root, bg="#FAFAFA")

# places the frames
leftFrame.grid(row=0, column=0)
rightFrame.grid(row=0, column=1)
bottomFrame.grid(row=1, column=0, columnspan=2)
veryBottomFrame.grid(row=2, column=0, columnspan=2)

# Fills the left frame -- in order: label, Options Menus, Entry Box
# Label - left
label_left = Label(leftFrame, text="From:", bg="#FAFAFA")
label_left.grid(row=0, column=0, sticky=W, padx=10, pady=5)

# option menu - left
inputUnit = StringVar(leftFrame)
inputUnit.set(options_list[0])
unit_selector1 = OptionMenu(leftFrame, inputUnit, *options_list)
unit_selector1.grid(row=0, column=1, sticky=E, padx=10, pady=5)

# Entry Box - left
entry_box_1 = Entry(leftFrame, width=28, bg="white", highlightbackground="light blue")
entry_box_1.grid(row=1, column=0, padx=10, pady=10, sticky=W, columnspan=2)
entry_box_1.focus_set()  # sets the entry box as first focus in window

# Fills the RIGHT frame -- In order: Label, Options Menu, Entry Box
# Label - right
label_right = Label(rightFrame, text="To:", bg="#FAFAFA", fg="black")
label_right.grid(row=0, column=0, sticky=W, padx=10, pady=5, columnspan=2)

# Option Menu - right
outputUnit = StringVar(rightFrame)
outputUnit.set(options_list[0])
unit_selector2 = OptionMenu(rightFrame, outputUnit, *options_list)
unit_selector2.grid(row=0, column=1, sticky=E, padx=10, pady=5)

# Entry Box - right
entry_box_2 = Entry(rightFrame, width=30, bg="#FAFAFA", highlightbackground='#FAFAFA', fg='black')
entry_box_2.grid(row=1, column=0, padx=10, pady=10, sticky=W, columnspan=2)


# This is the main logic that occurs when CONVERT is pressed. It uses PINT to handle the conversions by creating a PINT
# unit registry object, which can then be converted to any unit that pint is capable of handling.
def generate_answer():
    ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
    try:
        user_num = float(entry_box_1.get())  # pulls the entry in the entry box, will not work if not a number
    except ValueError:
        entry_box_1.delete(0, END)  # deletes the users invalid entry
        tkinter.messagebox.showinfo(title="Try Again", message="You must input digits")  # alerts user of mistake
        entry_box_1.focus_set()  # sets the focus back on the entry box

    entry_box_2.delete(0, END)  # clears the results box in case there was a previous calculation

    input = inputUnit.get().lower()  # pulls input unit from first option menu and changes to lowercase
    output = outputUnit.get().lower()  # pulls output unit from second option menu and changes to lowercase

    measurement_to_convert = user_num * ureg(input)  # creates a unit registry object using the Class from Pint
    converted_measurement = f'{measurement_to_convert.to(output)}'  # converts the unit object to the output unit
    num_only = (converted_measurement.split()[0]) # this splits result from the unit, leaving just the number
    rounded = round(float(num_only), significant_digits) # rounds the number to amount defined by significant digits
    if float(rounded) == int(rounded):  # checks if it necessary for the num to be a float
        rounded = int(rounded)

    if insert_commas == 1:
        entry_box_2.insert(0, f'{rounded:,} {output}')  # displays the answer in the second entry box, includes a comma
    else:
        entry_box_2.insert(0, f'{rounded} {output}')


def copy_num_only_button():  # this function takes the result, splits off the unit and copies the number to clipboard
    result = f'{entry_box_2.get()}'
    result_list = result.split()
    pyperclip.copy(result_list[0])


def copy_button():  # this copies the unit and number from the result to the clipboard
    pyperclip.copy(entry_box_2.get())


# This section defines the 3 buttons -- Generate --- Copy Num -- Copy All
# Generate button
generate_button = Button(leftFrame, text="Convert",
                         font=15,
                         width=28,
                         command=generate_answer,
                         relief=FLAT,
                         activeforeground='white')
generate_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky=W)

# Copy number Button
copy_num_button = Button(rightFrame,
                         text="Copy Number Only",
                         command=copy_num_only_button,
                         width=15,
                         activeforeground='white')
copy_num_button.grid(row=2, column=1, padx=10, pady=10, sticky=E)

# copy results button
copy_button = Button(rightFrame,
                     text="Copy All",
                     width=12,
                     command=copy_button,
                     activeforeground='white')
copy_button.grid(row=2, column=0, padx=10, pady=10, sticky=W)

separator_label = Label(bottomFrame, text=str('-' * 94),
                        fg='#DADADA',
                        bg='#FAFAFA')
separator_label.grid(row=0, column=0)


def change_sig_digits(num):
    global significant_digits
    significant_digits = int(num)


scale = Scale(veryBottomFrame, variable=significant_digits, command=change_sig_digits,
              orient=HORIZONTAL,
              from_=0, to=20,
              sliderlength=20,
              activebackground='#0073FF',
              troughcolor="#FAFAFA",
              length=200,
              width=10)
scale.grid(row=0, column=1, padx=10, pady=10)
scale.set(significant_digits)

scale_label = Label(veryBottomFrame, text="Number of decimals to round:", width=35, bg='#FAFAFA')
scale_label.grid(row=0, column=0, pady=7)


# this functions changes the options presented in the unit selections
def set_to(dimension):
    new_options_list = options_dict.get(dimension)
    unit_selector1['menu'].delete(0, END)
    unit_selector2['menu'].delete(0, END)

    inputUnit.set(new_options_list[0])
    outputUnit.set(new_options_list[0])

    for option in new_options_list:
        unit_selector1['menu'].add_command(label=option, command=tk._setit(inputUnit, option))

    for option in new_options_list:
        unit_selector2['menu'].add_command(label=option, command=tk._setit(outputUnit, option))


def commas():  # this function 'toggles' the insert_commas variable, dependent on the checkbox getting clicked
    global insert_commas
    if insert_commas == 1:
        insert_commas = 0
    elif insert_commas == 0:
        insert_commas = 1


comma_checkbox = Checkbutton(veryBottomFrame, text="Include commas as separators",
                             relief=FLAT,
                             bg='#FAFAFA',
                             command=commas)
comma_checkbox.grid(row=1, column=0, pady=10)


# this section creates the menu options
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

root.config(menu=menubar)  # sets the menubars above to be the menu for the window

root.mainloop()  # mainloop that runs until window is closed
