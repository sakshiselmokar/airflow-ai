def point_inside_bbox(point, bbox):
    px, py = point
    x, y, w, h = bbox

    return x <= px <= x + w and y <= py <= y + h


def map_text_to_shapes(text_points, shapes, recognized_text):
    for shape in shapes:
        for p in text_points:
            if point_inside_bbox(p, shape.bbox):
                shape.text = recognized_text
                print(f"Mapped text '{recognized_text}' to {shape.type}")
                break