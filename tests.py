import unittest
from bugbuster import *

class BugSpecTests(unittest.TestCase):

    def test_init(self):
        width = 5
        height = 10

        spec = BugSpec(width, height)

        self.assertEqual(width, spec.width)
        self.assertEqual(height, spec.height)

    def test_add_point(self):
        spec = BugSpec(5,5)

        p = Point('a', 0, 0)
        spec.add_point(p)

        self.assertEqual([p],spec.points)

class Tests(unittest.TestCase):

    def test_flatten(self):
        result = flatten([[1,2],[3,4]])
        self.assertEquals(result, [1,2,3,4]);
        
if __name__ == '__main__':
    unittest.main()
