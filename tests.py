import unittest
from bugbuster import *

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
    def setUp(self):
        self.tempfile = NamedTemporaryFile()
    
    def tearDown(self):
        self.tempfile.close()
    
    def _create_tempfile_with_lines(self, *lines):
        for line in lines:
            self.tempfile.write(line)
            self.tempfile.write('\n')
        self.tempfile.flush()

    # TODO extract ReadLandscapeTests
    def test_read_landscape(self):
        self._create_tempfile_with_lines("###", " - ")
        landscape = read_landscape(self.tempfile.name)

        self.assertEquals(landscape.rows, ["###", " - "])

    def test_read_landscape_trailing_empty_line_is_ignored(self):
        self._create_tempfile_with_lines("###", " - ", "")
        landscape = read_landscape(self.tempfile.name)

        self.assertEquals(landscape.rows, ["###", " - "])

    def test_read_landscape_leading_blank_line_is_added(self):
        self._create_tempfile_with_lines("   ", "###", " - ")
        landscape = read_landscape(self.tempfile.name)

        self.assertEquals(landscape.rows, ["   ", "###", " - "])

    def test_read_landscape_leading_empty_lines_are_ignored(self):
        self._create_tempfile_with_lines("", "", "###", " - ")
        landscape = read_landscape(self.tempfile.name)

        self.assertEquals(landscape.rows, ["###", " - "])

    def test_read_landscape_interjacent_empty_line_causes_error(self):
        self._create_tempfile_with_lines("###", "", " - ")
        self.assertRaises(AssertionError, read_landscape, self.tempfile.name)
        
    def test_read_bugspec(self):
        self._create_tempfile_with_lines("[]",
                                         "[]",
                                         "{}")
        bugspec = read_bugspec(self.tempfile.name)

        self.assertEquals(bugspec.width, 2)
        self.assertEquals(bugspec.height, 3)

        expectedPoints = set()
        expectedPoints.add(Point(0, 0, '['))
        expectedPoints.add(Point(1, 0, ']'))
        expectedPoints.add(Point(0, 1, '['))
        expectedPoints.add(Point(1, 1, ']'))
        expectedPoints.add(Point(0, 2, '{'))
        expectedPoints.add(Point(1, 2, '}'))

        self.assertEquals(bugspec.points, expectedPoints)

    def test_read_bugspec_whitespace_ignored(self):
        self._create_tempfile_with_lines("[ ]")
        bugspec = read_bugspec(self.tempfile.name)

        self.assertEquals(bugspec.width, 3)
        self.assertEquals(bugspec.height, 1)

        expectedPoints = set()
        expectedPoints.add(Point(0, 0, '['))
        expectedPoints.add(Point(2, 0, ']'))
        self.assertEquals(bugspec.points, expectedPoints)

    def test_read_bugspec_leading_trailing_empty_lines(self):
        self._create_tempfile_with_lines("",
                                         "!",
                                         "")
        bugspec = read_bugspec(self.tempfile.name)

        self.assertEquals(bugspec.width, 1)
        self.assertEquals(bugspec.height, 1)

        expectedPoints = set()
        expectedPoints.add(Point(0, 0, '!'))
        self.assertEquals(bugspec.points, expectedPoints)

    def test_read_bugspec_whitespaces_all_around(self):
        self._create_tempfile_with_lines("",
                                         "   ",
                                         " ! ",
                                         "   ",
                                         "")
        bugspec = read_bugspec(self.tempfile.name)

        self.assertEquals(bugspec.width, 1)
        self.assertEquals(bugspec.height, 1)

        expectedPoints = set()
        expectedPoints.add(Point(0, 0, '!'))
        self.assertEquals(bugspec.points, expectedPoints)

    def read_bugspec_relative_coords(self):
        self._create_tempfile_with_lines("   ",
                                         "  x",
                                         " x ",
                                         "   ")
        bugspec = read_bugspec(self.tempfile.name)

        self.assertEquals(bugspec.width, 2)
        self.assertEquals(bugspec.height, 2)

        expectedPoints = set()
        expectedPoints.add(Point(1, 0, 'x'))
        expectedPoints.add(Point(0, 1, 'x'))
        self.assertEquals(bugspec.points, expectedPoints)

class CountBugsTests(unittest.TestCase):
    def _protobug_test(self, landscapefile, bugcount):
        result = count_bugs("bug.txt", landscapefile)
        self.assertEquals(result, bugcount)        
    
    def test_sample(self):
        self._protobug_test("landscape.txt", 3)

    def test_exactly_one_bug_fits_in_landscape(self):
        self._protobug_test("tests/res/landscape-single-bug-size.txt", 1)

    def test_landscape_smaller_than_bug(self):
        self._protobug_test("tests/res/landscape-smaller-than-bug.txt", 0)

    def test_partial_bugs(self):
        self._protobug_test("tests/res/landscape-partial-bugs.txt", 0)

    def test_bugs_next_to_each_other(self):
        self._protobug_test("tests/res/landscape-bugs-next-to-each-other.txt", 3)

    def test_empty_line(self):
        self._protobug_test("tests/res/landscape-empty-line.txt", 2)

    def test_other_symbols(self):
        self._protobug_test("tests/res/landscape-other-symbols.txt", 3)
        
if __name__ == '__main__':
    unittest.main()
