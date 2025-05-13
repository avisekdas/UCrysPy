import header
import lattice_param

def create_frame(self, i, posi, orien, typeids):
    frame = header.gsd.hoomd.Frame()
    frame.configuration.step = i
    frame.particles.N = len(posi)
    frame.particles.position = posi[:]
    frame.particles.typeid = typeids[:]
    frame.particles.types = self.particle_typeid[:]
    # shape_arr = []
    if len(self.unique_type_shapes) != 0:
        frame.particles.orientation = orien[:]
        frame.particles.type_shapes = self.unique_type_shapes[:]

    else:
        frame.particles.type_shapes = self.unique_type_shapes[:]

    frame.configuration.box = [self.uc_box.Lx, self.uc_box.Ly, self.uc_box.Lz, self.uc_box.xy,  self.uc_box.xz, self.uc_box.yz]
    return frame

def save_basis_func(self):
    options = header.QFileDialog.Options()
    options |= header.QFileDialog.DontUseNativeDialog
    fileName, _ = header.QFileDialog.getSaveFileName(self, 
        "Save File", "", "GSD Files(*.gsd);;Image Files(*.png);;All Files(*)", options = options)

    split_tup = header.os.path.splitext(self.fileName_traj)
    file_extension = split_tup[1]

    colors_arr = [header.matplotlib.colors.to_hex(self.color_original[0], keep_alpha=False) for _ in range(len(self.particle_types))] # single color
    color_arr = []
    for i in range(len(self.particle_types)):
        hex_colr = colors_arr[i]
        rgba_color = header.matplotlib.colors.to_rgba(hex_colr)
        color_arr.append(rgba_color)

    # Effective particle positions with respect to box center with respect to global frame
    id_arr = [[i for i, e in enumerate(self.all_uc_positions_wrt_center) if [round(float(e[0]), 3), round(float(e[1]), 3), round(float(e[2]), 3)] == [round(float(t[0]), 3), round(float(t[1]), 3), round(float(t[2]), 3)]][0] for t in (self.original_basis_positions)]
    # print(id_arr)
    if len(self.verts) != 0:
        basis_particles_orientations = [self.particles_orientations[t] for t in id_arr] # Get orientations of non-equivalent particles in the UC

        # Orientations in local frame of UC
        modified_orientations = []
        for i in range(len(basis_particles_orientations)):
            mat_form = header.rowan.to_matrix(header.np.array(basis_particles_orientations[i]), require_unit=False)
            mat = header.np.matmul(header.np.linalg.inv(self.R), mat_form)
            modified_orientations.append(header.rowan.from_matrix(mat, require_orthogonal=False))

    # Corner particle positions in the UC local frame
    box_center = header.np.average(header.np.array(self.all_uc_positions_wrt_center[:8]), axis=0)
    self.all_uc_positions_wrt_center = [(header.np.array(t)-box_center) for t in self.all_uc_positions_wrt_center]
    modified_positions_corner = []
    for i in range(len(self.all_uc_positions_wrt_center[:8])):
        modified_positions_corner.append(header.np.matmul(header.np.linalg.inv(self.R), header.np.array((self.all_uc_positions_wrt_center[i]))))

    modified_positions_corner = header.np.array(modified_positions_corner)

    modified_basis_positions = []
    for i in range(len(self.original_basis_positions)):
        modified_basis_positions.append(header.np.matmul(header.np.linalg.inv(self.R), header.np.array((self.original_basis_positions[i]))))

    modified_basis_positions = header.np.array(modified_basis_positions)

    # alpha, beta, gamma = 0, header.np.deg2rad(10), header.np.deg2rad(10)
    # q = header.rowan.normalize(header.rowan.from_euler(alpha, beta, gamma, convention='zyx'))

    # User input to get the orientationa of the configuration for saving image file. Euler's angle in degree
    '''alpha = float(input("Enter alpha : "))
    beta = float(input("Enter beta : "))
    gamma = float(input("Enter gamma : "))
    q = header.rowan.normalize(header.rowan.from_euler(header.np.deg2rad(alpha), header.np.deg2rad(beta), header.np.deg2rad(gamma), convention='zyx'))'''
    

    # Rotate corner particle positions by an unit quaternion for visualisation 
    # q  = self.q
    q = [1, 0, 0, 0]
    rotated_positions_corner = [header.rowan.rotate(q, t) for t in modified_positions_corner]
    rotated_basis_positions = [header.rowan.rotate(q, t) for t in modified_basis_positions]

    #**************************************************************
    if len(self.verts) != 0:
        rotated_orientations = [header.rowan.multiply(q, t) for t in modified_orientations]  # # Rotate corner particle orientations by an unit quaternion for visualisation

    edges = [[3, 4], [1, 4], [0, 1], [0, 3], [4, 7], [6, 7], [1, 6], [2, 6], [2, 5], [5, 7], [0, 2], [3, 5]]
    uc_verts = rotated_positions_corner[:]
    starting_coord = [uc_verts[t[0]] for t in edges]
    ending_coord = [uc_verts[t[1]] for t in edges]

    rotated_lattice_vec = [header.np.matmul(header.np.linalg.inv(self.R), t) for t in self.lattice_vec_raw]
    modified_lattice_vec = [header.rowan.rotate(q, t) for t in rotated_lattice_vec]
    a = lattice_param.lattice_param_func(modified_lattice_vec)
    # print(a[0], a[1], a[2], a[3], a[4], a[5])
    self.uc_box = header.freud.box.Box.from_box_lengths_and_angles(L1=a[0], L2=a[1], L3=a[2], alpha=header.np.deg2rad(a[3]), beta=header.np.deg2rad(a[4]), gamma=header.np.deg2rad(a[5]), dimensions=3)
    
    if file_extension == ".png":
        if len(self.verts) != 0:
            poly_info = header.draw1.ConvexPolyhedra(colors=color_arr, positions=rotated_basis_positions, orientations=rotated_orientations, outline=0.01, vertices=self.verts, primitive_color_mix=0, roughness = 0.1, specular = 1.0, spec_trans=0.1)
        else:
            poly_info = header.draw1.Spheres(colors=color_arr, positions=rotated_basis_positions, radii=self.sphereRadius)

        box_info = []
        box_info.append(poly_info)
        box_primitive_real = header.draw1.Box(start_points=starting_coord, end_points=ending_coord, widths=0.05, colors=[0, 0, 0, 1], width=0.05, color=[0, 0, 0, 1], box_radius=.03)
        box_info.append(box_primitive_real)
        total_info = tuple(box_info)
        scene = header.draw1.Scene(total_info, size=(self.figsize, self.figsize), pixel_scale=100)
        scene.enable("ambient_light", 1.5)
        scene.enable("directional_light", header.rowan.rotate(self.quat, [1, 0, 0]))
        scene.enable("antialiasing", 1.0)
        scene.enable("pathtracer", samples=self.samples)
        scene.save(fileName + '.png')

    elif file_extension == ".gsd":
        '''uc_boxVec = [(uc_verts[t]-uc_verts[0]) for t in range(1, 4)]
        uc_boxMatrix = header.np.transpose(header.np.array(uc_boxVec))
        self.uc_box = header.freud.box.Box.from_matrix(uc_boxMatrix, dimensions=3)
        print(self.uc_box)'''
        if len(self.verts) != 0:
            f = header.gsd.hoomd.open(name=fileName + '.gsd', mode='w')
            uc_particles_typeids = [self.original_typeid[g] for g in self.basis_id]
            uc_typeid_category = [[g for g, e in enumerate(uc_particles_typeids) if e == k] for k in self.typeid_arr_int]
            uc_particles_category = [[self.basis_id[m] for m in k] for k in uc_typeid_category]
            f.append(create_frame(self, 0, rotated_basis_positions, rotated_orientations, uc_particles_typeids))
        else:
            rotated_orientations = []
            f = header.gsd.hoomd.open(name=fileName + '.gsd', mode='w')
            uc_particles_typeids = [self.original_typeid[g] for g in self.basis_id]
            uc_typeid_category = [[g for g, e in enumerate(uc_particles_typeids) if e == k] for k in self.typeid_arr_int]
            uc_particles_category = [[self.basis_id[m] for m in k] for k in uc_typeid_category]
            f.append(create_frame(self, 0, rotated_basis_positions, rotated_orientations, uc_particles_typeids))