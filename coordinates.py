class Coordinates:
    def __init__(self, x, y):
        self._x = x  # Use private attributes
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return isinstance(other, Coordinates) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Coordinates({self.x}, {self.y})"

    def is_adjacent(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1
    
# Test adjacency
coord1 = Coordinates(2, 3)
coord2 = Coordinates(2, 4)
assert coord1.is_adjacent(coord2)

# Test hashing (for sets/dicts)
coord_set = {coord1, coord2}
assert Coordinates(2, 3) in coord_set  # True    
