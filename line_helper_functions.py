def get_line(point1, point2):
    if point2[0] - point1[0] != 0:
        m = (point2[1] - point1[1]) / (point2[0] - point1[0])
        c = point1[1] - m * point1[0]
        return (m, c)
    else:
        return None