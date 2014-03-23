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
    def _init_simple(self):
        landscape = Landscape()
        landscape.add_row("foo")
        landscape.add_row("bar")
        return landscape
    
    def test_width(self):
        landscape = self._init_simple()
        self.assertEqual(landscape.width, 3)

    def test_height(self):
        landscape = self._init_simple()
        self.assertEqual(landscape.height, 2)

    def test_rows(self):
        landscape = self._init_simple()
        self.assertEqual(landscape.rows, ["foo","bar"])
    
    def test_row_width_verification(self):
        landscape = Landscape()
        landscape.add_row("short row")

        self.assertRaises(AssertionError, landscape.add_row, "way longer row")

from tempfile import NamedTemporaryFile

class MainTests(unittest.TestCase):
    def test_read_landscape(self):
        tmp = NamedTemporaryFile()
        tmp.write('###\n')
        tmp.write(' - \n')
        tmp.flush()
        
        landscape = read_landscape(tmp.name)

        self.assertEquals(landscape.rows, ["###", " - "])
        
        tmp.close()
        
if __name__ == '__main__':
    unittest.main()
