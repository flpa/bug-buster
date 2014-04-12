"""bugbuster.py: Main file of bugbuster."""

from model import *
        
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

def read_bugspec(filepath, char_predicate=_is_not_blank):
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
