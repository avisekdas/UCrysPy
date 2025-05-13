# Visualization of the anisotropic polyhedra with the box using PyVista and PyQt5

import header
from frame_handle import frame_handle_func
from rdf import rdf_func
from save_rdf import save_rdf_func
from clear_rdf import clear_rdf_func

def pyvista_interface_func(self):
    if self.file_upload_state == 0:
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
        self.cat_positions, self.cat_orientations, self.cat_particleids, self.cat_verts = [], [], [], []
        for t in self.typeid_arr_int:
            indices = [i for i, e in enumerate(self.raw_typeid_arr_int.tolist()) if e == t]
            self.typeid_positions = [self.positions[i] for i in indices]
            self.typeid_orientations = [self.orientations[i] for i in indices]
            self.verts_cat = [self.verts[i] for i in indices]
            self.cat_verts.append(self.verts_cat)
            self.cat_particleids.append(indices)
            self.cat_positions.append(header.np.array(self.typeid_positions))
            self.cat_orientations.append(header.np.array(self.typeid_orientations))

        self.added_mesh_arr = []
        for a in range(len(self.typeid_arr_int)):
            self.v_arr = []
            self.poly_verts, self.spehere_posi, self.spehere_radius, self.part_types = [], [], [], []
            return_list = [isinstance(self.cat_verts[a][t1], list) for t1 in range(len(self.cat_orientations[a]))]
            posi_return, neg_return = [t for t in range(len(return_list)) if return_list[t] == True], [t for t in range(len(return_list)) if return_list[t] == False]
            if len(posi_return) > 0:
                self.v_arr = [[(header.np.array(self.cat_positions[a][t1]) + header.rowan.rotate(self.cat_orientations[a][t1], self.cat_verts[a][t1][t2]).tolist()) for t2 in range(len(self.cat_verts[a][t1]))] for t1 in posi_return]
                self.poly_verts = [self.cat_verts[a][t1] for t1 in posi_return]
                self.part_types = [self.cat_verts[a][t1] for t1 in posi_return]
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
                # print(len(polyhedron_connectivity), len(celltypes), len(points))
                self.ungrid = header.pv.UnstructuredGrid(cells, celltypes, points)
                self.added_mesh = self.plotter.add_mesh(self.ungrid, show_edges=True, line_width=1, color=self.color_arr[a], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                self.added_mesh_arr.append(self.added_mesh)

            if len(neg_return) > 0:
                self.spehere_posi = [self.cat_positions[a][t1] for t1 in neg_return]
                self.spehere_radius = [self.cat_verts[a][t1] for t1 in neg_return]

                self.added_mesh = self.plotter.add_points(self.spehere_posi, render_points_as_spheres=True, point_size=self.spehere_radius[0], color=header.pv.Color('0x3ba099'), lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                self.added_mesh_arr.append(self.added_mesh)

        self.plotter.reset_camera()
        # light = header.pv.Light(color=self.c, light_type='headlight')
        # self.plotter.add_light(light)
        self.plotter.add_camera_orientation_widget()
        self.plotter.update()

    else:
        # Remove snapshot
        for p in self.added_mesh_arr:
            self.plotter.remove_actor(p) 
        # Again add it
        self.cat_positions, self.cat_orientations, self.cat_particleids = [], [], []
        for t in self.typeid_arr_int:
            indices = [i for i, e in enumerate(self.raw_typeid_arr_int.tolist()) if e == t]
            self.typeid_positions = [self.positions[i] for i in indices]
            self.typeid_orientations = [self.orientations[i] for i in indices]
            self.cat_particleids.append(indices)
            self.cat_positions.append(header.np.array(self.typeid_positions))
            self.cat_orientations.append(header.np.array(self.typeid_orientations))

        self.added_mesh_arr = []
        for a in range(len(self.typeid_arr_int)):
            poly = header.coxeter.shapes.ConvexPolyhedron(self.verts)
            faces = poly.faces
            self.v_arr = [self.cat_positions[a][t1]+header.rowan.rotate(self.cat_orientations[a][t1], self.verts) for t1 in range(len(self.cat_orientations[a]))]
            points = list(header.chain.from_iterable(self.v_arr))
            polyhedron_connectivity = []
            num_particles = len(self.cat_orientations[a])
            for i in range(num_particles):
                sub_arr = []
                sub_arr.append(len(faces))
                for j in range(len(faces)):
                    sub_arr.append(len(faces[j]))
                    for k in range(len(faces[j])):
                        sub_arr.append(faces[j][k]+i*len(self.v_arr[i]))

                sub_arr = [len(sub_arr)] + sub_arr
                for s in sub_arr:
                    polyhedron_connectivity.append(s)
            
            # Creating unstructured grid from pyvista
            cells = polyhedron_connectivity[:]
            celltypes = [header.pv.CellType.POLYHEDRON for _ in range(num_particles)]
            self.ungrid = header.pv.UnstructuredGrid(cells, celltypes, points)

            self.added_mesh = self.plotter.add_mesh(self.ungrid, show_edges=True, line_width=1, color=self.color_original[t], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
            self.added_mesh_arr.append(self.added_mesh)

        self.plotter.reset_camera()
        self.plotter.update()

    frame_handle_func(self)

    # Activate RDF
    if self.counter == 0:
        def get_bins(a):
            self.bins = int(a.text())
            # print(self.bins)

        self.bins_submenu = self.rdfMenu.addMenu('Bins')
        # some  actions created manually
        bins_min, bins_max, bins_count = self.data["bins_min"], self.data["bins_max"], self.data["bins_count"]
        bins_list = [t for t in range(bins_min, bins_max, bins_count)]
        for t in bins_list:
            self.bins_submenu.addAction(str(t))

        self.bins_submenu.triggered[header.QAction].connect(get_bins)

        def get_rmax(a):
            self.rmax = float(a.text())
            # print(self.rmax)

        self.rmax_submenu = self.rdfMenu.addMenu('rmax')
        rmax_min, rmax_max, rmax_count = self.data["rmax_min"], self.data["rmax_max"], self.data["rmax_count"]
        rmax_list = [t for t in range(rmax_min, rmax_max, rmax_count)]
        for t in rmax_list:
            self.rmax_submenu.addAction(str(t))

        self.rmax_submenu.triggered[header.QAction].connect(get_rmax)

        self.go_action = header.QAction("&Go", self)
        self.go_action.triggered.connect(lambda:rdf_func(self))
        self.rdfMenu.addAction(self.go_action)

        self.save_action = header.QAction("&Save", self)
        self.save_action.triggered.connect(lambda:save_rdf_func(self))
        self.rdfMenu.addAction(self.save_action)

        self.clear_action = header.QAction("&Clear", self)
        self.clear_action.triggered.connect(lambda:clear_rdf_func(self))
        self.rdfMenu.addAction(self.clear_action)

        self.rdf_state = 0

    # It records the total number of back and forth of the plot, i.e. how many times this thing is being plotted
    self.counter = self.counter + 1
