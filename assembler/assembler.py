import sys

import constants

def tokenise(line):
    line = line.lower()
    line = line.split(';')[0]
    line = line.replace(",", "")
    return line.strip().split()

def assemble(lines):
    symbol_table = {}
    macros = {}
    output = []
    current_address = 0
    macro_mode = False
    macro_body = []
    macro_args = []
    current_macro_name = None
    line_number = 0

    def get_addressing_mode(operands):
        if operands[0].startswith('#'):
            return 'immediate'
        elif operands[0].startswith('r'):
            return 'register'
        elif operands[0].startswith('('):
            return 'indirect'
        elif operands[0].startswith('['):
            if "+" in operands:
                return 'indexed'
            else:
                return 'register_indirect'
        else:
            return 'direct'

    def remove_addressing_identifier(operand):
        if operand.startswith('#'):
            return operand.replace('#', '')

    def get_instruction_size(instruction, operands):
        nonlocal line_number
        if instruction not in constants.INSTRUCTION_BYTES:
            exit(f"Unknown instruction '{instruction}'\nline {line_number}")

        modes = constants.INSTRUCTION_BYTES[instruction]
        if not operands:
            if 'none' in modes:
                return modes['none'], 'none'
            else:
                exit(f"'{instruction}' requires operands\nline {line_number}")

        mode = get_addressing_mode(operands)
        if mode not in modes:
            exit(f"Unsupported addressing mode for {instruction}: {mode}\nline {line_number}")

        return modes[mode], mode

    def remove_base_identifiers(text):
        text = text.replace("%", "")
        text = text.replace("$", "")
        return text

    def find_base(text):
        if text.isnumeric():
            return 10
        elif text.startswith("$"):
            return 16
        elif text.startswith("%"):
            return 2

    def process_directive(tokens, current_address):
        nonlocal macro_mode, macro_body, current_macro_name, macro_args

        if tokens[0] == ".equ":
            # handled by first pass
            pass

        elif tokens[0] == ".org":
            # Set the current address
            if tokens[1] in symbol_table:
                current_address = symbol_table[tokens[1]]
            else:
                current_address = int(remove_base_identifiers(tokens[1]), find_base(tokens[1]))

        elif tokens[0] == ".fill":
            if len(tokens) != 3:
                exit(f".fill directive requires exactly two arguments: end address and fill value.\nline {line_number}")

            end_address = int(remove_base_identifiers(tokens[1]), find_base(tokens[1]))
            fill_value = int(remove_base_identifiers(tokens[2]), find_base(tokens[2]))

            while current_address <= end_address:
                output.append(fill_value & 0xFF)
                current_address += 1

        elif tokens[0] in [".byte", ".db"]:
            # Insert byte values
            for value in tokens[1:]:
                output.append(int(remove_base_identifiers(value), find_base(value)))
                current_address += 1

        elif tokens[0] in [".word", ".dw"]:
            # Insert word values (16-bit)
            for value in tokens[1:]:
                word_value = int(remove_base_identifiers(value), find_base(value))
                output.extend([word_value & 0xFF, (word_value >> 8) & 0xFF])
                current_address += 2

        elif tokens[0] == ".macro":
            # Define a macro

            macro_mode = True
            current_macro_name = tokens[1]
            macro_args = tokens[2:]

        elif tokens[0] == ".endm":
            # End macro definition
            macros[current_macro_name] = (macro_args, macro_body)
            macro_mode = False
            macro_body = []
            macro_args = []
            current_macro_name = None

        else:
            exit(f"Unknown directive: '{tokens[0]}'\nline {line_number}")

        return current_address

    def pass_directives(tokens, current_address):

        if tokens[0] == ".equ":
            symbol_table[tokens[1]] = int(remove_base_identifiers(tokens[2]), find_base(tokens[2]))

        elif tokens[0] == ".org":
            if tokens[1] in symbol_table:
                current_address = symbol_table[tokens[1]]
            else:
                current_address = int(remove_base_identifiers(tokens[1]), find_base(tokens[1]))

        elif tokens[0] == ".fill":
            end_address = int(remove_base_identifiers(tokens[1]), find_base(tokens[1]))
            while current_address <= end_address:
                current_address += 1

        elif tokens[0] in [".byte", ".db"]:
            for _ in tokens[1:]:
                current_address += 1

        elif tokens[0] in [".word", ".dw"]:
            for _ in tokens[1:]:
                current_address += 2

        elif tokens[0] == ".macro":
            pass

        elif tokens[0] == ".endm":
            pass

        return current_address

    def expand_macro(macro_name, macro_params):
        # Expand a macro with its arguments
        args, body = macros[macro_name]
        arg_map = dict(zip(args, macro_params))
        for line in body:
            for key, value in arg_map.items():
                line = line.replace(key, value)
            process_line(line)

    def pass_macro_expansion(macro_name, macro_params):
        args, body = macros[macro_name]
        arg_map = dict(zip(args, macro_params))
        for line in body:
            for key, value in arg_map.items():
                line = line.replace(key, value)
            first_pass(line)

    def data_move_stuff(operands: list, addressing_mode):
        if addressing_mode == "register_indirect":
            output.append(constants.REGISTERS[operands[1]] << 4)

        elif addressing_mode == "direct" or "indirect":
            if addressing_mode == "indirect":
                operands[0] = operands[0].replace("(", "")
                operands[0] = operands[0].replace(")", "")
            if operands[0] not in symbol_table:
                output.append(int(remove_base_identifiers(operands[0]), find_base(operands[0])) & 0xFF)
                output.append(int(remove_base_identifiers(operands[0]), find_base(operands[0])) >> 8)
                output.append(constants.REGISTERS[operands[1]] << 4)
            else:
                output.append(symbol_table[operands[0]] & 0xFF)
                output.append(symbol_table[operands[0]] >> 8)
                output.append(constants.REGISTERS[operands[1]] << 4)

    def ALU_operand_logic(operands: list, addressing_mode: str):
        if addressing_mode == "immediate":
            if operands[0] in symbol_table:
                output.append(symbol_table[operands[0]])
                register1 = constants.REGISTERS[operands[1]] << 4
                register2 = constants.REGISTERS[operands[2]]
                output.append(register1 + register2)
            else:
                output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                  find_base(remove_addressing_identifier(operands[0]))))
                register1 = constants.REGISTERS[operands[1]] << 4
                register2 = constants.REGISTERS[operands[2]]
                output.append(register1 + register2)
        elif addressing_mode == "register":
            register1 = constants.REGISTERS[operands[0]] << 4
            register2 = constants.REGISTERS[operands[1]]
            output.append(register1 + register2)
            output.append(constants.REGISTERS[operands[2]])

    def jump_operand_logic(operands: list, addressing_mode: str):
        if addressing_mode == "direct" or "indirect":
            if addressing_mode == "indirect":
                operands[0] = operands[0].replace("(", "")
                operands[0] = operands[0].replace(")", "")
            if operands[0] in symbol_table:
                output.append(symbol_table[operands[0]] & 0xFF)
                output.append(symbol_table[operands[0]] >> 8)
            else:
                output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                  find_base(remove_addressing_identifier(operands[0]))) & 0xFF)
                output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                  find_base(remove_addressing_identifier(operands[0]))) >> 8)

    def parse_operands(instruction, operands, addressing_mode):
        output = []
        if instruction in ['nop', 'hlt']:
            return None

        if instruction == "mw":
            if addressing_mode == "immediate": # from immediate to register
                output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                  find_base(remove_addressing_identifier(operands[0]))))
                output.append(constants.REGISTERS[operands[1]] << 4)
            elif addressing_mode == "register": # from r1 to r2
                register1 = constants.REGISTERS[operands[0]] << 4
                register2 = constants.REGISTERS[operands[1]]
                output.append(register1 + register2)
        elif instruction == "push":
            if addressing_mode == "immediate":
                output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                  find_base(remove_addressing_identifier(operands[0]))))
            elif addressing_mode == "register":
                output.append(constants.REGISTERS[operands[0]] << 4)
        elif instruction == "pop":
             if addressing_mode == "register":
                output.append(constants.REGISTERS[operands[0]] << 4)
        elif instruction == "sw":
            data_move_stuff(operands, addressing_mode)
        elif instruction == "lw":
            data_move_stuff(operands, addressing_mode)
        elif instruction == "push":
            if addressing_mode == "immediate":
                if operands[0] not in symbol_table:
                    output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                      find_base(remove_addressing_identifier(operands[0]))))
                else:
                    output.append(symbol_table[operands[0]])
            elif addressing_mode == "register":
                output.append(constants.REGISTERS[operands[0]] << 4)
        elif instruction == "pop":
            output.append(constants.REGISTERS[operands[0]] << 4)
        elif instruction == "inb":
            if addressing_mode == "register":
                output.append(constants.REGISTERS[operands[0]] << 4)
        elif instruction == "outb":
            if addressing_mode == "immediate":
                if operands[0] not in symbol_table:
                    output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                      find_base(remove_addressing_identifier(operands[0]))))
                else:
                    output.append(symbol_table[operands[0]])
            elif addressing_mode == "register":
                output.append(constants.REGISTERS[operands[0]] << 4)
        elif instruction == "add":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "adc":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "sub":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "sbb":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "nor":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "or":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "and":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "rsh":
            ALU_operand_logic(operands, addressing_mode)
        elif instruction == "jmp":
            jump_operand_logic(operands, addressing_mode)
        elif instruction == "jc":
            jump_operand_logic(operands, addressing_mode)
        elif instruction == "jnc":
            jump_operand_logic(operands, addressing_mode)
        elif instruction == "jz":
            jump_operand_logic(operands, addressing_mode)
        elif instruction == "jnz":
            jump_operand_logic(operands, addressing_mode)
        elif instruction == "lda": # load address
            if addressing_mode == "immediate":
                if operands[0] in symbol_table:
                    output.append(symbol_table[operands[0]] & 0xFF)
                    output.append(symbol_table[operands[0]] >> 8)
                else:
                    output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                    find_base(remove_addressing_identifier(operands[0]))) & 0xFF)
                    output.append(int(remove_addressing_identifier(remove_base_identifiers(operands[0])),
                                      find_base(remove_addressing_identifier(operands[0]))) >> 8)

        else:
            exit(f"Unknown instruction: '{instruction}'\nline {line_number}")

        return output


    def first_pass(line):
        nonlocal current_address, macro_body
        tokens = tokenise(line)

        if not tokens or tokens[0].startswith(";"):
            # Skip empty lines or comments
            return

        if tokens[0].endswith(":"):
            label = tokens[0][:-1]
            symbol_table[label] = current_address

        elif tokens[0].startswith("."):
            current_address = pass_directives(tokens, current_address)

        elif tokens[0] in macros:
            pass_macro_expansion(tokens[0], tokens[1:])

        else:
            instruction = tokens[0]
            operands = tokens[1:]

            address, _ = get_instruction_size(instruction, operands)

            current_address += address

    def process_line(line):
        nonlocal current_address, macro_mode, macro_body
        tokens = tokenise(line)

        if macro_mode:
            # Collect macro body lines
            if tokens[0].startswith("."):
                current_address = process_directive(tokens, current_address)
                return
            macro_body.append(line)
            return

        if not tokens or tokens[0].startswith(";"):
            # Skip empty lines or comments
            return

        if tokens[0].startswith("."):
            # Process directives
            current_address = process_directive(tokens, current_address)

        elif tokens[0].endswith(':'):
            # handled in first pass
            pass

        elif tokens[0] in macros:
            # Expand macros
            expand_macro(tokens[0], tokens[1:])

        else:
            instruction = tokens[0]
            operands = tokens[1:]

            address, mode = get_instruction_size(instruction, operands)

            opcode = int(format(constants.INSTRUCTION_SET[instruction], '06b') +
                         format(constants.ADDRESSING_MODE_BITS[instruction][mode], '02b'),
                         base=2)

            output.append(opcode)

            operand_bytes = parse_operands(instruction, operands, mode)
            if operand_bytes:
                output.extend(operand_bytes)

            current_address += address

    for line in lines:
        line_number += 1
        first_pass(line)

    line_number = 0
    current_address = 0

    for line in lines:
        line_number += 1
        process_line(line)

    return output, symbol_table

def read_file(filename):
    output = []
    with open(filename, 'r') as f:
        output.extend(f.readlines())
    return output

def write_file(filename, content, mode):
    with open(filename, mode) as f:
        if mode == "wb":
            for number in content:
                f.write(number.to_bytes(1, byteorder='big'))
        elif mode == "w":
            for number in content:
                f.write(" ")
                f.write(format(number, "08b"))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(f"Usage: assembler.py <filename> [output]")

    output_filename = "output.bin"
    if len(sys.argv) == 3:
        output_filename = sys.argv[2]

    assembly_code = read_file(sys.argv[1])

    output, symbol_table = assemble(assembly_code)

    while len(output) > 65535:
        output.pop()

    write_file(output_filename, output, mode="wb")

