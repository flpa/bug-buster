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

    def _pointset_from_tuples(self, *tuples):
        newset = set()
        for t in tuples:
            newset.add(Point(*t))
        return newset

    def _check_width_height_points(self, width, height, points):
        bugspec = read_bugspec(self.tempfile.name)

        self.assertEquals(bugspec.width, width)
        self.assertEquals(bugspec.height, height)
        self.assertEquals(bugspec.points, points)

    def test_read_bugspec(self):
        self._create_tempfile_with_lines("[]",
                                         "[]",
                                         "{}")
        expected_points = self._pointset_from_tuples((0, 0, '['),
                                                    (1, 0, ']'),
                                                    (0, 1, '['),
                                                    (1, 1, ']'),
                                                    (0, 2, '{'),
                                                    (1, 2, '}'))

        self._check_width_height_points(2, 3, expected_points)

    def test_read_bugspec_whitespace_ignored(self):
        self._create_tempfile_with_lines("[ ]")
        expected_points = self._pointset_from_tuples((0, 0, '['),
                                                    (2, 0, ']'))

        self._check_width_height_points(3, 1, expected_points)
        
    def test_read_bugspec_leading_trailing_empty_lines(self):
        self._create_tempfile_with_lines("",
                                         "!",
                                         "")
        expected_points = self._pointset_from_tuples((0, 0, '!'))

        self._check_width_height_points(1, 1, expected_points)

    def test_read_bugspec_whitespaces_all_around(self):
        self._create_tempfile_with_lines("",
                                         "   ",
                                         " ! ",
                                         "   ",
                                         "")
        expected_points = self._pointset_from_tuples((0, 0, '!'))

        self._check_width_height_points(1, 1, expected_points)
        
    def read_bugspec_relative_coords(self):
        self._create_tempfile_with_lines("   ",
                                         "  x",
                                         " x ",
                                         "   ")
        expected_points = self._pointset_from_tuples((1, 0, 'x'),
                                                    (0, 1, 'x'))

        self._check_width_height_points(2, 2, expected_points)

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
