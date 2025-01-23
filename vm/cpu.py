from time import sleep

def read(filename, mode):
    machine_code = None
    with open(filename, mode) as f:
        machine_code = f.read()

    if mode == "rb":
        int_machine_code = list(machine_code)
        return int_machine_code

    return machine_code

class CPU:
    def __init__(self, Hz):
        self.registers = {
            "0000": 0x0,  # r0
            "0001": 0x0,  # r1
            "0010": 0x0,  # r2
            "0011": 0x0,  # r3
            "0100": 0x0,  # r4
            "0101": 0x0,  # r5
            "0110": 0x0,  # r6
            "0111": 0x0,  # r7
            "1000": 0x0,  # r8
            "1001": 0x0,  # r9
            "1010": 0x0,  # r10
            "1011": 0x0,  # r11
            "1100": 0x0,  # r12
            "1101": 0x0,  # r13
            "1110": 0x0,  # r14
            "1111": 0x0,  # r15
        }

        self.PC = 0x0000

        self.H = 0x00
        self.L = 0x00

        self.SP = 0xFFFF

        self.F = {
            "Z": "0",
            "C": "0"
        }

        self.memory = [0x00] * 0xFFFF

        self.Hz = Hz

    def set_flags(self, raw_value):
        new_value = raw_value % 256
        self.F["C"] = "1" if raw_value > 255 else "0"
        self.F["Z"] = "1" if new_value == 0 else "0"

    def read_byte(self, address):
        return self.memory[address]

    def write_byte(self, address: int, value: int):
        if address > 0xFFE:
            self.memory[address] = value

    def fetch(self) -> str:
        return_val = self.read_byte(self.PC)
        self.PC += 1
        return str(format(return_val, '08b'))

    def check_condition(self, condition):
        if condition == "00": # ZERO
            return True if self.F["Z"] == "1" else False
        elif condition == "01": # NOT ZERO
            return True if self.F["Z"] == "0" else False
        elif condition == "10": # CARRY
            return True if self.F["C"] == "1" else False
        elif condition == "11": # NOT CARRY
            return True if self.F["C"] == "0" else False

    def execute(self, command):
        opcode = command[:6]
        addressing_mode = command[6:8]
        if opcode == "000000": # NOP
            pass
        elif opcode == "000001": # HLT
            return False
        elif opcode == "000010": # MW
            if addressing_mode == "00": # immediate
                constant = int(self.fetch(), base=2)
                register = self.fetch()[:4]
                self.registers[register] = constant
            elif addressing_mode == "01": # register
                operand = self.fetch()
                register1 = operand[:4]
                register2 = operand[4:]
                self.registers[register2] = self.registers[register1]
        elif opcode == "000011": # SW
            if addressing_mode == "00": # direct
                address_low = self.fetch()
                address_high = self.fetch()
                address = int(address_high + address_low, base=2)
                register = self.fetch()[:4]
                self.write_byte(address, self.registers[register])
            elif addressing_mode == "01": # indirect
                address_low = self.fetch()
                address_high = self.fetch()
                register = self.fetch()[:4]
                address = int(address_high + address_low, base=2)
                address_low = format(self.read_byte(address), '08b')
                address_high = format(self.read_byte(address + 1), '08b')
                address = int(address_high + address_low, base=2)
                self.write_byte(address, self.registers[register])
            elif addressing_mode == "10": # register indirect
                register = self.fetch()[:4]
                address = int(format(self.H, "08b") + format(self.L, "08b"), base=2)
                self.write_byte(address, self.registers[register])
            elif addressing_mode == "11": # indexed
                # address = int(str(self.H) + str(self.L), base=2) + int(self.fetch(), base=2)
                # register = self.fetch()[:4]
                # self.write_byte(address, self.registers[register])
                pass
        elif opcode == "000100": # LW
            if addressing_mode == "00": # direct
                address_low = self.fetch()
                address_high = self.fetch()
                address = int(address_high + address_low, base=2)
                register = self.fetch()[:4]
                self.registers[register] = self.read_byte(address)
            elif addressing_mode == "01": # indirect
                address_low = self.fetch()
                address_high = self.fetch()
                register = self.fetch()[:4]
                address = int(address_high + address_low, base=2)
                address_low = format(self.read_byte(address), '08b')
                address_high = format(self.read_byte(address + 1), '08b')
                address = int(address_high + address_low, base=2)
                self.registers[register] = self.read_byte(address)
            elif addressing_mode == "10": # register indirect
                pass
            elif addressing_mode == "11": # indexed
                register = command[8:12]
                address = int(str(self.H) + str(self.L), base=2) + int(command[16:24], base=2)
                self.registers[register] = self.read_byte(address)
        elif opcode == "000101": # PUSH
            pass
        elif opcode == "000110": # POP
            pass
        elif opcode == "000111": # INB
            pass
        elif opcode == "001000": # OUTB
            pass
        elif opcode == "001001": # ADD
            pass
        elif opcode == "001010": # ADC
            pass
        elif opcode == "001011": # SUB
            pass
        elif opcode == "001100": # SBB
            pass
        elif opcode == "001101": # NOR
            pass
        elif opcode == "001110": # OR
            pass
        elif opcode == "001111": # AND
            pass
        elif opcode == "010000": # RSH
            pass
        elif opcode == "010001": # JMP
            address_low = self.fetch()
            address_high = self.fetch()
            address = int(address_high + address_low, base=2)
            self.PC = address
        elif opcode == "010010": pass # JC
        elif opcode == "010011": pass # JNC
        elif opcode == "010100": pass # JZ
        elif opcode == "010101": pass # JNZ
        elif opcode == "010110": # LDA
            LowByte = self.fetch()
            HighByte = self.fetch()
            self.H = int(HighByte, base=2)
            self.L = int(LowByte, base=2)
        elif opcode == "010111": pass # CLF
        elif opcode == "011000": pass # SIE
        elif opcode == "011001": pass # CIE
        return True

    def run(self):
        instruction = 0
        while True:
            self.registers["0000"] = 0x0
            command = self.fetch()
            instruction += 1
            if not self.execute(command):
                break
            sleep(self.Hz)

        #print("instructions:", instruction)

    def load_program(self, bytes: list):
        for i, byte in enumerate(bytes):
            self.memory[i] = byte

cpu = CPU(1/100000)
program = read("../assembler/output.bin", "rb")
cpu.load_program(program)
cpu.run()
