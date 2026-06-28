# gui.py
# This file makes the simple Tkinter window for our project.
# It has buttons to load instructions and run the simulation,
# and text boxes to show instructions, registers, and memory.

import tkinter as tk
from tkinter import scrolledtext

from parser import parse_instructions, parse_single_line
from cpu import CPU
from memory import Memory


class SimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RISC-V R-Type and S-Type Instruction Simulator")
        self.root.geometry("700x600")

        # this list will hold the parsed instructions after loading
        self.instructions = []

        # this separate list only keeps instructions that the user
        # typed manually in the GUI (so we can show them separately
        # from the ones loaded from instructions.txt)
        self.manual_instructions = []

        # creating our memory and cpu objects
        self.memory = Memory()
        self.cpu = CPU(self.memory)

        # ---------- Title Label ----------
        title_label = tk.Label(
            root,
            text="RISC-V R-Type and S-Type Instruction Simulator",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        # ---------- Buttons Frame ----------
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        self.load_button = tk.Button(
            button_frame, text="Load Instructions", width=18, command=self.load_instructions
        )
        self.load_button.grid(row=0, column=0, padx=10)

        self.run_button = tk.Button(
            button_frame, text="Run Simulation", width=18, command=self.run_simulation
        )
        self.run_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(
            button_frame, text="Reset", width=18, command=self.reset_simulator
        )
        self.reset_button.grid(row=0, column=2, padx=10)

        # ---------- Status Label ----------
        self.status_label = tk.Label(root, text="Status: Waiting...", fg="blue")
        self.status_label.pack(pady=5)

        # ---------- Type Your Own Instruction Frame ----------
        # this lets the user type an instruction directly in the GUI
        # instead of having to edit instructions.txt every time.
        type_frame = tk.Frame(root)
        type_frame.pack(pady=5)

        type_label = tk.Label(type_frame, text="Type an instruction:")
        type_label.grid(row=0, column=0, padx=5)

        self.instr_entry = tk.Entry(type_frame, width=30)
        self.instr_entry.grid(row=0, column=1, padx=5)
        # so the user can also just press Enter instead of clicking the button
        self.instr_entry.bind("<Return>", lambda event: self.add_instruction())

        self.add_button = tk.Button(
            type_frame, text="Add Instruction", width=14, command=self.add_instruction
        )
        self.add_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(
            type_frame, text="Clear Instructions", width=14, command=self.clear_instructions
        )
        self.clear_button.grid(row=0, column=3, padx=5)

        # ---------- Set Register Value Frame ----------
        # since this project only supports R-Type and S-Type
        # instructions, there is no "li" or "addi" instruction to
        # put a starting value into a register. So we add this small
        # section to let the user set a register's value manually
        # before running their own add/sub/etc instructions.
        reg_set_frame = tk.Frame(root)
        reg_set_frame.pack(pady=5)

        reg_set_label = tk.Label(reg_set_frame, text="Set Register:")
        reg_set_label.grid(row=0, column=0, padx=5)

        reg_name_label = tk.Label(reg_set_frame, text="x")
        reg_name_label.grid(row=0, column=1)

        self.reg_number_entry = tk.Entry(reg_set_frame, width=5)
        self.reg_number_entry.grid(row=0, column=2, padx=2)

        equals_label = tk.Label(reg_set_frame, text="=")
        equals_label.grid(row=0, column=3)

        self.reg_value_entry = tk.Entry(reg_set_frame, width=10)
        self.reg_value_entry.grid(row=0, column=4, padx=2)

        self.set_reg_button = tk.Button(
            reg_set_frame, text="Set Register", width=14, command=self.set_register_value
        )
        self.set_reg_button.grid(row=0, column=5, padx=10)

        # ---------- Manually Typed Instructions Box ----------
        # this box ONLY shows instructions that the user typed by hand
        # in the box above. It will NOT show instructions loaded from
        # instructions.txt, so the student can clearly see what they
        # entered manually versus what came from the file.
        manual_label = tk.Label(root, text="Manually Entered Instructions:")
        manual_label.pack()
        self.manual_box = scrolledtext.ScrolledText(root, height=5, width=80)
        self.manual_box.pack(pady=5)

        # ---------- Instruction Display Box ----------
        instr_label = tk.Label(root, text="Instructions:")
        instr_label.pack()
        self.instr_box = scrolledtext.ScrolledText(root, height=8, width=80)
        self.instr_box.pack(pady=5)

        # ---------- Register Display Box ----------
        reg_label = tk.Label(root, text="Registers:")
        reg_label.pack()
        self.reg_box = scrolledtext.ScrolledText(root, height=8, width=80)
        self.reg_box.pack(pady=5)

        # ---------- Memory Display Box ----------
        mem_label = tk.Label(root, text="Memory:")
        mem_label.pack()
        self.mem_box = scrolledtext.ScrolledText(root, height=8, width=80)
        self.mem_box.pack(pady=5)

        # showing the starting registers (all 0) and starting memory
        # right when the app opens, so the user can see registers
        # are already at 0 before they even click anything
        self.reg_box.insert(tk.END, self.cpu.get_registers_as_string())
        self.mem_box.insert(tk.END, self.memory.get_memory_as_string())

    # this function runs when "Set Register" button is clicked.
    # it lets the user manually put a value into a register, since
    # this project does not have an "li" or "addi" instruction.
    def set_register_value(self):
        reg_text = self.reg_number_entry.get().strip()
        val_text = self.reg_value_entry.get().strip()

        if reg_text == "" or val_text == "":
            self.status_label.config(text="Status: Please enter both register number and value", fg="red")
            return

        try:
            reg_num = int(reg_text)
            value = int(val_text)

            if reg_num < 0 or reg_num > 31:
                self.status_label.config(text="Status: Register number must be between 0 and 31", fg="red")
                return

            # using the cpu's own set_register function, so x0 stays
            # protected and always remains 0
            self.cpu.set_register(reg_num, value)

            # update the register box right away so the user can see it
            self.reg_box.delete("1.0", tk.END)
            self.reg_box.insert(tk.END, self.cpu.get_registers_as_string())

            # clear the entry boxes for next use
            self.reg_number_entry.delete(0, tk.END)
            self.reg_value_entry.delete(0, tk.END)

            self.status_label.config(text="Status: Register x" + str(reg_num) + " Set", fg="green")
        except Exception as e:
            self.status_label.config(text="Status: Error Setting Register (" + str(e) + ")", fg="red")

    # this function runs when "Add Instruction" is clicked (or Enter is pressed)
    # it takes whatever the user typed in the entry box and adds it to our
    # instruction list, instead of reading from instructions.txt
    def add_instruction(self):
        line = self.instr_entry.get()  # get text typed by the user
        line = line.strip()

        if line == "":
            # user did not type anything, do nothing
            return

        try:
            instr = parse_single_line(line)
            self.instructions.append(instr)

            # also keep track of it in our separate "manual" list
            self.manual_instructions.append(instr)

            # show the new instruction in the main instruction box
            self.instr_box.insert(tk.END, instr["raw"] + "\n")

            # also show it in the manual instructions box
            self.manual_box.insert(tk.END, instr["raw"] + "\n")

            # clear the entry box so it is ready for the next instruction
            self.instr_entry.delete(0, tk.END)

            self.status_label.config(text="Status: Instruction Added", fg="green")
        except Exception as e:
            self.status_label.config(text="Status: Error in Instruction (" + str(e) + ")", fg="red")

    # this function clears the instruction list, so the user can start fresh
    def clear_instructions(self):
        self.instructions = []
        self.manual_instructions = []
        self.instr_box.delete("1.0", tk.END)
        self.manual_box.delete("1.0", tk.END)
        self.status_label.config(text="Status: Instructions Cleared", fg="blue")

    # this function resets EVERYTHING back to the starting state.
    # it clears the instruction lists, empties the registers and
    # memory boxes, and makes a brand new cpu and memory object.
    def reset_simulator(self):
        # clear both instruction lists
        self.instructions = []
        self.manual_instructions = []

        # make a fresh memory and cpu, this puts all registers
        # back to their starting values (x0 = 0, etc.)
        self.memory = Memory()
        self.cpu = CPU(self.memory)

        # clear the entry box too, in case something was half typed
        self.instr_entry.delete(0, tk.END)
        self.reg_number_entry.delete(0, tk.END)
        self.reg_value_entry.delete(0, tk.END)

        # empty out the instruction boxes
        self.instr_box.delete("1.0", tk.END)
        self.manual_box.delete("1.0", tk.END)

        # show the fresh registers (all 0) and fresh memory right away,
        # instead of leaving these boxes blank
        self.reg_box.delete("1.0", tk.END)
        self.reg_box.insert(tk.END, self.cpu.get_registers_as_string())

        self.mem_box.delete("1.0", tk.END)
        self.mem_box.insert(tk.END, self.memory.get_memory_as_string())

        self.status_label.config(text="Status: Reset Done - Registers are 0", fg="blue")

    # this function runs when "Load Instructions" button is clicked
    def load_instructions(self):
        try:
            self.instructions = parse_instructions("instructions.txt")

            # clearing the instruction box and showing all loaded lines
            self.instr_box.delete("1.0", tk.END)
            for instr in self.instructions:
                self.instr_box.insert(tk.END, instr["raw"] + "\n")

            self.status_label.config(text="Status: Instructions Loaded", fg="green")
        except Exception as e:
            self.status_label.config(text="Status: Error in Instruction (" + str(e) + ")", fg="red")

    # this function runs when "Run Simulation" button is clicked
    def run_simulation(self):
        # if user did not load instructions yet, do not run
        if len(self.instructions) == 0:
            self.status_label.config(text="Status: Please load instructions first", fg="red")
            return

        # NOTE: we do NOT make a fresh cpu/memory here anymore.
        # this is on purpose - so that any register values the user
        # set manually using "Set Register" are NOT wiped out.
        # we only clear the old execution log before running again.
        self.cpu.log = []

        error_happened = False

        for instr in self.instructions:
            success = self.cpu.execute(instr)
            if not success:
                error_happened = True

        # showing the execution log in the instruction box
        self.instr_box.delete("1.0", tk.END)
        for line in self.cpu.log:
            self.instr_box.insert(tk.END, line + "\n")

        # showing register values
        self.reg_box.delete("1.0", tk.END)
        self.reg_box.insert(tk.END, self.cpu.get_registers_as_string())

        # showing memory values
        self.mem_box.delete("1.0", tk.END)
        self.mem_box.insert(tk.END, self.memory.get_memory_as_string())

        if error_happened:
            self.status_label.config(text="Status: Error in Instruction", fg="red")
        else:
            self.status_label.config(text="Status: Simulation Complete", fg="green")