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

# main part
        
def read_landscape(filepath):
    """Creates a Landscape by parsing the given file."""
    
    landscape = Landscape()
    f = open(filepath, "r")
    try:
        for line in f:
            landscape.add_row(line.strip('\n'))
    finally:
        f.close()
    return landscape

def _is_not_blank(char):
    """Determines whether a character is not equal to ' '."""
    return char != ' '

def read_bugspec(filepath, char_predicate=_is_blank):
    """Reads a bug specification from a file.

    Keyword arguments:
    char_predicate -- the predicate function that decides whether a character
    is relevant for the bug specification (default is_blank)
    """

    x = y = 0
    x_max = x_min = y_max = y_min = None
    points = []

    f = open(filepath, "r")
    try:
        for char in f.read():
            if char == '\n':
                y += 1
                x = 0
                continue

            if char_predicate(char):
                points.append(Point(x, y, char))
                x_max = max(x_max, x)
                x_min = _get_lower(x_min, x)
                y_max = max(y_max, y)
                y_min = _get_lower(y_min, y)

            x += 1
    finally:
        # using the 'with' statement would look way better but requires 2.5+
        f.close()

    assert points, "The bug specification contains no relevant points!"
    
    _adapt_coordinates(points, x_min, y_min)

    # + 1 to compensate zero-based indexes
    width = x_max - x_min + 1
    height = y_max - y_min + 1
        
    return BugSpec(width, height, set(points))

def _adapt_coordinates(points, x_min, y_min):
    """Adapt coordinates in 'points' according to 'x_min' and 'y_min".

    Adapting means modifying the point coordinates so that they reflect
    their positions in a virtual rectangle encircling the points, e.g.
    when invoked with points = ((1 1) (1 2)), x_min = 1, y_min = 1, points
    will be modified to be ((0 0) (0 1)).
    """

    if x_min | y_min:
        for p in points:
            p.x -= x_min
            p.y -= y_min

def _get_lower(old, new):
    if old is None or old > new:
        return new
    return old

def count_bugs(bugfile, landscapefile):
    bugspec = read_bugspec(bugfile)
    landscape = read_landscape(landscapefile)

    x_offset = 0
    y_offset = 0

    bug_count = 0

    # TODO instance vars reduce param passing
    while _in_landscape(landscape, bugspec, x_offset, y_offset):
        if _all_points_match(landscape, bugspec, x_offset, y_offset):
            bug_count += 1

        if _reached_row_border(landscape, bugspec, x_offset):
            x_offset = 0
            y_offset += 1
        else:
            x_offset += 1
    
    return bug_count

def _in_landscape(landscape, bugspec, x_offset, y_offset):
    return (landscape.width >= bugspec.width + x_offset and
            landscape.height >= bugspec.height + y_offset)

def _all_points_match(landscape, bugspec, x_offset, y_offset):
    return all(landscape.rows[y_offset + p.y][x_offset + p.x] == p.value
               for p in bugspec.points)

def _reached_row_border(landscape, bugspec, x_offset):
    return landscape.width == bugspec.width + x_offset
