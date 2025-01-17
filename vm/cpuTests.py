import unittest
from cpu import CPU, read

Hz = 1e+16


class TestInstructions(unittest.TestCase):
    def test_MW_Immediate_MovesValueToRegister(self):
        # Given
        cpu = CPU(1/Hz)
        cpu.load_program(read("./testFiles/MW_Immediate", "wb"))
        # When
        cpu.run()
        # Then
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
