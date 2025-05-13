import header

def create_frame(self, i, posi, orien):
    frame = header.gsd.hoomd.Frame()
    frame.configuration.step = i
    frame.particles.N = len(posi)
    frame.particles.position = posi[:]
    if len(self.verts) != 0:
        frame.particles.orientation = orien[:]
    frame.configuration.box = [self.uc_box.Lx, self.uc_box.Ly, self.uc_box.Lz, self.uc_box.xy,  self.uc_box.Ly, self.uc_box.Lz]
    return frame


def save_uc_func(self):
    options = header.QFileDialog.Options()
    options |= header.QFileDialog.DontUseNativeDialog
    fileName, _ = header.QFileDialog.getSaveFileName(self, 
        "Save File", "", "Image Files(*.png);;GSD Files(*.gsd);;All Files(*)", options = options)

    split_tup = header.os.path.splitext(self.fileName_traj)
    file_extension = split_tup[1]

    if -1 not in self.particles_arr:
        colors_arr = [header.matplotlib.colors.to_hex(self.c, keep_alpha=False) for _ in range(len(self.particle_arr_positions))] # single color
        color_arr = []
        for i in range(len(self.particle_arr_positions)):
            hex_colr = colors_arr[i]
            rgba_color = header.matplotlib.colors.to_rgba(hex_colr)
            color_arr.append(rgba_color)
    else:
        real_colors_arr = [header.matplotlib.colors.to_hex(self.c, keep_alpha=False) for _ in range(len(self.real_particles_positions))] # single color
        real_color_arr = []
        for i in range(len(self.real_particles_positions)):
            hex_colr = real_colors_arr[i]
            rgba_color = header.matplotlib.colors.to_rgba(hex_colr)
            real_color_arr.append(rgba_color)

        imag_colors_arr = ["#ff0000" for _ in range(len(self.imag_particles_positions))] # single color
        imag_color_arr = []
        for i in range(len(self.imag_particles_positions)):
            hex_colr = imag_colors_arr[i]
            rgba_color = header.matplotlib.colors.to_rgba(hex_colr)
            imag_color_arr.append(rgba_color)

    #****************************************************************************************
    if len(self.verts) != 0:
        if -1 not in self.particles_arr:
            modified_orientations = []
            for i in range(len(self.particles_orientations)):
                mat_form = header.rowan.to_matrix(header.np.array(self.particles_orientations[i]), require_unit=False)
                mat = header.np.matmul(header.np.linalg.inv(self.R), mat_form)
                modified_orientations.append(header.rowan.from_matrix(mat, require_orthogonal=False))

            modified_orientations = header.np.array(modified_orientations)
        else:
            # Real and imag particles modified orientations
            modified_real_orientations = []
            for i in range(len(self.real_particles_orientations)):
                mat_form = header.rowan.to_matrix(header.np.array(self.real_particles_orientations[i]), require_unit=False)
                mat = header.np.matmul(header.np.linalg.inv(self.R), mat_form)
                modified_real_orientations.append(header.rowan.from_matrix(mat, require_orthogonal=False))

            modified_real_orientations = header.np.array(modified_real_orientations)

            modified_imag_orientations = []
            for i in range(len(self.imag_particles_orientations)):
                mat_form = header.rowan.to_matrix(header.np.array(self.imag_particles_orientations[i]), require_unit=False)
                mat = header.np.matmul(header.np.linalg.inv(self.R), mat_form)
                modified_imag_orientations.append(header.rowan.from_matrix(mat, require_orthogonal=False))

            modified_imag_orientations = header.np.array(modified_imag_orientations)

    #****************************************************************************************
    # Now rotate the particles in the UC local frame ---> Might be non-orthogonal rotation
    if -1 not in self.particles_arr:
        all_modified_positions = []
        for i in range(len(self.particle_arr_positions)):
            all_modified_positions.append(header.np.matmul(header.np.linalg.inv(self.R), header.np.array(self.particle_arr_positions[i])))

        all_modified_positions = header.np.array(all_modified_positions)
    else:
        all_modified_positions = []
        for i in range(len(self.particle_arr_positions)):
            all_modified_positions.append(header.np.matmul(header.np.linalg.inv(self.R), header.np.array(self.particle_arr_positions[i])))

        all_modified_positions = header.np.array(all_modified_positions)
        
        # Real and imag particles modified positions
        modified_real_positions = []
        for i in range(len(self.real_particles_positions)):
            modified_real_positions.append(header.np.matmul(header.np.linalg.inv(self.R), header.np.array(self.real_particles_positions[i])))

        modified_real_positions = header.np.array(modified_real_positions)

        modified_imag_positions = []
        for i in range(len(self.imag_particles_positions)):
            modified_imag_positions.append(header.np.matmul(header.np.linalg.inv(self.R), header.np.array(self.imag_particles_positions[i])))

        modified_imag_positions = header.np.array(modified_imag_positions)

    if file_extension == ".png":
        # alpha, beta, gamma = 0, header.np.deg2rad(10), header.np.deg2rad(10)
        # q = header.rowan.normalize(header.rowan.from_euler(alpha, beta, gamma, convention='zyx'))

        # User input to get the orientationa of the configuration for saving image file. Euler's angle in degree
        alpha = float(input("Enter alpha : "))
        beta = float(input("Enter beta : "))
        gamma = float(input("Enter gamma : "))
        q = header.rowan.normalize(header.rowan.from_euler(header.np.deg2rad(alpha), header.np.deg2rad(beta), header.np.deg2rad(gamma), convention='zyx'))
        self.q = q

        if len(self.verts) != 0:
            if -1 not in self.particles_arr:
                all_rotated_positions = [header.rowan.rotate(q, t) for t in all_modified_positions]
                all_rotated_orientations = [header.rowan.multiply(q, t) for t in modified_orientations]
            else:
                all_rotated_positions = [header.rowan.rotate(q, t) for t in all_modified_positions]
                rotated_real_positions = [header.rowan.rotate(q, t) for t in modified_real_positions]
                rotated_real_orientations = [header.rowan.multiply(q, t) for t in modified_real_orientations]
                rotated_imag_positions = [header.rowan.rotate(q, t) for t in modified_imag_positions]
                rotated_imag_orientations = [header.rowan.multiply(q, t) for t in modified_imag_orientations]

        else:
            if -1 not in self.particles_arr:
                all_rotated_positions = [header.rowan.rotate(q, t) for t in all_modified_positions]
            else:
                all_rotated_positions = [header.rowan.rotate(q, t) for t in all_modified_positions]
                rotated_real_positions = [header.rowan.rotate(q, t) for t in modified_real_positions]
                rotated_imag_positions = [header.rowan.rotate(q, t) for t in modified_imag_positions]

        mean_rotated_positions = header.np.mean(header.np.array(all_rotated_positions), axis=0)
        if -1 not in self.particles_arr:
            all_rotated_positions = [(header.np.array(t)-mean_rotated_positions) for t in all_rotated_positions]
        else:
            rotated_real_positions = [(header.np.array(t)-mean_rotated_positions) for t in rotated_real_positions]
            rotated_imag_positions = [(header.np.array(t)-mean_rotated_positions) for t in rotated_imag_positions]

        '''all_rotated_positions = self.particle_arr_positions[:]
        all_rotated_orientations = self.particles_orientations[:]
        rotated_real_positions, rotated_real_orientations = self.real_particles_positions[:], self.real_particles_orientations[:]
        rotated_imag_positions, rotated_imag_orientations = self.imag_particles_positions[:], self.imag_particles_orientations[:]'''

        if -1 not in self.particles_arr:
            if len(self.verts) != 0:
                poly_info = header.draw1.ConvexPolyhedra(colors=color_arr, positions=all_rotated_positions, orientations=all_rotated_orientations, outline=0.01, vertices=self.verts, primitive_color_mix=0, roughness = 0.1, specular = 1.0, spec_trans=0.1)
            else:
                poly_info = header.draw1.Spheres(colors=color_arr, positions=all_rotated_positions, radii=self.sphereRadius)
        else:
            if len(self.verts) != 0:
                real_poly_info = header.draw1.ConvexPolyhedra(colors=real_color_arr, positions=rotated_real_positions, orientations=rotated_real_orientations, outline=0.01, vertices=self.verts, primitive_color_mix=0, roughness = 0.1, specular = 1.0, spec_trans=0.1)
                imag_poly_info = header.draw1.ConvexPolyhedra(colors=imag_color_arr, positions=rotated_imag_positions, orientations=rotated_imag_orientations, outline=0.01, vertices=self.verts, primitive_color_mix=0, roughness = 0.1, specular = 1.0, spec_trans=0.1)
            else:
                real_poly_info = header.draw1.Spheres(colors=real_color_arr, positions=rotated_real_positions, radii=self.sphereRadius)
                imag_poly_info = header.draw1.Spheres(colors=imag_color_arr, positions=rotated_imag_positions, radii=self.sphereRadius)

        edges = [[3, 4], [1, 4], [0, 1], [0, 3], [4, 7], [6, 7], [1, 6], [2, 6], [2, 5], [5, 7], [0, 2], [3, 5]]
        box_info = []
        if -1 not in self.particles_arr:
            box_info.append(poly_info)
        else:
            box_info.append(real_poly_info)
            box_info.append(imag_poly_info)
        uc_verts = all_rotated_positions[:8]
        starting_coord = [uc_verts[t[0]] for t in edges]
        ending_coord = [uc_verts[t[1]] for t in edges]
        box_primitive_real = header.draw1.Box(start_points=starting_coord, end_points=ending_coord, widths=0.05, colors=[0, 0, 0, 1], width=0.05, color=[0, 0, 0, 1], box_radius=.03)
        box_info.append(box_primitive_real)

        self.figsize = 15
        self.samples = 32

        total_info = tuple(box_info)
        scene = header.draw1.Scene(total_info, size=(self.figsize, self.figsize), pixel_scale=100)
        scene.enable("ambient_light", 1.5)
        scene.enable("directional_light", header.rowan.rotate(self.quat, [1, 0, 0]))
        scene.enable("antialiasing", 1.0)
        scene.enable("pathtracer", samples=self.samples)
        scene.save(fileName + '.png')

    elif file_extension == ".gsd":
        if len(self.verts) != 0:
            if -1 not in self.particles_arr:
                posi = all_modified_positions[:]
                orien = modified_orientations[:]
            else:
                posi, orien = [], []
                for i in range(len(modified_real_positions)):
                    posi.append(modified_real_positions[i])
                    orien.append(modified_real_orientations[i])
                
                for i in range(len(modified_imag_positions)):
                    posi.append(modified_imag_positions[i])
                    orien.append(modified_imag_orientations[i])


            f= header.gsd.hoomd.open(name=fileName +'.gsd', mode='w')
            f.extend(self, create_frame(0, posi, orien))

        else:
            if -1 not in self.particles_arr:
                posi = all_modified_positions[:]
                orien = []
            else:
                posi, orien = [], []
                for i in range(len(modified_real_positions)):
                    posi.append(modified_real_positions[i])
                
                for i in range(len(modified_imag_positions)):
                    posi.append(modified_imag_positions[i])

            f= header.gsd.hoomd.open(name=fileName +'.gsd', mode='w')
            f.append(create_frame(self, 0, posi, orien))