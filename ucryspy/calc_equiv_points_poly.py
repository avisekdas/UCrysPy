# INPUTS : only vertices of the polyhedron, from the centroids of the clusters detected by K-means clustering

import header
from calc_normal import calc_normal_func
import detect_pg_regular_body
import convexpolyhedron_from_geo3d

def calc_equiv_points_poly_func(self, vertices, faces, edges):
    """ Calculates the symmetry axes and angles of Point group elements using face mid-points and edge mid-points of the constructed polyhedron using the vertices
    i.e. centroid of the clouds of BOD

    Checks the satisfied crystal class of the Bravais structure based on the symmetry elements

    Parameters
    ----------
    vertices: list ([Num_vertices X 3])
            Vertices of the polyhedron to be constructed
    
    faces: list
        2D-list containing the vertices ids for each face
    
    edges: list
        2D-list containing the vertices ids for each edge


    Returns
    -------
    symm_arr : list ([Num_C6, Num_C4, Num_C3, Num_C2])

    vertices_direc_arr: list ([Num_vertices X 3])
                        Positional vector joining center of geometry of the polyhedron and each of the vertices
    
    faces_direc_arr: list ([Num_faces X 3])
                        Positional vector joining center of geometry of the polyhedron and each of the faces
    
    edges_direc_arr: list ([Num_edges X 3])
                        Positional vector joining center of geometry of the polyhedron and each of the edges

    ty: str
        CUBIC/HEXAGONAL/TETRAGONAL/RHOMBOHEDRAL/ORTHORHOMBIC/MONOCLINIC/TRICILINIC
    
    """
    # Center of the polyhedron
    center = header.np.mean(header.np.array([vertices[i] for i in range(len(vertices))]), axis=0).tolist()
    # print(vertices)
    # Joining vectors from center to vertices
    vertices_direc_arr = []
    for i in range(len(vertices)):
        vv = header.np.array(vertices[i]) - header.np.array(center)
        vertices_direc_arr.append(vv.tolist())

    # Face mid-points
    faces_direc_arr = []
    for i in range(len(faces)):
        vertice_arr = [vertices[faces[i][j]] for j in range(len(faces[i]))]
        face_midpt = header.np.mean(header.np.array(vertice_arr), axis=0)
        vv = face_midpt - header.np.array(center)
        vv = face_midpt[:]
        faces_direc_arr.append(vv.tolist())

    # Nomral to the faces from the center
    '''center_to_face_normal = []
    # faces_direc_arr = []
    for i in range(len(faces)):
        polygon_vertices = [header.np.array(vertices[faces[i][j]]) for j in range(len(faces[i]))]
        points = polygon_vertices[:]
        # print(polygon_vertices[:])
        if len(points) >= 3:
            n_unit = calc_normal_func(points)
            p_vec = vertices[faces[i][0]]
            d = -p_vec[0]*n_unit[0] - p_vec[1]*n_unit[1] - p_vec[2]*n_unit[2]
            dist_to_plane = header.np.dot(header.np.array(n_unit), header.np.array(center)) + d
            pt = header.np.array(center) - dist_to_plane*header.np.array(n_unit)
            center_to_face_normal.append(pt.tolist())

    for i in range(len(center_to_face_normal)):
        vv = header.np.array(center_to_face_normal[i])
        faces_direc_arr.append(vv.tolist())'''

    # Calculate the edges mid point
    edges_arr = []
    for e in range(len(list(edges))):
        edges_arr.append(list(list(edges)[e]))

    edge_midpt_arr = [header.np.mean(header.np.array([vertices[edges_arr[i][j]] for j in range(len(edges_arr[i]))]), axis=0) for i in range(len(edges_arr))]
    edges_len = [header.np.linalg.norm(header.np.array(vertices[edges_arr[i][0]]) - header.np.array(vertices[edges_arr[i][1]])) for i in range(len(edges_arr))]
    # print(edges_len)
    edges_direc_arr = []
    for i in range(len(edge_midpt_arr)):
        vv = header.np.array(edge_midpt_arr[i]) - header.np.array(center)
        edges_direc_arr.append(vv.tolist())

    mod_positions_all, symm_positions_all = [], []
    #*******************************************************************
    # Local neighbor symmetry, tried once, but didn't impelent. Will be considered for further studies
    # Calculating the symmetric axes (intersection by Geometry3D)
    # vertices_set, invariant_quantity, symm_axes = detect_pg_regular_body.calc_pg(self, vertices, len(edges), len(faces))
    # print("Number of symmetry of local environment : ", len(invariant_quantity))

    '''cph0 = convexpolyhedron_from_geo3d.convexpolyhedron_from_geo3d_func(vertices, edges, faces)
    posi = []
    all_posi = []
    # intersection of polyhedron and all symmetric axes
    for axis in symm_axes:
        vec = header.Vector(axis[0], axis[1], axis[2])
        s = header.Line(header.Point(0, 0, 0), vec)
        cpg = header.intersection(cph0,s)
        if type(cpg[0]) is float:
            all_posi.append([cpg[0], cpg[1], cpg[2]])
        else:
            all_posi.append([cpg[0][0], cpg[0][1], cpg[0][2]])
            all_posi.append([cpg[1][0], cpg[1][1], cpg[1][2]])

    posi = [i for i in all_posi if i != [0, 0, 0]]
    # symmetric axes
    for p in posi:
        symm_positions_all.append(p)'''
    #******************************************************************
    vertices_set, invariant_quantity, symm_axes = detect_pg_regular_body.calc_pg(self, vertices, len(edges), len(faces))
    # print("Number of symmetry of local environment : ", invariant_quantity)
    t0 = -1
    serial_arr = {'TRICLINIC':1, 'MONOCLINIC':2, 'ORTHORHOMBIC':4, 'RHOMBOHEDRAL':6, 'TETRAGONAL':8, 'HEXAGONAL':12, 'CUBIC':24}
    class_key, class_values = list(serial_arr.keys()), list(serial_arr.values())

    angle_arr = [60.0, 90.0, 120.0, 180.0]
    symm_arr = [self.occur_values[[i for i, e in enumerate(self.angles_values) if e == t][0]] for t in angle_arr]
    symm_arr[-1] =int(symm_arr[-1]/2)
    print(symm_arr)

    if symm_arr == [0, 6, 8, 9]:
        self.ty = 'CUBIC'
    elif symm_arr == [2, 0, 2, 7]:
        self.ty = 'HEXAGONAL'
    elif symm_arr == [0, 2, 0, 5]:
        self.ty = 'TETRAGONAL'
    elif symm_arr == [0, 0, 2, 3]:
        self.ty = 'RHOMBOHEDRAL'
    elif symm_arr == [0, 0, 0, 3]:
        self.ty = 'ORTHORHOMBIC'
    elif symm_arr == [0, 0, 0, 1]:
        self.ty = 'MONOCLINIC'
    elif symm_arr == [0, 0, 0, 0]:
        self.ty = 'TRICLINIC'
    else:
        self.ty = 'NONE'

    print("Detected crystal class is : ", self.ty)
    
    #******************************************************************

    for p in vertices_direc_arr:
        mod_positions_all.append(p)
        # print(p)

    for p in faces_direc_arr:
        mod_positions_all.append(p)
        # print(p)

    for p in edges_direc_arr:
        mod_positions_all.append(p)
        # print(p)

    #*******************************************************************
    # *sorted_mod_positions_all,=map(list,{*map(tuple,mod_positions_all)})
    # print("Equivalent points are calculated")
    # sorted_mod_positions_all = [list(x) for x in set(tuple(x) for x in mod_positions_all)]
    sorted_mod_positions_all = mod_positions_all[:]

    return sorted_mod_positions_all[:], vertices_direc_arr, faces_direc_arr, edges_direc_arr
