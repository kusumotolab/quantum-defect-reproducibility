import unittest
import importlib.util
import sys

target_file = sys.argv.pop(1)
spec = importlib.util.spec_from_file_location("target", target_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Test(unittest.TestCase):
    def test_4(self):
        result = module.run()
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()