import unittest
from cpu import CPU

Hz = 1e+16


class TestInstructions(unittest.TestCase):
    def test_MW_Immediate_MovesValueToRegister(self):
        # Given
        cpu = CPU(1/Hz)
        cpu.load_program([0b00001000, 0b00010101, 0b01100000, 0b00000100])
        # When
        cpu.run()
        # Then
        self.assertEqual(cpu.registers["0110"], 0b00010101)

    def test_MW_Register_MovesValueFromRegisterToRegister(self):
        cpu = CPU(1/Hz)
        cpu.load_program([0b0001000, 0b01000001, 0b00010000, 0b00001001, 0b00010011, 0b00000100])

        cpu.run()

        self.assertEqual(cpu.registers["0011"], 0b01000001)

    def test_SW_Direct_StoresValueFromRegister(self):
        cpu = CPU(1/Hz)
        cpu.load_program([0b00001000, 0b00010111, 0b00010000, 0b00001100, 0b00000000, 0b00010000, 0b00010000, 0b00000100])

        cpu.run()

        self.assertEqual(cpu.memory[0x1000], 0b00010111)

    def test_SW_Indirect_StoresValueFromRegister(self):
        pass


if __name__ == '__main__':
    unittest.main()
