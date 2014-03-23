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
    def _write_tempfile(self, *lines):
        tmp = NamedTemporaryFile()
        for line in lines:
            tmp.write(line)
            tmp.write('\n')
        tmp.flush()
        return tmp
    
    def test_read_landscape(self):
        tmpfile = self._write_tempfile("###", " - ")
        landscape = read_landscape(tmpfile.name)

        self.assertEquals(landscape.rows, ["###", " - "])
        
        tmpfile.close()

    def test_read_bugspec(self):
        tmpfile = self._write_tempfile("[]", "{}")
        bugspec = read_bugspec(tmpfile.name)

        self.assertEquals(bugspec.width, 2)
        self.assertEquals(bugspec.height, 2)

        expectedPoints = set()
        expectedPoints.add(Point(0,0,'['))
        expectedPoints.add(Point(1,0,']'))
        expectedPoints.add(Point(0,1,'}'))
        expectedPoints.add(Point(1,1,'}'))

        self.assertEquals(bugspec.points, expectedPoints)
        
        tmpfile.close()
        
if __name__ == '__main__':
    unittest.main()
