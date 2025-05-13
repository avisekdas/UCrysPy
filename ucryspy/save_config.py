import header

def save_config_func(self):
    options = header.QFileDialog.Options()
    options |= header.QFileDialog.DontUseNativeDialog
    fileName, _ = header.QFileDialog.getSaveFileName(self, 
        "Save File", "", "Image Files(*.png);;All Files(*)", options = options)

    # alpha, beta, gamma = 0, header.np.deg2rad(10), header.np.deg2rad(10)
    # q = header.rowan.normalize(header.rowan.from_euler(alpha, beta, gamma, convention='zyx'))

    # User input to get the orientationa of the configuration for saving image file. Euler's angle in degree
    print("Enter euler angles (alpha, beta, gamma) to save the configuration in particular orientation")
    alpha, beta, gamma = float(input("Enter alpha : ")), float(input("Enter beta : ")), float(input("Enter gamma : "))
    self.quat = header.rowan.normalize(header.rowan.from_euler(header.np.deg2rad(alpha), header.np.deg2rad(beta), header.np.deg2rad(gamma), convention='zyx'))

    num_particles = len(self.positions)
    colors_arr = [header.matplotlib.colors.to_hex(self.hex_colors[0], keep_alpha=False) for _ in range(num_particles)]
    # Render using Fresnel
    color_arr = []
    for i in range(len(self.positions)):
        hex_colr = colors_arr[i]
        rgba_color = header.matplotlib.colors.to_rgba(hex_colr)
        color_arr.append(rgba_color)

    if len(self.verts) != 0:
        poly_info = header.draw1.ConvexPolyhedra(colors=color_arr, positions=self.positions, orientations=self.orientations, outline=0.01, vertices=self.verts, primitive_color_mix=0, roughness = 0.1, specular = 1.0, spec_trans=0.1)
    else:
        poly_info = header.draw1.Spheres(colors=color_arr, positions=self.positions, radii=self.sphereRadius)

    box_primitive = header.draw1.Box(Lx=self.box[0], Ly=self.box[1], Lz=self.box[2], xy=self.box[3], xz=self.box[4], yz=self.box[5], widths=0.3, colors=[0, 0, 0, 1], width=0.1, color=[0, 0, 0, 1])
    
    # High quality image
    '''scene = header.draw1.Scene((poly_info, box_primitive), rotation=q, size=(70, 70),  pixel_scale=100)
    scene.enable("ambient_light", 1.5)
    scene.enable("directional_light", [-1.5, 0, 0])
    scene.enable("antialiasing", 1.0)
    scene.enable("pathtracer", samples=128)
    scene.save(fileName + '.png')'''

    # Standard quality image
    scene = header.draw1.Scene((poly_info, box_primitive), rotation=self.quat, size=(self.figsize, self.figsize),  pixel_scale=50)
    scene.enable("ambient_light", 1.5)
    scene.enable("directional_light", header.rowan.rotate(self.quat, [1, 0, 0]))
    scene.enable("antialiasing", 1.0)
    scene.enable("pathtracer", samples=self.samples)
    scene.save(fileName + '.png')