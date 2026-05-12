import unittest
import importlib.util
import sys

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_7(self):
        circuit, unctl_circuit, final_circuit = module.run()
        self.assertEqual(str(circuit),'      ┌──────┐\nqr_0: ┤1     ├\n      │      │\nqr_1: ┤0 ghz ├\n      │      │\nqr_2: ┤2     ├\n      └──┬───┘\nqr_3: ───■────\n              ')
        self.assertEqual(str(final_circuit),'      ┌──────┐\nqr_0: ┤1     ├\n      │      │\nqr_1: ┤0 ghz ├\n      │      │\nqr_2: ┤2     ├\n      └──────┘\nqr_3: ────────\n              ')
        self.assertEqual(str(unctl_circuit),'              \nqr_0: ────────\n      ┌──────┐\nqr_1: ┤0     ├\n      │      │\nqr_2: ┤1 ghz ├\n      │      │\nqr_3: ┤2     ├\n      └──────┘')


if __name__ == '__main__':
    unittest.main()