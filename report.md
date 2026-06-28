# RISC-V R-Type and S-Type Instruction Simulator with Simple GUI

### Computer Architecture (CA) Semester Project

---

## 1. Abstract

This project is a small simulator for some basic RISC-V instructions,
made using Python. It implements the most common R-Type instructions
(add, sub, and, or, xor, sll, srl, slt) and S-Type instructions
(sb, sh, sw). The simulator reads instructions from a text file, runs
them one at a time, and shows the updated registers and memory in a
simple Tkinter GUI. The goal of this project is to understand how a
CPU executes basic instructions and how registers and memory change as
a result, not to build a fully working processor emulator.

## 2. Introduction

RISC-V is an open instruction set architecture (ISA) that is used a
lot in computer architecture courses because it is simple compared to
ISAs like x86. In our CA course we learned about instruction formats
like R-Type and S-Type, and how the CPU uses registers and memory to
do its work. For this semester project, we decided to build a small
simulator in Python that can read a list of RISC-V instructions and
actually execute them, showing the results in a simple graphical
window instead of just printing to the terminal.

## 3. Objectives

The main objectives of this project are:

- To understand the structure of R-Type and S-Type RISC-V instructions.
- To practice implementing instruction execution logic in software.
- To learn how registers and memory work together during execution.
- To build a basic, working GUI using Tkinter.
- To get hands-on experience connecting instruction parsing, CPU
  logic, and a user interface together in one project.

## 4. Problem Statement

Understanding how a CPU executes instructions can be hard just from
reading textbook diagrams. Students can benefit from a small, visual
tool that lets them type in instructions and immediately see what
happens to the registers and memory. This project tries to solve that
by giving a simple simulator where a student can load a list of
instructions and watch them execute step by step, with the final
register and memory state displayed clearly.

## 5. Theory of RISC-V

RISC-V is a Reduced Instruction Set Computer (RISC) architecture. This
means most of its instructions are simple and take roughly the same
amount of time to execute, unlike CISC architectures (like x86) which
have many complex instructions. RISC-V has 32 general purpose
registers, named x0 to x31, each one being 32 bits wide in the basic
RV32I version. Register x0 is special — it is hardwired to always be
zero, no matter what is written to it.

Instructions in RISC-V are grouped into different "types" based on
their format, such as R-Type, I-Type, S-Type, B-Type, U-Type, and
J-Type. Each type tells the CPU how to read the fields of the
instruction (which bits are the opcode, which are the registers, and
so on). In this project we focus only on R-Type and S-Type since those
were the two types assigned for our semester project.

## 6. R-Type Instructions

R-Type instructions are "register type" instructions. They take two
source registers (rs1 and rs2) and a destination register (rd), and
do not use any memory or immediate values. The general form is:

```
op  rd, rs1, rs2
```

The R-Type instructions implemented in this project are:

| Instruction | Meaning                          |
|-------------|-----------------------------------|
| add         | rd = rs1 + rs2                    |
| sub         | rd = rs1 - rs2                    |
| and         | rd = rs1 AND rs2 (bitwise)        |
| or          | rd = rs1 OR rs2 (bitwise)         |
| xor         | rd = rs1 XOR rs2 (bitwise)        |
| sll         | rd = rs1 shifted left by rs2      |
| srl         | rd = rs1 shifted right by rs2     |
| slt         | rd = 1 if rs1 < rs2, else 0       |

## 7. S-Type Instructions

S-Type instructions are "store type" instructions. They are used to
write a value from a register into memory. The general form is:

```
op  rs2, offset(rs1)
```

This means: take the value in rs2 and store it at the memory address
calculated as rs1 + offset. The S-Type instructions implemented in
this project are:

| Instruction | Meaning                              |
|-------------|---------------------------------------|
| sb          | store the lowest 8 bits of rs2 to memory  |
| sh          | store the lowest 16 bits of rs2 to memory |
| sw          | store the full 32 bits of rs2 to memory   |

In our simulator, instead of using real binary encoding, we simply
read the instruction text directly (for example `sw x5 0 x6`) and
calculate the address as `register[x6] + 0`, then store the value of
`x5` at that address inside our memory dictionary.

## 8. Methodology

We split the project into small, separate Python files so that each
part has one clear job:

1. **parser.py** reads instructions.txt line by line and turns each
   line into a small dictionary containing the operation name and its
   arguments.
2. **memory.py** holds a Python dictionary that acts as our memory.
   Addresses are the dictionary keys and stored values are the
   dictionary values.
3. **cpu.py** has the CPU class with 32 registers and a function
   called `execute()` that looks at the operation name and performs
   the right calculation, updating either a register or memory.
4. **gui.py** builds the Tkinter window, connects the buttons to the
   above logic, and displays the results in text boxes.
5. **main.py** simply creates the window and starts the GUI.

We tested the project by running it with the sample instructions in
instructions.txt and checking that the register and memory values
matched what we calculated by hand.

## 9. Algorithm

```
1. Start the program (main.py creates the GUI window)
2. User clicks "Load Instructions"
   a. Read instructions.txt
   b. Skip blank lines and comment lines
   c. Split each line into operation + arguments
   d. Store all instructions in a list
   e. Show the instructions in the instruction box
3. User clicks "Run Simulation"
   a. Create fresh registers (all 0 except a few preset test values)
   b. Create fresh memory
   c. For each instruction in the list:
        - Look at the operation name
        - If it is an R-Type op, read rs1 and rs2 from registers,
          calculate the result, and write it to rd
        - If it is an S-Type op, calculate the address from
          rs1 + offset, and store the value of rs2 at that address
        - If something goes wrong, log "Error in Instruction"
   d. Show updated registers in the register box
   e. Show updated memory in the memory box
   f. Update the status label (Simulation Complete / Error)
4. End
```

## 10. ASCII Flowchart

```
            +-------------------------+
            |      Start Program      |
            +-------------------------+
                       |
                       v
            +-------------------------+
            |  Click "Load            |
            |  Instructions" button   |
            +-------------------------+
                       |
                       v
            +-------------------------+
            | Read instructions.txt   |
            | Parse each line         |
            +-------------------------+
                       |
                       v
            +-------------------------+
            | Show instructions in    |
            | GUI text box            |
            +-------------------------+
                       |
                       v
            +-------------------------+
            |  Click "Run Simulation" |
            +-------------------------+
                       |
                       v
            +-------------------------+
            | For each instruction:   |
            |   - R-Type? do math,    |
            |     update register     |
            |   - S-Type? calculate   |
            |     address, update     |
            |     memory              |
            +-------------------------+
                       |
                       v
            +-------------------------+
            | Show registers & memory |
            | Update status label     |
            +-------------------------+
                       |
                       v
                  +---------+
                  |   End   |
                  +---------+
```

## 11. Screenshots Section (Placeholder)

*(Insert screenshots of the running application here before final
submission. Recommended screenshots:)*

1. Screenshot of the GUI right after opening the program.
2. Screenshot after clicking "Load Instructions" (showing the
   instruction list).
3. Screenshot after clicking "Run Simulation" (showing updated
   registers and memory).

```
[ Screenshot 1 - Initial Window ]



[ Screenshot 2 - After Loading Instructions ]



[ Screenshot 3 - After Running Simulation ]


```

## 12. Testing

We tested the simulator manually using the sample instructions.txt
file included in this project. Some of the test cases:

| Test Case                         | Expected Result                  | Result   |
|-----------------------------------|-----------------------------------|----------|
| add x8 x1 x2 (x1=10, x2=20)        | x8 = 30                           | Passed   |
| sub x9 x2 x1 (x2=20, x1=10)        | x9 = 10                           | Passed   |
| sll x13 x3 x4 (x3=5, x4=2)         | x13 = 20                          | Passed   |
| slt x15 x1 x2 (10 < 20)            | x15 = 1                           | Passed   |
| sw x5 0 x6 (x5=100, x6=0)          | mem[0] = 100                      | Passed   |
| writing to x0                      | x0 stays 0                        | Passed   |
| unknown instruction in file        | shows "Error in Instruction"      | Passed   |

We also tested that x0 always stays 0 even if an instruction tries to
write to it, since this is a special rule in real RISC-V hardware.

## 13. Results

The simulator successfully executes all the R-Type and S-Type
instructions listed in the requirements. After clicking "Run
Simulation", the register box correctly shows updated values for all
32 registers, and the memory box correctly shows the addresses that
were written to by the sb, sh, and sw instructions. The status label
correctly updates to show "Simulation Complete" when everything runs
fine, and shows an error message if an instruction is invalid or
written incorrectly in instructions.txt.

## 14. Conclusion

This project helped us understand RISC-V R-Type and S-Type
instructions in a much more practical way compared to only studying
them from slides. By actually writing the Python logic for each
instruction, we got a clearer picture of how registers and memory
interact during execution, and how a CPU's instruction cycle (read,
decode, execute) can be represented in code, even in a simplified
form. Building the small Tkinter GUI also gave us experience
connecting backend logic to a user interface.

## 15. Future Scope

This simulator only covers a small part of the RISC-V instruction set.
In the future, this project could be extended to support:

- I-Type instructions (like addi, lw)
- B-Type and J-Type instructions (branches and jumps)
- A proper program counter (PC) to support actual program flow
- Loading instructions directly from compiled RISC-V binaries
- A nicer GUI with instruction highlighting during execution

## 16. References

1. RISC-V Foundation, "The RISC-V Instruction Set Manual."
2. Course lecture slides and lab material from Computer Architecture
   (CA) course.
3. Python official documentation - https://docs.python.org/3/
4. Python Tkinter documentation - https://docs.python.org/3/library/tkinter.html
