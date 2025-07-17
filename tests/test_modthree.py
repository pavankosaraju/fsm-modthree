import sys
sys.path.append('./src')
import unittest
import random
from src.modthree import modthree,readfile

class TestModThree(unittest.TestCase):
    def setUp(self):
        self.test_file_path = './tests/testcases.txt'
        self.modthree_test_cases = dict()

        # Get 10 random sample cases
        for i in range(10):
            intv = random.randint(1, 1000)
            mod3 = intv%3
            self.modthree_test_cases[str(bin(intv)[2:])] = mod3

    def test_valid_readfile(self):
        vals = readfile(self.test_file_path)
        self.assertIsInstance(vals, list)

    def test_invalid_readfile(self):
        random_file = 'random.csv'
        with self.assertRaisesRegex(Exception, f"Invalid file type {random_file}. Only .txt files are supported"):
            readfile(random_file)

    def test_modthree(self):
        for k,v in self.modthree_test_cases.items():
            _,result = modthree(k,verbose=False)[0]
            self.assertEqual(result, str(v))

    def test_modthree_file(self):
        result = modthree(self.test_file_path,verbose=False)
        self.assertIsInstance(result, list)
        for bin_int,mod3 in result:
            self.assertIsInstance(bin_int, str)
            self.assertIsInstance(mod3, str)
            act_mod3 = int(bin_int, 2)%3
            self.assertEqual(act_mod3, int(mod3))

    def test_invalid_modthree(self):
        test_case = '10101211'
        valid_alpabets = {'0','1'}
        with self.assertRaisesRegex(ValueError, f"Invalid input symbol: 2. Must be one of {valid_alpabets}"):
             modthree(test_case)


if __name__ == '__main__':
    unittest.main()