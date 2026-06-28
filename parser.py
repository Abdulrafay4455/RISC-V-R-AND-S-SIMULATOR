# parser.py
# This file is responsible for reading the instructions.txt file
# and converting each line into a simple format our CPU can understand.

# We are keeping it very simple.
# Each line in instructions.txt looks like this:
#   add x1 x2 x3        -> R type
#   sw x5 0 x6          -> S type (store x5 into address [x6 + 0])
#
# We split the line by spaces and figure out what to do based on
# the first word (the operation name).

def parse_instructions(filename):
    instruction_list = []

    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        line = line.strip()  # remove extra spaces and newline

        # skip empty lines and comment lines (lines starting with #)
        if line == "" or line.startswith("#"):
            continue

        instr = parse_single_line(line)
        instruction_list.append(instr)

    return instruction_list


# this function turns ONE line of text into an instruction dictionary.
# we made this separate function so the GUI can use it too, when the
# user types an instruction directly into the GUI instead of using
# the instructions.txt file.
def parse_single_line(line):
    line = line.strip()
    parts = line.split()
    # parts[0] is the operation, like "add" or "sw"

    instr = {
        "raw": line,
        "op": parts[0],
        "args": parts[1:]
    }
    return instr


# small helper function to turn "x5" into just the number 5
def reg_number(reg_text):
    # remove the letter x in front of the number
    reg_text = reg_text.replace("x", "")
    return int(reg_text)