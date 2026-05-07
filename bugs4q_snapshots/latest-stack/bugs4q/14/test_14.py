import unittest
import importlib.util
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.utils import compute_component_delta

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_14(self):
        exval, qval = module.run()
        delta_real = compute_component_delta(exval.real, total_shots=100000)
        delta_imag = compute_component_delta(exval.imag, total_shots=100000)

        self.assertAlmostEqual(qval.real, exval.real, delta=delta_real)
        self.assertAlmostEqual(qval.imag, exval.imag, delta=delta_imag)


if __name__ == '__main__':
    unittest.main()