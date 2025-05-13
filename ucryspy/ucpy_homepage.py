import header
from pyvista_interface import pyvista_interface_func
from pyvista_sphere import pyvista_sphere_func
from gsd_reader import gsd_reader_func
from plot_config import plot_config_func

def upload_traj_func(self):
    self.fileName_traj, _ = header.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "","GSD Files (*.gsd)", options=header.QFileDialog.DontUseNativeDialog)
    if self.fileName_traj and self.file_upload_state == 0:
        split_tup = header.os.path.splitext(self.fileName_traj)
        file_extension = split_tup[1]
        if file_extension == ".gsd":   # Reads GSD file
            gsd_reader_func(self)

        if len(self.verts) != 0:
            pyvista_interface_func(self)  # for anisotropic polyhedra

        else:
            pyvista_sphere_func(self)   # for spheres; only positional info
    
        #******************************************
        self.file_upload_state = self.file_upload_state + 1

        self.avg_input, done1 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Average over frames? (y/n)') 
        if self.avg_input == "y":
            # Remove snapshot
            self.plotter.remove_actor(self.added_mesh) 
            self.plotter.remove_actor(self.sim_added_box)

            self.verts = [] # Make the particles sphere
            position_arr, orientation_arr, box_arr = [], [], []
            for t in range(self.frame_num-20, self.frame_num, 1):
                self.snap = self.traj[t]
                box_info = self.snap.configuration.box
                box = box_info
                box = [box[0], box[1], box[2], box[3], box[4], box[5]]

                positions = self.snap.particles.position
                if len(self.verts) != 0:
                    orientations = self.snap.particles.orientation
                    orientation_arr.append(orientations)

                position_arr.append(positions)
                box_arr.append(box)

            # Averaging positions and orientations over last few frames
            self.positions = header.np.average(header.np.array(position_arr), axis=0)
            '''f len(self.verts) != 0:
                self.orientations = header.np.average(header.np.array(orientation_arr), axis=0)'''
            self.box = header.np.average(header.np.array(box_arr), axis=0)
            self.box_arr = header.freud.box.Box(Lx=self.box[0], Ly=self.box[1], Lz=self.box[2],
                                xy=self.box[3], xz=self.box[4], yz=self.box[5], is2D=False)
            
            self.typeid = self.snap.particles.typeid
            self.original_typeid = self.typeid[:]
            self.original_positions = self.positions[:]
            self.diameter = self.snap.particles.diameter
            self.radii = self.diameter/2.0
            self.original_radii = self.radii[:]
            self.typeid_arr = self.snap.particles.types   # Types
            self.typeid_arr_int = self.snap.particles.typeid  # Typeid
            self.raw_typeid_arr_int = self.typeid_arr_int[:]
            self.typeid_arr_int = list(set(self.raw_typeid_arr_int))
            self.particle_typeid = list(set(self.typeid_arr))
            self.original_particleids = [i for i in range(len(self.original_positions))]
            self.particleids = self.original_particleids[:]

            '''if len(self.verts) != 0:
                self.original_orientations = self.orientations[:]
            else:
                self.orientations = header.np.array([[1, 0, 0, 0] for _ in range(len(self.original_positions))])
                self.original_orientations = self.orientations[:]'''


            self.orientations = header.np.array([[1, 0, 0, 0] for _ in range(len(self.original_positions))])
            self.original_orientations = self.orientations[:]

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

            self.added_mesh = self.plotter.add_points(self.positions, render_points_as_spheres=True, point_size=self.r, color=self.color_original[self.id], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
            self.plotter.reset_camera()
            light = header.pv.Light(color=self.c, light_type='headlight')
            # self.plotter.add_light(light)
            # self.plotter.add_camera_orientation_widget()
            self.plotter.update()

        else:
            pass

        def get_typeval(a):
            self.typeval = int(a.text())

        # Add type menu after loading gsd file
        for t in range(len(self.typeid_arr_int)):
            self.id_submenu = self.typeMenu.addMenu('Type ' + str(self.typeid_arr_int[t]))
            self.id_submenu.addAction(str(self.typeid_arr_int[t]))
            self.id_submenu.triggered[header.QAction].connect(get_typeval)

        self.go_action = header.QAction("&Go", self)
        self.go_action.triggered.connect(lambda:plot_config_func(self, self.typeval))
        self.typeMenu.addAction(self.go_action)

    else:
        if len(self.verts) != 0:
            pyvista_interface_func(self)  # for anisotropic polyhedra

        else:
            pyvista_sphere_func(self)   # for spheres; only positional info
        

def load_traj_func(self):
    # Check whether GSD or POS file is uploaded, based on it reader should be defined
    if self.file_upload_state == 0:
        if len(self.fileName_traj) >= 1:
            split_tup = header.os.path.splitext(self.fileName_traj)
            file_extension = split_tup[1]
            if file_extension == ".gsd":   # Reads GSD file
                gsd_reader_func(self)

            if len(self.verts) != 0:
                pyvista_interface_func(self)  # for anisotropic polyhedra

            else:
                pyvista_sphere_func(self)   # for spheres; only positional info
        
            #******************************************
            self.file_upload_state = self.file_upload_state + 1

            self.avg_input, done1 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Average over frames? (y/n)') 
            if self.avg_input == "y":
                # Remove snapshot
                self.plotter.remove_actor(self.added_mesh) 
                self.plotter.remove_actor(self.sim_added_box)

                self.verts = [] # Make the particles sphere
                position_arr, orientation_arr, box_arr = [], [], []
                for t in range(self.frame_num-20, self.frame_num, 1):
                    self.snap = self.traj[t]
                    box_info = self.snap.configuration.box
                    box = box_info
                    box = [box[0], box[1], box[2], box[3], box[4], box[5]]

                    positions = self.snap.particles.position
                    if len(self.verts) != 0:
                        orientations = self.snap.particles.orientation
                        orientation_arr.append(orientations)

                    position_arr.append(positions)
                    box_arr.append(box)

                # Averaging positions and orientations over last few frames
                self.positions = header.np.average(header.np.array(position_arr), axis=0)
                '''f len(self.verts) != 0:
                    self.orientations = header.np.average(header.np.array(orientation_arr), axis=0)'''
                self.box = header.np.average(header.np.array(box_arr), axis=0)
                self.box_arr = header.freud.box.Box(Lx=self.box[0], Ly=self.box[1], Lz=self.box[2],
                                    xy=self.box[3], xz=self.box[4], yz=self.box[5], is2D=False)
                
                self.typeid = self.snap.particles.typeid
                self.original_typeid = self.typeid[:]
                self.original_positions = self.positions[:]
                self.diameter = self.snap.particles.diameter
                self.radii = self.diameter/2.0
                self.original_radii = self.radii[:]
                self.typeid_arr = self.snap.particles.types   # Types
                self.typeid_arr_int = self.snap.particles.typeid  # Typeid
                self.raw_typeid_arr_int = self.typeid_arr_int[:]
                self.typeid_arr_int = list(set(self.raw_typeid_arr_int))
                self.particle_typeid = list(set(self.typeid_arr))
                self.original_particleids = [i for i in range(len(self.original_positions))]
                self.particleids = self.original_particleids[:]

                '''if len(self.verts) != 0:
                    self.original_orientations = self.orientations[:]
                else:
                    self.orientations = header.np.array([[1, 0, 0, 0] for _ in range(len(self.original_positions))])
                    self.original_orientations = self.orientations[:]'''


                self.orientations = header.np.array([[1, 0, 0, 0] for _ in range(len(self.original_positions))])
                self.original_orientations = self.orientations[:]

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

                self.added_mesh = self.plotter.add_points(self.positions, render_points_as_spheres=True, point_size=self.r, color=self.color_original[self.id], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                self.plotter.reset_camera()
                light = header.pv.Light(color=self.c, light_type='headlight')
                # self.plotter.add_light(light)
                # self.plotter.add_camera_orientation_widget()
                self.plotter.update()

            else:
                pass

            def get_typeval(a):
                self.typeval = int(a.text())

            # Add type menu after loading gsd file
            for t in range(len(self.typeid_arr_int)):
                self.id_submenu = self.typeMenu.addMenu('Type ' + str(self.typeid_arr_int[t]))
                self.id_submenu.addAction(str(self.typeid_arr_int[t]))
                self.id_submenu.triggered[header.QAction].connect(get_typeval)

        self.go_action = header.QAction("&Go", self)
        self.go_action.triggered.connect(lambda:plot_config_func(self, self.typeval))
        self.typeMenu.addAction(self.go_action)

    else:
        if len(self.verts) != 0:
            pyvista_interface_func(self)  # for anisotropic polyhedra

        else:
            pyvista_sphere_func(self)   # for spheres; only positional info