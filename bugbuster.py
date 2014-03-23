class Point: #TODO naming
    """A single point in a bug spec."""

    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y

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
        landscape.add_row(line)
    return landscape
        
def read_bugspec(filepath):
    """Reads a bug specification from a file."""
#    spec =

def equalp(a,b):
    """Simple equality predicate, equivalent to 'a == b'."""
    # TODO Doesn't Python have this somewhere?
    return a == b
    



