import unittest
import importlib.util
import sys
import warnings

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_37(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('error', message='.*qiskit.compile.*', category=DeprecationWarning)
            module.run()


if __name__ == '__main__':
    unittest.main()