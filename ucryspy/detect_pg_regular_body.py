import header
import face_edge_from_vertex
from calc_normal import calc_normal_func

def calc_pg(self, vertices, num_edges, num_faces):
    edges, faces, vertices = face_edge_from_vertex.face_edge_from_vertex_func(vertices, num_edges, num_faces)

    tol = 4
    center = header.np.mean(header.np.array([vertices[i] for i in range(len(vertices))]), axis=0).tolist()
    # center = header.np.array([0, 0, 0])
    positions = []
    # Vertices
    for i in range(len(vertices)):
        vv = header.np.array(vertices[i]) - header.np.array(center)
        positions.append(vv.tolist())

    for i in range(len(faces)):
        vertice_arr = [vertices[faces[i][j]] for j in range(len(faces[i]))]
        face_midpt = header.np.mean(header.np.array(vertice_arr), axis=0)
        vv = face_midpt - header.np.array(center)
        positions.append(vv.tolist())

    # Center to face normal
    '''center_to_face_normal = []
    for i in range(len(faces)):
        polygon_vertices = [header.np.array(vertices[faces[i][j]]) for j in range(len(faces[i]))]
        n_cap = calc_normal_func(polygon_vertices)
        p_vec = vertices[faces[i][0]]
        d = -p_vec[0]*n_cap[0] - p_vec[1]*n_cap[1] - p_vec[2]*n_cap[2]
        dist_to_plane = header.np.dot(header.np.array(n_cap), header.np.array(center)) + d
        pt = header.np.array(center) - dist_to_plane*header.np.array(n_cap)
        center_to_face_normal.append(pt.tolist())

    for i in range(len(center_to_face_normal)):
        vv = header.np.array(center_to_face_normal[i])
        positions.append(vv.tolist())'''

    edges_arr = []
    for e in range(len(list(edges))):
        edges_arr.append(list(list(edges)[e]))

    # center to edges midpoint
    edge_midpt_arr = [header.np.mean(header.np.array([vertices[edges_arr[i][j]] for j in range(len(edges_arr[i]))]), axis=0) for i in range(len(edges_arr))]
    edges_len = [header.np.linalg.norm(header.np.array(vertices[edges_arr[i][0]]) - header.np.array(vertices[edges_arr[i][1]])) for i in range(len(edges_arr))]
    # print(edges_len)

    for i in range(len(edge_midpt_arr)):
        vv = header.np.array(edge_midpt_arr[i]) - header.np.array(center)
        positions.append(vv.tolist())

    #****************************************************************************
    '''angle_arr = [header.np.rad2deg(header.np.arccos(round(header.np.dot(i/header.np.linalg.norm(i), j/header.np.linalg.norm(j)), 3))) for i in positions for  j in positions]
    angle_arr = [round(t, 4) for t in angle_arr if round(t, 2) != 0]
    original_angle_arr = angle_arr[:]
    angle_arr.sort()
    self.tolerance = round(angle_arr[0] * 0.95, 4) 
    print(self.tolerance)'''
    #****************************************************************************

    mod_positions_all = [header.np.array(positions[i]).tolist() for i in range(len(positions))]
    '''rot_arr = [header.np.deg2rad(180), header.np.deg2rad(120), header.np.deg2rad(240), header.np.deg2rad(90), header.np.deg2rad(270),
        header.np.deg2rad(72), header.np.deg2rad(144), header.np.deg2rad(216), header.np.deg2rad(288), header.np.deg2rad(60),
        header.np.deg2rad(300),header.np.deg2rad(45), header.np.deg2rad(135), header.np.deg2rad(225), header.np.deg2rad(315), header.np.deg2rad(252), header.np.deg2rad(324),
        header.np.deg2rad(36), header.np.deg2rad(108), header.np.deg2rad(-120), header.np.deg2rad(-240), header.np.deg2rad(-90), header.np.deg2rad(-270),
        header.np.deg2rad(-72), header.np.deg2rad(-144), header.np.deg2rad(-216), header.np.deg2rad(-288), header.np.deg2rad(-60),
        header.np.deg2rad(-300),header.np.deg2rad(-45), header.np.deg2rad(-135), header.np.deg2rad(-225), header.np.deg2rad(-315),
        header.np.deg2rad(-36), header.np.deg2rad(-108), header.np.deg2rad(-252), header.np.deg2rad(-324)]'''
    
    rot_arr = [header.np.deg2rad(180), header.np.deg2rad(120), header.np.deg2rad(90), header.np.deg2rad(60)]

    ref_vertices = vertices[:]
    ref_vertices_rounded = []
    for i in range(len(vertices)):
        ref_vertices_rounded.append(header.np.array(ref_vertices[i]).tolist())

    final_q_arr, mod_positions_sym = [], []
    Arr = []
    dic_data = {}
    for t in rot_arr:
        dic_data[round(header.np.rad2deg(t),0)] = []

    for i in range(len(positions)):
        vecvec = positions[i]
        unit_vec = positions[i]/header.np.linalg.norm(positions[i])
        for j in range(len(rot_arr)):
            q = header.rowan.normalize(header.rowan.from_axis_angle(unit_vec, rot_arr[j]))
            q_rounded = [round(m, tol) for m in q]  # rounding off to 4 decimal places
            count = 0
            for k in range(len(ref_vertices)):
                vec = header.rowan.rotate(q, ref_vertices[k])
                vec_rounded = vec.tolist()
                for t in range(len(ref_vertices_rounded)):
                    a = header.np.isclose(vec_rounded, ref_vertices_rounded[t], atol=self.rtol)
                    a_true = [t for t in a if t==True]
                    '''if len(a_true) == len(vec_rounded):
                        count = count + 1
                        break'''
                    if header.np.linalg.norm(vec_rounded) != 0 and header.np.linalg.norm(ref_vertices_rounded[t]) != 0:
                        angle = header.np.rad2deg(header.np.arccos(round(header.np.dot(vec_rounded/header.np.linalg.norm(vec_rounded), ref_vertices_rounded[t]/header.np.linalg.norm(ref_vertices_rounded[t])), tol)))
                        if angle <= self.tolerance:
                            count = count + 1
                            break

            if count == len(ref_vertices) and q_rounded not in final_q_arr:
                # print(q_rounded, header.np.round(unit_vec, 4), round(header.np.rad2deg(rot_arr[j]), 2))
                dic_data[round(header.np.rad2deg(rot_arr[j]),0)].append(header.np.array(vecvec).tolist()) 
                Arr.append(header.math.gcd(360, int(round(header.np.rad2deg(rot_arr[j]), tol))))
                final_q_arr.append(q_rounded)
                mod_positions_sym.append(header.np.array(vecvec).tolist())

    # Removing duplicate 1d list from 2d list
    # *sorted_mod_positions_sym,=map(list,{*map(tuple,mod_positions_sym)})
    # *sorted_quat_arr,=map(list,{*map(tuple,final_q_arr)})

    sorted_mod_positions_sym = mod_positions_sym[:]
    sorted_quat_arr = final_q_arr[:]

    invariant_quantity = []
    for i in final_q_arr:
        invariant_quantity.append(i)

    invariant_quantity.append([1, 0, 0, 0])
    # invariant_quantity.append([-1, 0, 0, 0])
    nonsymm_axes = []
    for v in positions:
        if v not in sorted_mod_positions_sym:
            nonsymm_axes.append(header.np.array(v).tolist())

    #*********************************************************************
    # Rot symmetry 
    self.angles_values, self.occur_values = list(dic_data.keys()), list(dic_data.values())
    self.occur_values = [len(t) for t in self.occur_values]
    # print(self.angles_values, self.occur_values)
    #*********************************************************************

    '''if len(sorted_mod_positions_sym) > 0:
        symm_sorted_posi = [sorted_mod_positions_sym[0]]
        for i in range(1, len(sorted_mod_positions_sym)):
            count = 0
            for j in range(len(symm_sorted_posi)):
                angle = header.np.rad2deg(header.np.arccos(round(header.np.dot(sorted_mod_positions_sym[i]/header.np.linalg.norm(sorted_mod_positions_sym[i]), symm_sorted_posi[j]/header.np.linalg.norm(symm_sorted_posi[j])), 4)))
                if self.angle_cutoff < angle < (180-self.angle_cutoff):
                    count = count + 1

            if count == len(symm_sorted_posi):
                if sorted_mod_positions_sym[i] not in symm_sorted_posi:
                    symm_sorted_posi.append(sorted_mod_positions_sym[i])

        symm_axes = symm_sorted_posi[:]
        # print(len(symm_axes), symm_axes)

    else:
        symm_axes = []'''
    
    symm_axes = sorted_mod_positions_sym[:]
    #*********************************************************
    fve_points = positions[:]
    # Proper rotation
    vertices_set = []
    for i in range(len(final_q_arr)):
        vertices_set.append(header.rowan.rotate(final_q_arr[i], vertices))

    # proper reflection
    '''for i in range(len(fve_points)):
        n_cap = fve_points[i]
        n_cap = n_cap/header.header.np.linalg.norm(n_cap)
        d = -center[0]*n_cap[0] - center[1]*n_cap[1] - center[2]*n_cap[2]
        reflected_vertices = []
        for k in range(len(vertices)):
            pt = vertices[k]
            t = (d-n_cap[0]*pt[0]-n_cap[1]*pt[1]-n_cap[2]*pt[2])/(n_cap[0]*n_cap[0]+n_cap[1]*n_cap[1]+n_cap[2]*n_cap[2])
            v = [(pt[0]+2*t*n_cap[0]), (pt[1]+2*t*n_cap[1]), pt[2]+2*t*n_cap[2]]
            reflected_vertices.append(header.header.np.array(v))

        reflected_vertices = header.header.np.array(reflected_vertices)
        reflected_vertices_rounded = reflected_vertices.tolist()
        count = 0
        for k in range(len(reflected_vertices_rounded)):
            vec_rounded = reflected_vertices_rounded[k]
            if vec_rounded in ref_vertices_rounded:
                    count = count + 1
            else:
                break

        if count == len(ref_vertices):
            vertices_set.append(reflected_vertices)
            invariant_quantity.append(n_cap)

    # print(len(vertices_set))
    # Proper rotation + reflection
    rot_ref_axis, rot_ref_angle = [], []
    for i in range(len(fve_points)):
        vecvec = fve_points[i]
        unit_vec = fve_points[i]/header.np.linalg.norm(fve_points[i])
        for j in range(len(rot_arr)):
            q = rowan.normalize(rowan.from_axis_angle(unit_vec, rot_arr[j]))
            rotated_vertices_arr = []
            for k in range(len(ref_vertices)):
                vec = rowan.rotate(q, ref_vertices[k])
                rotated_vertices_arr.append(vec)
            
            n_cap = unit_vec[:]
            d = -center[0]*n_cap[0] - center[1]*n_cap[1] - center[2]*n_cap[2]
            rotated_vertices_reflected = []
            for k in range(len(rotated_vertices_arr)):
                pt = rotated_vertices_arr[k]
                t = (d-n_cap[0]*pt[0]-n_cap[1]*pt[1]-n_cap[2]*pt[2])/(n_cap[0]*n_cap[0]+n_cap[1]*n_cap[1]+n_cap[2]*n_cap[2])
                v = [(pt[0]+2*t*n_cap[0]), (pt[1]+2*t*n_cap[1]), pt[2]+2*t*n_cap[2]]
                rotated_vertices_reflected.append(header.header.np.array(v))

            rotated_vertices_reflected = header.header.np.array(rotated_vertices_reflected)
            rotated_vertices_reflected_rounded = rotated_vertices_reflected.tolist()
            count = 0
            for k in range(len(rotated_vertices_reflected_rounded)):
                vec_rounded = rotated_vertices_reflected_rounded[k]
                if vec_rounded in ref_vertices_rounded:
                        count = count + 1
                else:
                    break

            if count == len(ref_vertices):
                vertices_set.append(rotated_vertices_reflected)
                invariant_quantity.append([q, n_cap])
                rot_ref_axis.append(unit_vec)
                if rot_arr[j] not in rot_ref_angle:
                    rot_ref_angle.append(rot_arr[j])

    # print(len(vertices_set))
    # (Proper rotation + reflection) ---> multiple times
    for i in range(len(fve_points)):
        vecvec = fve_points[i]
        unit_vec = fve_points[i]/header.np.linalg.norm(fve_points[i])
        for j in range(len(rot_ref_angle)):
            for t in range(3):
                q = rowan.normalize(rowan.from_axis_angle(unit_vec, rot_ref_angle[j]))
                rotated_vertices_arr = []
                for k in range(len(ref_vertices)):
                    vec = rowan.rotate(q, ref_vertices[k])
                    rotated_vertices_arr.append(vec)
                
                # Reflection
                n_cap = unit_vec[:]
                d = -center[0]*n_cap[0] - center[1]*n_cap[1] - center[2]*n_cap[2]
                rotated_vertices_reflected = []
                for k in range(len(rotated_vertices_arr)):
                    pt = rotated_vertices_arr[k]
                    t = (d-n_cap[0]*pt[0]-n_cap[1]*pt[1]-n_cap[2]*pt[2])/(n_cap[0]*n_cap[0]+n_cap[1]*n_cap[1]+n_cap[2]*n_cap[2])
                    v = [(pt[0]+2*t*n_cap[0]), (pt[1]+2*t*n_cap[1]), pt[2]+2*t*n_cap[2]]
                    rotated_vertices_reflected.append(header.header.np.array(v))

                ref_vertices = rotated_vertices_reflected[:]

            ref_vertices_ss = header.header.np.array(ref_vertices)
            ref_vertices_ss_rounded = ref_vertices_ss.tolist()
            count = 0
            for k in range(len(ref_vertices_ss_rounded)):
                vec_rounded = ref_vertices_ss_rounded[k]
                if vec_rounded in ref_vertices_rounded:
                    count = count + 1
                else:
                    break
            # print(len(ref_vertices), count)
            if count == len(ref_vertices_ss):
                vertices_set.append(ref_vertices_ss)
                # print(vecvec, header.header.np.rad2deg(rot_ref_angle[j]))

    # print(len(vertices_set))'''
    return vertices_set, invariant_quantity, symm_axes
