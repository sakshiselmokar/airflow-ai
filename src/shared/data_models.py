class Shape:
    def __init__(self, shape_type, center, meaning="process"):
        self.type = shape_type
        self.center = center
        self.meaning = meaning

        # 🔥 NEW
        self.text = ""
        self.bbox = None    


class Connection:
    def __init__(self, from_shape, to_shape):
        self.from_shape = from_shape
        self.to_shape = to_shape


    def __repr__(self):
        return f"{self.from_shape.type} -> {self.to_shape.type}"    


class Node:
    def __init__(self, id, type, position):
        self.id = id
        self.type = type
        self.position = position


class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node   