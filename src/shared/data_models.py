class Shape:
    def __init__(self, shape_type, center):
        self.type = shape_type
        self.center = center

    def __repr__(self):
        return f"{self.type} at {self.center}"
    

class Connection:
    def __init__(self, from_shape, to_shape):
        self.from_shape = from_shape
        self.to_shape = to_shape

    def __repr__(self):
        return f"{self.from_shape.type} -> {self.to_shape.type}"    