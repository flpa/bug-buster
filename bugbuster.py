class Point(object): #TODO naming
    """A single point in a bug specification, consisting of x/y coordinates \
    and a value 'val'."""

    def __init__(self, x, y, val):
        self.val = val
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overridden equality check comparing class and attributes."""
        return (isinstance(other, self.__class__) and self.val == other.val
                and self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        """Overriden not-equals method for consistency with __eq__."""
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.val) + hash(self.x) + hash(self.y)

    def __repr__(self):
        return "%s(%s/%s)" % (self.val, self.x, self.y)

class BugSpec(object):
    """Represents a bug specification and holds width, height and the points \
    the bug consists of."""

    def __init__(self, width, height, points):
        self.width = width
        self.height = height
        self.points = points

class Landscape(object):
    """A class representing a landscape to be scanned for bugs. It consists \
    of a collection of rows of equal length, and holds information about the \
    total width and height."""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []
        self._interjacent_empty_rows = []

    def add_row(self, row):
        if row:
            assert not self._interjacent_empty_rows, "There have been empty \
rows since the last content row. This is currently not supported."
            
            self._set_or_verify_width(row)
            self._add_row(row)
        elif self.rows:
            self._interjacent_empty_rows.append(row)
        
    def _set_or_verify_width(self, row):
        row_length = len(row)
        if self.width == 0:
            self.width = row_length
        else:
            assert self.width == row_length, \
                "Row length %s differs from width %s, this is currently not \
supported" % (row_length, self.width)
            
    def _add_row(self,row):
        self.rows.append(row)
        self.height += 1

# main part
        
def read_landscape(filepath):
    landscape = Landscape()
    for line in open(filepath, "r"):
        landscape.add_row(line.strip('\n'))
    return landscape

def _is_blank(char):
    """Determines whether a character is relevant for a bug specification.
    Currently we only ignore blanks (' ')."""
    return char != ' '

def read_bugspec(filepath, char_predicate=_is_blank):
    """Reads a bug specification from a file."""

    x = y = 0
    x_max = x_min = y_max = y_min = None
    points = []
    
    for char in open(filepath, "r").read():
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
    
    _adapt_coordinates(points, x_min, y_min)

    width = x_max - x_min + 1
    height = y_max - y_min + 1
        
    return BugSpec(width, height, set(points))

def _adapt_coordinates(points, x_min, y_min):
    # adapt coordinates to be relative to a rectangle only surrounding actual
    # bug points
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
    
    while landscape.width >= bugspec.width + x_offset and \
            landscape.height >= bugspec.height + y_offset:
        all_match = True
        for p in bugspec.points:
            if landscape.rows[y_offset + p.y][x_offset + p.x] != p.val:
                all_match = False
                break

        if all_match:
            bug_count += 1

        if landscape.width == bugspec.width + x_offset:
            x_offset = 0
            y_offset += 1
        else:
            x_offset += 1
    
    return bug_count


