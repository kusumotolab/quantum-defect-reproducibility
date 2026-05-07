import unittest
import importlib.util
import sys

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_10(self):
        qc = module.run()
        self.assertEqual(str(qc), '   ┌─────────┐\nq: ┤ P(0.24) ├\n   └─────────┘')


if __name__ == '__main__':
    unittest.main()