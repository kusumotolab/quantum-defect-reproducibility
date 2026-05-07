import unittest
import importlib.util
import sys
from qiskit.test import *
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.utils import lower_confidence_bound

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(QiskitTestCase,unittest.TestCase):
    def test_30(self):
        counts = module.run()
        logical_counts = {bitstring[::-1]: count for bitstring, count in counts.items()}
        marked = {'0101', '1100', '1101', '1110', '1111'}
        marked_total = sum(logical_counts.get(bit, 0) for bit in marked)
        total_shots = sum(logical_counts.values())
        p_theory = 0.95        
        lower_bound = lower_confidence_bound(p_theory, total_shots)

        self.assertGreaterEqual(marked_total / total_shots, lower_confidence_bound(p_theory, total_shots))


if __name__ == '__main__':
    unittest.main()