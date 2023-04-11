
class Vec2:
    def __init__(self, x: any, y: any):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vec2(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other):
        return Vec2(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other):
        return Vec2(self.x // other.x, self.y // other.y)

    def __repr__(self) -> str:
        return f"Vec2<{self.x}, {self.y}>"

    def get(self):
        return (self.x, self.y)
    
    @staticmethod
    def normalize(vector):
	    return vector / (vector.x ** 2 + vector.y ** 2) ** 0.5
