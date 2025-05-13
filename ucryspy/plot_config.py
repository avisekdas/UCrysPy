import header

def plot_config_func(self, id):
    self.id = id
    '''indices = [i for i, e in enumerate(self.raw_typeid_arr_int) if e == id]
    self.positions = header.np.array([self.positions[t] for t in indices])
    self.orientations = header.np.array([self.orientations[t] for t in indices])'''

    self.c = self.color_arr[self.id]
    self.positions, self.orientations, self.particleids = self.cat_positions[id], self.cat_orientations[id], self.cat_particleids[id]
    if len(self.verts) != 0:    
        self.verts = self.cat_verts[id]


    # Remove snapshot
    for p in self.added_mesh_arr:
        self.plotter.remove_actor(p) 
    self.plotter.remove_actor(self.sim_added_box)

    # Box info
    box_matrix = self.box_arr.to_matrix()
    b1, b2, b3 = box_matrix[:,0], box_matrix[:,1], box_matrix[:,2]
    # print(b1, b2, b3)

    # Box vertices
    boxvert1 = (-b1/2.0) + (-b2/2.0) + (-b3/2.0)
    boxvert2 = (-b1/2.0) + (b2/2.0) + (-b3/2.0)
    boxvert3 = (b1/2.0) + (-b2/2.0) + (-b3/2.0)
    boxvert4 = (b1/2.0) + (b2/2.0) + (-b3/2.0)
    boxvert5 = (-b1/2.0) + (-b2/2.0) + (b3/2.0)
    boxvert6 = (-b1/2.0) + (b2/2.0) + (b3/2.0)
    boxvert7 = (b1/2.0) + (-b2/2.0) + (b3/2.0)
    boxvert8 = (b1/2.0) + (b2/2.0) + (b3/2.0)

    box_points = header.np.array([boxvert1, boxvert3, boxvert2, boxvert5, boxvert7, boxvert6, boxvert4, boxvert8])
    # print(box_points)
    box_faces = [[0, 1, 4, 3], [1, 6, 7, 4], [6, 2, 5, 7], [2, 0, 3, 5], [0, 1, 6, 2], [3, 4, 7, 5]]
    modified_box_faces = []
    for b in box_faces:
        modified_box_faces.append(len(b))
        for a in b:
            modified_box_faces.append(a)

    self.box_mesh = header.pv.PolyData(box_points, modified_box_faces)
    visibleEdges = self.box_mesh.extract_feature_edges()
    self.sim_added_box = self.plotter.add_mesh(visibleEdges, color='k', line_width=5)
    #*****************************************************************
    # In case of the polyhedra
    self.added_mesh_arr = []
    if len(self.verts) != 0: # Polyhedra
        self.v_arr = []
        self.poly_verts, self.spehere_posi, self.spehere_radius, self.part_types = [], [], [], []
        return_list = [isinstance(self.verts[t1], list) for t1 in range(len(self.orientations))]
        posi_return, neg_return = [t for t in range(len(return_list)) if return_list[t] == True], [t for t in range(len(return_list)) if return_list[t] == False]
        if len(posi_return) > 0:
            self.v_arr = [[(header.np.array(self.positions[t1]) + header.rowan.rotate(self.orientations[t1], self.verts[t1][t2]).tolist()) for t2 in range(len(self.verts[t1]))] for t1 in posi_return]
            self.poly_verts = [self.verts[t1] for t1 in posi_return]
            self.part_types = [self.verts[t1] for t1 in posi_return]
            points = list(header.chain.from_iterable(self.v_arr))
            poly = header.coxeter.shapes.ConvexPolyhedron(self.poly_verts[0])
            faces = poly.faces
            all_faces = [[(faces[u]+t*len(self.v_arr[t])) for u in range(len(faces))] for t in range(len(self.v_arr))]
            polyhedron_connectivity = [[*[[len(all_faces[t][u]), *all_faces[t][u]] for u in range(len(all_faces[t]))]] for t in range(len(all_faces))]
            polyhedron_connectivity = [list(header.chain.from_iterable(polyhedron_connectivity[t])) for t in range(len(polyhedron_connectivity))] 
            polyhedron_connectivity = [[len(faces), *polyhedron_connectivity[t]] for t in range(len(polyhedron_connectivity))]
            polyhedron_connectivity = [[len(polyhedron_connectivity[t]), *polyhedron_connectivity[t]] for t in range(len(polyhedron_connectivity))]
            polyhedron_connectivity = list(header.chain.from_iterable(polyhedron_connectivity))
            
            # Creating unstructured grid from pyvista
            cells = polyhedron_connectivity[:]
            celltypes = [header.pv.CellType.POLYHEDRON for _ in range(len(self.v_arr))]
            print(len(polyhedron_connectivity), len(celltypes), len(points))
            self.ungrid = header.pv.UnstructuredGrid(cells, celltypes, points)
            self.added_mesh = self.plotter.add_mesh(self.ungrid, show_edges=True, line_width=1, color=self.c, lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
            self.added_mesh_arr.append(self.added_mesh)

        if len(neg_return) > 0:
            self.spehere_posi = [self.positions[t1] for t1 in neg_return]
            self.spehere_radius = [self.verts[t1] for t1 in neg_return]

            self.added_mesh = self.plotter.add_points(self.spehere_posi, render_points_as_spheres=True, point_size=self.spehere_radius[0], color=header.pv.Color('0x3ba099'), lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
            self.added_mesh_arr.append(self.added_mesh)

    else:  # Spheres with positions only
        self.added_mesh = self.plotter.add_points(self.positions, render_points_as_spheres=True, point_size=self.r, color=self.c, lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
        self.added_mesh_arr.append(self.added_mesh)

    self.plotter.add_camera_orientation_widget()
    # light = header.pv.Light(color=self.c, light_type='headlight')
    # self.plotter.add_light(light)
    self.plotter.reset_camera()
    self.plotter.update()