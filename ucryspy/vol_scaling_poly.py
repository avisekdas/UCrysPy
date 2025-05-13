import header

def vol_scaling_poly_func(shape_vertices_basic, upcoming_particle_volume, particle_volume):
    dim = 3
    inverse_dim = 1.0/float(dim)
    upcoming_shape_vertices = []
    for i in range(len(shape_vertices_basic)):
        upcoming_shape_vertices.append([])

    for i in range(0, len(shape_vertices_basic)):
        for j in range(0, len(shape_vertices_basic[i])):
            upcoming_shape_vertices[i].append((shape_vertices_basic[i][j]) * header.np.power((upcoming_particle_volume/particle_volume), inverse_dim))

    return upcoming_shape_vertices