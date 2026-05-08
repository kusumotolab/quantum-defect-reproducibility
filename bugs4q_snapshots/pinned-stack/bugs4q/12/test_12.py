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
    def test_12(self):
        counts = module.run()
        expected = {'00': 256, '01': 256, '10': 256, '11': 256}
        pvalue, alpha = chi_square_pvalue(expected, counts)
        self.assertIsNotNone(pvalue)
        self.assertGreater(pvalue, alpha)


if __name__ == '__main__':
    unittest.main()