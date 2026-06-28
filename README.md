# RISC-V R-Type and S-Type Instruction Simulator

This is a small Computer Architecture (CA) semester project made in Python.
It simulates a tiny part of a RISC-V CPU. It can run R-Type instructions
(add, sub, and, or, xor, sll, srl, slt) and S-Type instructions
(sb, sh, sw). It has a simple GUI made using Tkinter.

## Project Files

- main.py – starts the GUI application
- gui.py – contains the Tkinter window and button logic
- cpu.py – contains the 32 registers and instruction execution code
- parser.py – reads and parses instructions.txt
- memory.py – simple memory model using a Python dictionary
- instructions.txt – sample instructions used by the simulator
- report.md – full project report

## Requirements

- Python 3.x (Tkinter comes built-in with most Python installations)
- No extra libraries need to be installed. Everything used is from the
  Python standard library.

## How to Run

1. Make sure all the files (main.py, gui.py, cpu.py, parser.py,
   memory.py, instructions.txt) are in the same folder.
2. Open a terminal / command prompt in that folder.
3. Run the following command:

```
python main.py
```

(On some systems you may need to type `python3 main.py` instead.)

4. The simulator window will open.
5. Click the **Load Instructions** button. This will read
   instructions.txt and show the instructions in the box.
6. Click the **Run Simulation** button. This will execute every
   instruction one by one and show the updated register values and
   memory contents.
7. The status label at the top will tell you if everything worked,
   for example "Simulation Complete", or if something went wrong,
   for example "Error in Instruction".
8. Click **Reset** any time to clear everything — instructions,
   registers, and memory all go back to their starting state.

## Manually Entered Instructions Box

When you type an instruction directly into the "Type an instruction:"
box and click **Add Instruction**, it shows up in two places:

- The main **Instructions** box (along with anything loaded from
  instructions.txt)
- A separate **Manually Entered Instructions** box, which ONLY shows
  instructions you typed by hand, so you can clearly tell them apart
  from the ones loaded from the file.

## How To Add Your Own Instructions

There are two ways to add your own instructions:

**Option 1: Type directly in the GUI (easiest)**
1. Run the program (`python main.py`).
2. Type your instruction into the "Type an instruction:" box near the top
   (for example `add x9 x1 x2`).
3. Click **Add Instruction** (or just press Enter).
4. It will show up in the instructions box right away.
5. Repeat for as many instructions as you want.
6. Click **Run Simulation** when you are done.
7. Use the **Clear Instructions** button if you want to start over.

**Option 2: Edit instructions.txt**
Open instructions.txt in any text editor and add new lines using
this format:

```
add x1 x2 x3        (R-Type: rd rs1 rs2)
sw  x5 0  x6         (S-Type: rs2 offset rs1)
```

Then click **Load Instructions** in the GUI to load them (note: this
replaces any instructions you typed directly in the GUI).

Lines starting with `#` are treated as comments and are ignored.

## Notes

- Register x0 is hardwired to 0, just like in real RISC-V, so writing
  to it does nothing.
- ALL registers (x0 to x31) start at 0 when you open the app or click
  Reset. This project does not implement instructions like `li` or
  `addi`, so there is no built-in way to load a starting value into a
  register using an instruction.
- If you want your `add`, `sub`, etc. instructions to produce
  meaningful (non-zero) results, use the **Set Register** box in the
  GUI first. For example, type `1` in the register box and `15` in
  the value box, click **Set Register**, and `x1` becomes `15`.
  Do this for any registers you want before clicking Run Simulation.
- Clicking **Run Simulation** does NOT reset your registers — it runs
  on top of whatever values are currently there, so your "Set
  Register" values stay in place. Use **Reset** if you want to clear
  everything (registers, memory, instructions) and start from 0 again.