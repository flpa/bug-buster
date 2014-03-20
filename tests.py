import unittest
from bugbuster import *

class BugSpecTests(unittest.TestCase):

    def test_init(self):
        width = 5
        height = 10

        spec = BugSpec(width, height)

        self.assertEqual(width, spec.width)
        self.assertEqual(height, spec.height)

    def test_addpoint(self):
        spec = BugSpec(5,5)

        p = Point('a', 0, 0)
        spec.addpoint(p)

        self.assertEqual([p], spec.points)
        
if __name__ == '__main__':
    unittest.main()
