# Separete the environemnt in case the initial system is non-Bravais. 
# For the Bravais lattice, the system will be intact.

# INPUTS :  all the system coordinates and the number of clusters possible in BOD within the fixed distance

# OUTPUTS :  seprate the environment based on the cluster ids

import header

def env_separation_func(self):
    self.comp, done3 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Bravais/Non-bravaias (b/nb)?') 

    # Type "s" if you think that the chosen system is Bravais depending on the percentage value.
    # Tpe "c" in case of of a non-Bravais lattice depending on the percentage
    # For ideal Bravis lattice, the percentage will be 100%
    # This depends on the user considering the noise present in the sytem
    if self.comp == "nb":  # separate the environemnt by choosing the points based on the identical cluster ids
        self.positions = header.np.array([self.positions[t] for t in self.chosen_particle_arr])
        self.orientations = header.np.array([self.orientations[t] for t in self.chosen_particle_arr])
        self.particleids = [self.particleids[t] for t in self.chosen_particle_arr]
        if len(self.verts) != 0:
            self.verts = [self.verts[t] for t in self.chosen_particle_arr]

        # self.radii = header.np.array([self.radii[t] for t in self.chosen_particle_arr])
        # self.typeid = header.np.array([self.typeid[t] for t in self.chosen_particle_arr])

        from ucpy_homepage import load_traj_func
        from save_config import save_config_func

        # Removing the previous calculated analyses, RDF, BOD and K-means
        # Remove the previous kmeans
        self.grid.removeWidget(self.canvas_kmeans)
        self.ax_kmeans.remove()
        self.canvas_kmeans.deleteLater()

        # Remove the previous bod
        self.grid.removeWidget(self.canvas_bod)
        self.ax_bod.remove()
        self.canvas_bod.deleteLater()
        
        # Remove the previous rdf
        self.grid.removeWidget(self.canvas_rdf)
        self.ax_rdf.remove()
        self.canvas_rdf.deleteLater()
        

        # Remove snapshot
        for p in self.added_mesh_arr:
            self.plotter.remove_actor(p) 

        self.plotter.remove_actor(self.sim_added_box)

        # Object for initializing RDF
        self.figure_rdf = header.Figure(figsize=(self.w, self.h))
        self.canvas_rdf = header.FigureCanvasQTAgg(self.figure_rdf)
        self.canvas_rdf.draw()

        # Object for bond order diagram (BOD)
        self.figure_bod = header.Figure(figsize=(self.w, self.h))
        self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)
        self.canvas_bod.draw()

        # Object for k-means clustering
        self.figure_kmeans = header.Figure(figsize=(self.w, self.h))
        self.canvas_kmeans = header.FigureCanvasQTAgg(self.figure_kmeans)
        self.canvas_kmeans.draw()

        # Object for 1D RDF, not implemented
        '''self.figure_onedrdf = header.Figure()
        self.canvas_onedrdf = header.FigureCanvasQTAgg(self.figure_onedrdf)
        self.canvas_onedrdf.draw()'''

        # Define the position of 'UCPy' logo for the image axes
        '''self.figure_onedrdf = header.Figure(figsize=(self.w, self.h))
        self.ax_image = self.figure_onedrdf.add_subplot(111)
        
        image = header.Image.open(self.image) # Open the image
        image_array = header.np.array(image)

        # Display the image
        self.ax_image.imshow(image_array)
        self.ax_image.axis('off')  # Remove axis of the image
        
        self.canvas_onedrdf = header.FigureCanvasQTAgg(self.figure_onedrdf)
        self.canvas_onedrdf.draw()'''

        # Add the widgets
        self.grid.addWidget(self.canvas_kmeans, 1, 0)
        self.grid.addWidget(self.canvas_bod, 2, 0)
        self.grid.addWidget(self.canvas_rdf, 3, 0)
        self.hlayout.addLayout(self.grid, 20)

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
        self.added_mesh_arr = []
        # In case of the polyhedra
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
                self.added_mesh = self.plotter.add_mesh(self.ungrid, show_edges=True, line_width=1, color=self.color_arr[self.id], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                self.added_mesh_arr.append(self.added_mesh)

            if len(neg_return) > 0:
                self.spehere_posi = [self.positions[t1] for t1 in neg_return]
                self.spehere_radius = [self.verts[t1] for t1 in neg_return]

                self.added_mesh = self.plotter.add_points(self.spehere_posi, render_points_as_spheres=True, point_size=self.color_arr[self.id], color=header.pv.Color('0x3ba099'), lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                self.added_mesh_arr.append(self.added_mesh)

        else:  # Spheres with positions only
            self.added_mesh = self.plotter.add_points(self.positions, render_points_as_spheres=True, point_size=self.r, color=self.c, lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
            self.added_mesh_arr.append(self.added_mesh)
        #******************************************

        self.plotter.reset_camera()
        light = header.pv.Light(color=self.c, light_type='headlight')
        # self.plotter.add_light(light)
        # self.plotter.add_camera_orientation_widget()
        self.plotter.update()
        self.rdf_state = 0
        if self.env_sep_iteration == 0:
            self.lattice_type = 'nonbravais'

        self.env_sep_iteration = self.env_sep_iteration + 1

        print("******************ENVIRONMENT HAS BEEN SEPARATED. PLEASE RE-CALCULATE RDF, BOD, K-Means and  'ENVIRONMENT SEPARATION' again to check for the Bravais lattice *********************")

        #******************************************************************************
        # RDF remained open

        # Deactivate BOD menu
        self.bodMenu.clear()
        # Deactivate K-Means menu
        self.kmeansMenu.clear()
        # Deactivate Env detection menu
        self.envdecMenu.clear()
        # Deactivate Env separation menu
        self.envsepMenu.clear()

        # Activate File menu partially
        self.save_menu = self.fileMenu.addMenu('Save configure')
        self.save_sphere_params = self.save_menu.addMenu('Sphere')
        #********************* Save as speheres *****************************************
        # self.c = '#bb2e1b' # Separated particles color
        # Sphere radius --> Save
        def get_SphereRadius(a):
            self.sphereRadius = float(a.text())

        self.save_sphere_params_radius = self.save_sphere_params.addMenu('radius')
        radius_arr = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        for r in radius_arr:
                self.save_sphere_params_radius.addAction(str(r))
        self.save_sphere_params_radius.triggered[header.QAction].connect(get_SphereRadius)

        # Sphere figsize --> Save
        def get_figsize(a):
            self.figsize = int(a.text())

        self.save_sphere_params_figsize = self.save_sphere_params.addMenu('Fig size')
        figsize_arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for r in figsize_arr:
                self.save_sphere_params_figsize.addAction(str(r))
        self.save_sphere_params_figsize.triggered[header.QAction].connect(get_figsize)

        # Sphere samples --> Save
        def get_samples(a):
            self.samples = int(a.text())

        self.save_sphere_params_samples = self.save_sphere_params.addMenu('Samples')
        samples_arr = [ 32, 64, 128, 256, 512]
        for r in samples_arr:
                self.save_sphere_params_samples.addAction(str(r))
        self.save_sphere_params_samples.triggered[header.QAction].connect(get_samples)

        #********************* Save as mesh *****************************************
        self.save_mesh_params = self.save_menu.addMenu('Mesh')
        # Mesh figsize --> Save
        def get_figsize(a):
            self.figsize = int(a.text())

        self.save_mesh_params_figsize = self.save_mesh_params.addMenu('Fig size')
        figsize_arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for r in figsize_arr:
                self.save_mesh_params_figsize.addAction(str(r))
        self.save_mesh_params_figsize.triggered[header.QAction].connect(get_figsize)

        # Mesh samples --> Save
        def get_samples(a):
            self.samples = int(a.text())

        self.save_mesh_params_samples = self.save_mesh_params.addMenu('Samples')
        samples_arr = [ 32, 64, 128, 256, 512]
        for r in samples_arr:
                self.save_mesh_params_samples.addAction(str(r))
        self.save_mesh_params_samples.triggered[header.QAction].connect(get_samples)

        #****************************************************************************

        save_action = header.QAction("&Save", self)
        save_action.triggered.connect(lambda:save_config_func(self))
        self.fileMenu.addAction(save_action)

        self.rdf_satisfied = 0
        self.bod_satisfied = 0
        self.kmeans_satisfied = 0

        self.comp = "t"
    
    elif self.comp == "b":
        from crys_class import crys_class_func

        orig_posi = [t.tolist() for t in self.original_positions]
        self.chosen_particle_arr = [[g for g, e in enumerate(orig_posi) if e == self.positions[t].tolist()][0] for t in range(len(self.positions))]

        # Deactivate RDF menu
        self.rdfMenu.clear()
        # Deactivate BOD menu
        self.bodMenu.clear()
        # Deactivate K-Means menu
        self.kmeansMenu.clear()
        if self.env_sep_iteration == 0:
            self.lattice_type = 'b'

        self.counter = 0

        #**************************************************************
        # Remove the previous bod
        self.grid.removeWidget(self.canvas_bod)
        self.ax_bod.remove()
        self.canvas_bod.deleteLater()

        # Replot BOD with cluster centers only
        self.figure_bod = header.Figure(figsize=(2.5, 2))
        self.ax_bod = self.figure_bod.add_subplot(projection="3d")
        self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)

        self.r_data = header.np.array(self.cluster_centers)
        x, y, z = self.r_data[:,0], self.r_data[:,1], self.r_data[:,2]

        # Scatter plot in 3D
        self.ax_bod.scatter(x, y, z, c='r', s=7.0)
        self.ax_bod.set_axis_off()
        self.ax_bod.set_box_aspect((self.rcut, self.rcut, self.rcut), zoom=1.3)
        self.figure_bod.tight_layout()
        self.canvas_bod.draw()

        self.ax_bod.set_title("BOD", fontsize=6)
        self.grid.addWidget(self.canvas_bod, 2, 0)
        #**************************************************************

        if self.enable_tol_func == False:
            # Activate classMenu 
            def get_elbow(a):
                self.elbow = int(a.text())

            self.elbow_submenu = self.classMenu.addMenu('elbow')

            c = 0
            start, end, width = self.data["elbow_min"], self.data["elbow_max"], self.data["elbow_count"]   # Change the limit if necessary
            num = (end - start)/width
            per_submenu = 20
            num_submenu = int(num/per_submenu) + 1
            g = 1
            c_end = 0
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                elbow_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.elbow_subsubmenu = self.elbow_submenu.addMenu(str(int(c_start)) + " - " + str(int(elbow_arr[-1])))
                for r in elbow_arr:
                    self.elbow_subsubmenu.addAction(str(int(r)))
                self.elbow_subsubmenu.triggered[header.QAction].connect(get_elbow)


            self.go_action = header.QAction("&Go", self)
            self.go_action.triggered.connect(lambda:crys_class_func(self))
            self.classMenu.addAction(self.go_action)