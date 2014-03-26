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
        self.interjacent_empty_rows = []

    def add_row(self, row):
        if row:
            assert len(self.interjacent_empty_rows) == 0, "There have been empty \
rows since the last content row. This is currently not supported."
            
            self._set_or_verify_width(row)
            self._add_row(row)
        elif self.rows:
            self.interjacent_empty_rows.append(row)
        
    def _set_or_verify_width(self, row):
        rowLength = len(row)
        if self.width == 0:
            self.width = rowLength
        else:
            assert self.width == rowLength, \
                "Row length %s differs from width %s, this is currently not \
supported" % (rowLength, self.width)
            
    def _add_row(self,row):
        self.rows.append(row)
        self.height += 1

# main part
        
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

def count_bugs(bugfile, landscapefile):
    bugspec = read_bugspec(bugfile)
    landscape = read_landscape(landscapefile)

    xOffset = 0
    yOffset = 0

    bugcounter = 0
    
    while landscape.width >= bugspec.width + xOffset and \
            landscape.height >= bugspec.height + yOffset:
        allMatch = True
        for p in bugspec.points:
            if landscape.rows[yOffset + p.y][xOffset + p.x] != p.val:
                allMatch = False
                break

        if allMatch:
            bugcounter += 1

        if landscape.width == bugspec.width + xOffset:
            xOffset = 0
            yOffset += 1
        else:
            xOffset += 1
    
    return bugcounter
