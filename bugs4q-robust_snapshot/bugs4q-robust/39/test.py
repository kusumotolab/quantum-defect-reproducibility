import unittest
import importlib.util
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.utils import chi_square_pvalue

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_39(self):
        counts, shots = module.run()
        expected = {
            '0000': shots/16, '0001': shots/16, '0010': shots/16, '0011': shots/16,
            '0100': shots/16, '0101': shots/16, '0110': shots/16, '0111': shots/16,
            '1000': shots/16, '1001': shots/16, '1010': shots/16, '1011': shots/16,
            '1100': shots/16, '1101': shots/16, '1110': shots/16, '1111': shots/16
        }
        pvalue, alpha = chi_square_pvalue(expected, counts)
        self.assertIsNotNone(pvalue)
        self.assertGreater(pvalue, alpha)


if __name__ == '__main__':
    unittest.main()