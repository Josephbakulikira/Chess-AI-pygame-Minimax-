from setting import Config
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other == None:
            return False
        elif self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def Compare(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def GetCopy(self):
        return Position(self.x, self.y)

    def getTuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

def OnBoard(position):
    # checking if the position is not out of the playing board
    return (position.x >= 0 and position.x < 8) and (position.y >= 0 and position.y < 8)
