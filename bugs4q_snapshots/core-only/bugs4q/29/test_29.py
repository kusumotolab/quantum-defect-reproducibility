import unittest
import importlib.util
import sys
from qiskit.test import QiskitTestCase

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(QiskitTestCase,unittest.TestCase):
    def test_27(self):
        answer = module.run()
        max_key = max(answer, key=answer.get)
        self.assertEqual(max_key, '011')


if __name__ == '__main__':
    unittest.main()