"""bugbuster.py: Main file of bugbuster."""

import codecs
from model import *
        
def read_landscape(filepath):
    """Creates a Landscape by parsing the given file."""
    landscape = Landscape()

    f = codecs.open(filepath, "r", "utf-8")
    try:
        for line in f:
            line_content = line.strip('\n').strip('\r')
            landscape.add_row(line_content)
    finally:
        # using the 'with' statement would look way better but requires 2.5+
        f.close()
    return landscape

def _is_not_blank(char):
    """Determines whether a character is not equal to ' '."""
    return char != ' '

def read_bugspec(filepath, char_predicate=_is_not_blank):
    """Reads a bug specification from a file.

    Keyword arguments:
    char_predicate -- the predicate function that decides whether a character
    is relevant for the bug specification (default: is_blank)
    """
    x = y = x_max = y_max = 0
    # init with infinity -> anything is smaller
    x_min = y_min = float('inf')
    points = []

    f = codecs.open(filepath, "r", "utf-8")
    try:
        for char in f.read():
            if char == '\r':
                continue
            if char == '\n':
                y += 1
                x = 0
                continue

            if char_predicate(char):
                points.append(Point(x, y, char))
                x_max = max(x_max, x)
                x_min = min(x_min, x)
                y_max = max(y_max, y)
                y_min = min(y_min, y)

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

def count_bugs(bugfile, landscapefile):
    """Counts occurrences of a bug in a landscape and returns the result."""
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
    # 'all' is not available in Python 2.4
    for p in bugspec.points:
        if landscape.rows[y_offset + p.y][x_offset + p.x] != p.value:
            return False
    return True

def _reached_row_border(landscape, bugspec, x_offset):
    return landscape.width == bugspec.width + x_offset
