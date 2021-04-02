import math

def angle_score(landmarks):
    ret = []
    for points in landmarks:
        x1 = points[0][0]
        y1 = points[0][1]
        x4 = points[1][0]
        y4 = points[1][1]
        x_nose = points[2][0]
        y_nose = points[2][1]
        x3 = points[3][0]
        y3 = points[3][1]
        x2 = points[4][0]
        y2 = points[4][1]
        xi = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        yi = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        if abs(xi-x_nose)>20:
            if  x_nose -xi >20:
                ret.append("LEFT")
            elif xi - x_nose > 20:
                ret.append("RIGHT")
            else: ret.append("")
        else:
            if abs(yi - y_nose)>5:
                if  y_nose -yi >5:
                    ret.append("BOTTOM")
                elif yi - y_nose > 20:
                    ret.append("UP")
                else: ret.append("CENTER")
            else:
                ret.append("CENTER")
    return ret


def face_goodness_score(angle_score, box, confidence, cross_line, max_x=1920, max_y=1080):
    x1, y1, x2, y2 = box[:4]
    width = x2 - x1
    height = y2 - y1
    d = min(abs(x1), abs(max_x - x2)) / (width / 2.0)
    # dy = min(abs(y1), abs(max_y - y2)) / (height / 2.0)
    d = max(min(d, 1.0), 0.0)
    center_coeff = d ** 2
    aspect = height / width
    aspect_score = min(1.0, aspect / 1.1)
    aspect_score = max(0.5, aspect_score)
    score = angle_score * confidence * center_coeff * aspect_score
    score = max(0.0, score)
    score = min(1.0, score)
    score = score ** 0.2  # to prevent score from being too low
    # prefer face near the crossing line
    cy = (y1 + y2) / 2.0
    if cy < cross_line:
        crossing_score = 1 - (cross_line - cy) / cross_line
    else:
        crossing_score = 1 - (cy - cross_line) / (max_y - cross_line)
    crossing_score = 0.9 + 0.1 * crossing_score
    score *= crossing_score
    return score