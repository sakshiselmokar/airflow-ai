class Shape:
    def __init__(self, shape_type, center):
        self.type = shape_type
        self.center = center

    def __repr__(self):
        return f"{self.type} at {self.center}"