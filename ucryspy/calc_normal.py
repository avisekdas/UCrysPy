import header

def calc_normal_func(points):
    a = header.np.array(points[1]) - header.np.array(points[0])
    b = header.np.array(points[2]) - header.np.array(points[0])
    n_cap = header.np.cross(a, b)
    n_unit = (n_cap/header.np.linalg.norm(n_cap))
    d = -n_unit[0]*points[0][0] - n_unit[1]*points[0][1] - n_unit[2]*points[0][2]

    return n_unit[:]