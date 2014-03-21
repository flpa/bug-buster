# ideas: 
# - function to find array in array? cant deal with stuff between legs i think
# - regex? hard to generate? could it even match?
# 
# added complexity:
# - rotation
# - different look(s)
# - partially covered bugs
# - bugs next to each other

class Point: #TODO naming
    """A single point in a bug spec."""

    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y

class BugSpec:
    """Specification of a bug."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = []

    def add_point(self, point):
        self.points.append(point)
    
