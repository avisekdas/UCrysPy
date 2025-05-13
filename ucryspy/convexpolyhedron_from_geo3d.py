import header

def convexpolyhedron_from_geo3d_func(vertices, edges, faces):
    # Vertices
    geo_vertices = []
    for v in vertices:
        geo_vertices.append(header.Point(v[0], v[1], v[2]))

    # faces
    polygon_arr = []
    for f in faces:
        geo_poly_arr = [geo_vertices[f[t]] for t in range(len(f))]
        polygon_arr.append(header.ConvexPolygon(tuple(geo_poly_arr)))

    cph0 = header.ConvexPolyhedron(tuple(polygon_arr))

    return cph0
