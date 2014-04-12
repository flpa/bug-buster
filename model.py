"""model.py: The class definitions for bugbuster."""

class Point(object):

    """A point in a bug specification.

    Instance variables:
    x
    y
    value
    """

    def __init__(self, x, y, value):
        self.value = value
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overridden equality check comparing class and attributes."""
        return (isinstance(other, self.__class__) and self.value == other.value
                and self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        """Overriden not-equals method for consistency with __eq__."""
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value) + hash(self.x) + hash(self.y)

    def __repr__(self):
        return "%s(%s/%s)" % (self.value, self.x, self.y)

class BugSpec(object):

    """A data object that holds the distinctive features of a bug.

    The representation is based on a virtual rectangle encircling the bug.
    Therefore, this class consists of a set of points that represents the
    features of the bug as well as width and height of the rectangle.
    Point coordinates are relative to the rectangle.
    
    Instance variables:
    width -- width of the virtual rectangle
    height -- height of the virtual rectangle
    points -- the set of points
    """

    def __init__(self, width, height, points):
        self.width = width
        self.height = height
        self.points = points

class Landscape(object):
    
    """A class representing a landscape to be scanned for bugs.
    
    A landscape consists of a collection of rows of equal length and holds 
    information about the total width and height.

    Instance variables:
    width
    height
    rows

    Methods:
    add_row
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []
        self._interjacent_empty_rows = []

    def add_row(self, row):
        
        """Add a row to the landscape.

        If 'row' is the first non-empty row, this initializes the width of
        the landscape. Otherwise, the width of the row is verified.

        Leading and trailing empty rows are ignored. Interjacent empty
        rows cause an AssertionError.
        """
        if row:
            self._verify_no_interjacent_empty_rows()
            self._set_or_verify_width(row)
            self._add_row(row)
        elif self.rows:
            self._interjacent_empty_rows.append(row)
        
    def _verify_no_interjacent_empty_rows(self):
        assert not self._interjacent_empty_rows, "There have been empty \
rows since the last content row. This is currently not supported!"

    def _set_or_verify_width(self, row):
        row_length = len(row)
        if self.width:
            self._verify_width(row_length)
        else:
            self.width = row_length
            
    def _verify_width(self, row_length):
        assert self.width == row_length, "Row length %s differs from width %s,\
 this is currently not supported!" % (row_length, self.width)
            
    def _add_row(self,row):
        self.rows.append(row)
        self.height += 1
