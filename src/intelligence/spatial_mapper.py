def point_inside_bbox(point, bbox):
    px, py = point
    x, y, w, h = bbox
    return x <= px <= x + w and y <= py <= y + h


def map_text_to_shapes(text_points, shapes, recognized_text):
    """
    Assign recognized text to the correct shape
    based on actual spatial overlap (NOT nearest guess)
    """

    if not text_points or not shapes or not recognized_text:
        return

    for shape in shapes:
        if not shape.bbox:
            continue

        inside_count = 0

        for p in text_points:
            if point_inside_bbox(p, shape.bbox):
                inside_count += 1

        # 🔥 robust threshold (at least 30% points inside)
        if inside_count > 0.3 * len(text_points):
            if not shape.text:
                shape.text = ""

            shape.text += recognized_text
            print(f"✅ Mapped '{recognized_text}' → {shape.type}")
            return  # map to only one shape