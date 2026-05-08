import unittest
import importlib.util
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.utils import lower_confidence_bound

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_30(self):
        counts, shots = module.run()
        logical_counts = {bitstring[::-1]: count for bitstring, count in counts.items()}
        marked = {'0101', '1100', '1101', '1110', '1111'}
        marked_total = sum(logical_counts.get(bit, 0) for bit in marked)
        p_theory = 0.95

        self.assertGreaterEqual(marked_total / shots, lower_confidence_bound(p_theory, shots))


if __name__ == '__main__':
    unittest.main()