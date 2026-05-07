import unittest
import importlib.util
import sys

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_16(self):
        statevector = module.run()
        self.assertEqual(str(statevector),'[0.70710678+0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.        +0.j\n 0.        +0.j 0.        +0.j 0.        +0.j 0.70710678+0.j]')


if __name__ == '__main__':
    unittest.main()