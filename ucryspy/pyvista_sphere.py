# Visualization of the spheres with only coordinates in 3D with the box using PyVista and PyQt5

import header
from frame_handle import frame_handle_func
from rdf import rdf_func
from save_rdf import save_rdf_func
from clear_rdf import clear_rdf_func

def pyvista_sphere_func(self):
    if self.file_upload_state == 0:
        # Box ifo
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
        self.cat_positions, self.cat_orientations, self.cat_particleids = [], [], []
        for t in self.typeid_arr_int:
            indices = [i for i, e in enumerate(self.raw_typeid_arr_int.tolist()) if e == t]
            self.typeid_positions = [self.positions[i] for i in indices]
            self.typeid_orientations = [self.orientations[i] for i in indices]
            self.cat_particleids.append(indices)
            self.cat_positions.append(header.np.array(self.typeid_positions))
            self.cat_orientations.append(header.np.array(self.typeid_orientations))

        self.added_mesh_arr = []
        for t in range(len(self.typeid_arr_int)):
            self.c = self.color_arr[0]
            self.added_mesh = self.plotter.add_points(self.positions, render_points_as_spheres=True, point_size=self.r, color=self.c, lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
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
        for t in range(len(self.typeid_arr_int)):
            self.added_mesh = self.plotter.add_points(self.cat_positions[t], render_points_as_spheres=True, point_size=self.r, color=self.color_original[t], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
            self.added_mesh_arr.append(self.added_mesh)

        self.plotter.reset_camera()
        self.plotter.update()

    frame_handle_func(self)

    #******************************************************************************
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