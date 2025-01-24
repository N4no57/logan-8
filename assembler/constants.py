INSTRUCTION_SET = {
    'nop'   : 0x00,
    'hlt'   : 0x01,
    'mw'    : 0x02,
    'sw'    : 0x03,
    'lw'    : 0x04,
    'push'  : 0x05,
    'pop'   : 0x06,
    'inb'   : 0x07,
    'outb'  : 0x08,
    'add'   : 0x09,
    'adc'   : 0x0A,
    'sub'   : 0x0B,
    'sbb'   : 0x0C,
    'nor'   : 0x0D,
    'or'    : 0x0E,
    'and'   : 0x0F,
    'rsh'   : 0x10,
    'jmp'   : 0x11,
    'jc'    : 0x12,
    'jnc'   : 0x13,
    'jz'    : 0x14,
    'jnz'   : 0x15,
    'lda'   : 0x16,
    'clf'   : 0x17,
    'sie'   : 0x18,
    'cie'   : 0x19
}

REGISTERS = {
    'r0': 0x0,
    'r1': 0x1,
    'r2': 0x2,
    'r3': 0x3,
    'r4': 0x4,
    'r5': 0x5,
    'r6': 0x6,
    'r7': 0x7,
    'r8': 0x8,
    'r9': 0x9,
    'r10': 0xA,
    'r11': 0xB,
    'r12': 0xC,
    'r13': 0xD,
    'r14': 0xE,
    'r15': 0xF
}

INSTRUCTION_BYTES = {
    'nop'   : {'none': 1},
    'hlt'   : {'none': 1},
    'mw'    : {'immediate': 3, 'register': 2},
    'sw'    : {'direct': 4, 'indirect': 4, 'register_indirect': 2, 'indexed': 2},
    'lw'    : {'direct': 4, 'indirect': 4, 'register_indirect': 2, 'indexed': 2},
    'push'  : {'immediate': 2, 'register': 2},
    'pop'   : {'register': 2},
    'inb'   : {'register': 2},
    'outb'  : {'immediate': 2, 'register': 2},
    'add'   : {'immediate': 3, 'register': 2},
    'adc'   : {'immediate': 3, 'register': 2},
    'sub'   : {'immediate': 3, 'register': 2},
    'sbb'   : {'immediate': 3, 'register': 2},
    'nor'   : {'immediate': 3, 'register': 2},
    'or'    : {'immediate': 3, 'register': 2},
    'and'   : {'immediate': 3, 'register': 2},
    'rsh'   : {'immediate': 3, 'register': 2},
    'jmp'   : {'direct': 3, 'indirect': 3},
    'jc'    : {'direct': 3, 'indirect': 3},
    'jnc'   : {'direct': 3, 'indirect': 3},
    'jz'    : {'direct': 3, 'indirect': 3},
    'jnz'   : {'direct': 3, 'indirect': 3},
    'lda'   : {'immediate': 3},
    'clf'   : {'none': 1},
    'sie'   : {'none': 1},
    'cie'   : {'none': 1}
}

ADDRESSING_MODE_BITS = {
    'nop'   : {'none': 0b00},
    'hlt'   : {'none': 0b00},
    'mw'    : {'immediate': 0b00, 'register': 0b01},
    'sw'    : {'direct': 0b00, 'indirect': 0b01, 'register_indirect': 0b10, 'indexed': 0b11},
    'lw'    : {'direct': 0b00, 'indirect': 0b01, 'register_indirect': 0b10, 'indexed': 0b11},
    'push'  : {'immediate': 0b00, 'register': 0b01},
    'pop'   : {'register': 0b00},
    'inb'   : {'register': 0b00},
    'outb'  : {'immediate': 0b00, 'register': 0b00},
    'add'   : {'immediate': 0b00, 'register': 0b01},
    'adc'   : {'immediate': 0b00, 'register': 0b01},
    'sub'   : {'immediate': 0b00, 'register': 0b01},
    'sbb'   : {'immediate': 0b00, 'register': 0b01},
    'nor'   : {'immediate': 0b00, 'register': 0b01},
    'or'    : {'immediate': 0b00, 'register': 0b01},
    'and'   : {'immediate': 0b00, 'register': 0b01},
    'rsh'   : {'immediate': 0b00, 'register': 0b01},
    'jmp'   : {'direct': 0b00, 'indirect': 0b01},
    'jc'    : {'direct': 0b00, 'indirect': 0b01},
    'jnc'   : {'direct': 0b00, 'indirect': 0b01},
    'jz'    : {'direct': 0b00, 'indirect': 0b01},
    'jnz'   : {'direct': 0b00, 'indirect': 0b01},
    'lda'   : {'immediate': 0b00},
    'clf'   : {'none': 0b00},
    'sie'   : {'none': 0b00},
    'cie'   : {'none': 0b00}
}

MAGIC_NUMBER = 0xCAFEBABE