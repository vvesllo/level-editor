
class Vec2:
    def __init__(self, x: any, y: any):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, number):
        return Vec2(self.x * number, self.y * number)
    
    def __truediv__(self, number):
        return Vec2(self.x / number, self.y / number)
    
    def __floordiv__(self, number):
        return Vec2(self.x // number, self.y // number)

    def __repr__(self) -> str:
        return f"Vec2<{self.x}, {self.y}>"

    def get(self):
        return (self.x, self.y)
    

def normalize(vector):
    return vector / (vector.x ** 2 + vector.y ** 2) ** 0.5
