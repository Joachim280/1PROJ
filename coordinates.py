class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

if __name__ == "__main__":
    a = Coordinates(2, 3)
    b = Coordinates(2, 3)
    print(a == b)  # True
    print(a)       # (2, 3)
