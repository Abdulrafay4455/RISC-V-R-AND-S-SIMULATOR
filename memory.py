# memory.py
# This file contains our simple memory model.
# We are using a Python dictionary instead of a real memory array
# because it is easy to understand for a student project.
# The key of the dictionary is the memory address (a number)
# and the value is the data stored at that address.

class Memory:
    def __init__(self):
        # empty dictionary to act as our memory
        self.mem = {}

        # we will fill some starting addresses with 0
        # just so the memory display does not look totally empty
        for addr in range(0, 64, 4):
            self.mem[addr] = 0

    # store a byte (used by sb instruction)
    def store_byte(self, address, value):
        # we only keep the lowest 8 bits, like real hardware would
        value = value & 0xFF
        self.mem[address] = value

    # store a half word, 2 bytes (used by sh instruction)
    def store_half(self, address, value):
        value = value & 0xFFFF
        self.mem[address] = value

    # store a full word, 4 bytes (used by sw instruction)
    def store_word(self, address, value):
        value = value & 0xFFFFFFFF
        self.mem[address] = value

    # this function reads memory value, if address not used yet, return 0
    def load(self, address):
        if address in self.mem:
            return self.mem[address]
        else:
            return 0

    # this function returns memory as a string so GUI can display it
    def get_memory_as_string(self):
        result = ""
        # sorting so the addresses show up in order
        for addr in sorted(self.mem.keys()):
            result = result + "Address " + str(addr) + " : " + str(self.mem[addr]) + "\n"
        return result
