import unittest
from bugbuster import *

class BugSpecTests(unittest.TestCase):

    # basic sanity test, will probably be removed
    def test_init(self):
        width = 5
        height = 10
        points = [4, 5]

        spec = BugSpec(width, height, points)

        self.assertEqual(width, spec.width)
        self.assertEqual(height, spec.height)
        self.assertEqual(points, spec.points)

    
class LandscapeTests(unittest.TestCase):
    def test_landscape(self):
        landscape = Landscape()
        landscape.add_row("abcd")
        landscape.add_row("efgh")
        
        self.assertEqual(landscape.width, 4)
        self.assertEqual(landscape.height, 2)

class Tests(unittest.TestCase):

    def test_flatten(self):
        result = flatten([[1,2],[3,4]])
        self.assertEquals(result, [1,2,3,4]);

    def test_array_matches_templaet(self):
        result = array_matches_template([[1],[2]], [[1], [3]])
        self.assertEquals(result, [1])
        
if __name__ == '__main__':
    unittest.main()
