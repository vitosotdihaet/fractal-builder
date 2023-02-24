import math

def calc_vector_length(vec):
    return math.sqrt(vec[0]**2 + vec[1]**2)

def calc_cos(v1, v2, l1, l2):
    return min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / (l1 * l2))

def calc_sin(y, cos):
    sin = math.sqrt(1 - cos**2)
    if y < 0: return sin
    return -sin