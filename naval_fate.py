class Position():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def move_ship(name, position, speed):
    print("moving", name,
          "to", "(%d,%d)" % (position.x, position.y),
          "at", speed, "knots")
