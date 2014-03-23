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

def read_bugspec(filepath):
    """Reads a bug specification from a file."""
#    spec =

def equalp(a,b):
    """Simple equality predicate, equivalent to 'a == b'."""
    # TODO Doesn't Python have this somewhere?
    return a == b
    
def array_matches_template(array, template, predicate=equalp):
    array_flat = flatten(array)
    template_flat = flatten(template)

    return [i for i,j in zip(array_flat, template_flat) if predicate(i,j)]

def flatten(iterable):
    """ A simplified function for flattening an iterable that works
    in our context (only one level of nested lists), because the
    proposed solutions covering general cases seem to rely on 2.6+
    functionality, e.g.:
    - http://docs.python.org/2/library/itertools.html#itertools.chain,
    - https://stackoverflow.com/a/2158532"""
    return [item for sublist in iterable for item in sublist]



