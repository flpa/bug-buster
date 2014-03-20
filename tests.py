import unittest
import bugbuster

class Tests(unittest.TestCase):
    def setUp(self):
        "hi"
    def test_sample(self):
        self.assertEqual(3, 2)

if __name__ == '__main__':
    unittest.main()
