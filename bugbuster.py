# ideas: 
# - function to find array in array? cant deal with stuff between legs i think
# - regex? hard to generate? could it even match?
# 
# added complexity:
# - rotation
# - different look(s)
# - partially covered bugs
# - bugs next to each other

class Point:
    """A single point in a bug spec."""

    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
    
