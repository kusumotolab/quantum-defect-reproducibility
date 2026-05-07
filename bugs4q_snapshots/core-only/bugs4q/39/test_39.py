import unittest
import importlib.util
import sys
from qiskit.test import *
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.utils import chi_square_pvalue

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(QiskitTestCase,unittest.TestCase):
    def test_39(self):
        counts = module.run()
        expected = {
            '0000': 64, '0001': 64, '0010': 64, '0011': 64,
            '0100': 64, '0101': 64, '0110': 64, '0111': 64,
            '1000': 64, '1001': 64, '1010': 64, '1011': 64,
            '1100': 64, '1101': 64, '1110': 64, '1111': 64
        }
        pvalue, alpha = chi_square_pvalue(expected, counts)
        self.assertIsNotNone(pvalue)
        self.assertGreater(pvalue, alpha)


if __name__ == '__main__':
    unittest.main()