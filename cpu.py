# cpu.py
from parser import reg_number

class CPU:
    def __init__(self, memory):
        self.registers = [0] * 32
        self.memory = memory
        self.log = []

    def set_register(self, reg_num, value):
        if reg_num == 0:
            return
        self.registers[reg_num] = value & 0xFFFFFFFF

    def get_register(self, reg_num):
        return self.registers[reg_num]

    # -------- ALU --------
    def add(self, a, b):
        return (a + b) & 0xFFFFFFFF

    def sub(self, a, b):
        b_twos = (~b + 1) & 0xFFFFFFFF
        return (a + b_twos) & 0xFFFFFFFF

    def and_op(self, a, b):
        return a & b

    def or_op(self, a, b):
        return a | b

    def xor_op(self, a, b):
        return a ^ b

    def sll(self, value, shamt):
        return (value << shamt) & 0xFFFFFFFF

    def srl(self, value, shamt):
        return (value & 0xFFFFFFFF) >> shamt

    def slt(self, a, b):
        return 1 if a < b else 0

    def execute(self, instr):
        op = instr["op"]
        args = instr["args"]

        try:
            if op == "add":
                rd, rs1, rs2 = map(reg_number, args[:3])
                result = self.add(self.get_register(rs1), self.get_register(rs2))
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "sub":
                rd, rs1, rs2 = map(reg_number, args[:3])
                result = self.sub(self.get_register(rs1), self.get_register(rs2))
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "and":
                rd, rs1, rs2 = map(reg_number, args[:3])
                result = self.and_op(self.get_register(rs1), self.get_register(rs2))
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "or":
                rd, rs1, rs2 = map(reg_number, args[:3])
                result = self.or_op(self.get_register(rs1), self.get_register(rs2))
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "xor":
                rd, rs1, rs2 = map(reg_number, args[:3])
                result = self.xor_op(self.get_register(rs1), self.get_register(rs2))
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "sll":
                rd, rs1, rs2 = map(reg_number, args[:3])
                shamt = self.get_register(rs2) & 0x1F
                result = self.sll(self.get_register(rs1), shamt)
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "srl":
                rd, rs1, rs2 = map(reg_number, args[:3])
                shamt = self.get_register(rs2) & 0x1F
                result = self.srl(self.get_register(rs1), shamt)
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "slt":
                rd, rs1, rs2 = map(reg_number, args[:3])
                result = self.slt(self.get_register(rs1), self.get_register(rs2))
                self.set_register(rd, result)
                self.log.append(f'{instr["raw"]} -> x{rd} = {result}')

            elif op == "sb":
                rs2 = reg_number(args[0]); offset = int(args[1]); rs1 = reg_number(args[2])
                address = self.get_register(rs1) + offset
                self.memory.store_byte(address, self.get_register(rs2))
                self.log.append(f'{instr["raw"]} -> mem[{address}] = {self.get_register(rs2)}')

            elif op == "sh":
                rs2 = reg_number(args[0]); offset = int(args[1]); rs1 = reg_number(args[2])
                address = self.get_register(rs1) + offset
                self.memory.store_half(address, self.get_register(rs2))
                self.log.append(f'{instr["raw"]} -> mem[{address}] = {self.get_register(rs2)}')

            elif op == "sw":
                rs2 = reg_number(args[0]); offset = int(args[1]); rs1 = reg_number(args[2])
                address = self.get_register(rs1) + offset
                self.memory.store_word(address, self.get_register(rs2))
                self.log.append(f'{instr["raw"]} -> mem[{address}] = {self.get_register(rs2)}')

            else:
                raise ValueError("Unknown instruction: " + op)

        except Exception as e:
            self.log.append("Error in Instruction: " + instr["raw"] + " (" + str(e) + ")")
            return False

        return True

    def get_registers_as_string(self):
        result = ""
        for i in range(32):
            result += f"x{i} = {self.registers[i]}\n"
        return result
