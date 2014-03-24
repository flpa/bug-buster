class Point: #TODO naming
    """A single point in a bug spec."""

    def __init__(self, x, y, val):
        self.val = val
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overridden equality check comparing class and attributes."""
        return (isinstance(other, self.__class__) and self.val == other.val
                and self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        """Overriden not-equals method, see __eq__"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.val) + hash(self.x) + hash(self.y)

    def __repr__(self):
        return "%s(%s/%s)" % (self.val, self.x, self.y)

class BugSpec:
    """Specification of a bug."""

    def __init__(self, width, height, points):
        self.width = width
        self.height = height
        self.points = points

class Landscape:
    """Class representing a landscape"""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []

    def add_row(self, row):
        self._set_or_verify_width(row)
        self._add_row(row)
        
    def _set_or_verify_width(self, row):
        rowLength = len(row)
        if self.width == 0:
            self.width = rowLength
        else:
            assert self.width == rowLength, \
                "Row length %s differs from width %s, this is currently not \
supported" % (rowLength,self.width)
            
    def _add_row(self,row):
        self.rows.append(row)
        self.height += 1

def read_landscape(filepath):
    landscape = Landscape()
    for line in open(filepath, "r"):
        landscape.add_row(line.strip('\n'))
    return landscape

def read_bugspec(filepath):
    """Reads a bug specification from a file."""

    x = y = 0
    xMax = xMin = yMax = yMin = None
    points = []
    
    for char in open(filepath, "r").read():
        if char == '\n':
            y += 1
            x = 0
            continue

        if _is_relevant_char(char):
            points.append(Point(x, y, char))

            xMax = _get_higher(xMax, x)
            xMin = _get_lower(xMin, x)
            yMax = _get_higher(yMax, y)
            yMin = _get_lower(yMin, y)

        x += 1

    # adapt coordinates to be relative to a rectangle only surrounding actual
    # bug points
    if xMin | yMin:
        for p in points:
            p.x -= xMin
            p.y -= yMin

    width = xMax - xMin + 1
    height = yMax - yMin + 1
        
    return BugSpec(width, height, set(points))

def _is_relevant_char(char):
    """Determines whether a character is relevant for a bug specification.
    Currently we only ignore blanks (' ')."""
    return char != ' '

def _get_lower(old, new):
    if old is None or old > new:
        return new
    return old

def _get_higher(old, new):
    if old is None or old < new:
        return new
    return old


def equalp(a,b):
    """Simple equality predicate, equivalent to 'a == b'."""
    # TODO Doesn't Python have this somewhere?
    return a == b

def count_bugs(bugfile, landscapefile):
    bugspec = read_bugspec(bugfile)
    landscape = read_landscape(landscapefile)

    return 0
