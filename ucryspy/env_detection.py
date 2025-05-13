import header
from env_separation import env_separation_func

def env_detection_func(self):
    # After the detection of elbow from the previous step
    self.n_clusters = self.elbow
    # Fitting the positions to the cluster
    self.model = header.KMeans(n_clusters=self.n_clusters, init='k-means++', n_init='auto', random_state=0)
    self.model.fit(self.position_arr)
    pred = self.model.fit_predict(self.position_arr)
    cluster_labels = pred
    # print(cluster_labels)
    centroid=self.model.cluster_centers_
    cluster_centers = centroid[:]
    self.cluster_centers = cluster_centers[:]
    inertia = self.model.inertia_
    self.labels =  self.model.labels_

    self.cluster_centers = header.np.array(cluster_centers)
    
    separation_arr_len = [len(t) for t in self.separation_arr]
    separataion_arr_flattened = list(header.chain.from_iterable(self.separation_arr))
    #*********************************************************************************
    # Suggested cutoffs
    avg_d_arr, avg_a_arr, var_arr = [], [], []
    for c in range(self.n_clusters):
        sorted_arr = [i for i, e in enumerate(self.labels) if e == c]
        sorted_separation_arr = header.np.array([separataion_arr_flattened[i] for i in sorted_arr])
        sorted_separation_arr_unit = [i/header.np.linalg.norm(i) for i in sorted_separation_arr]
        centroid = cluster_centers[c]
        centroid_normal = header.np.array(cluster_centers[c])/header.np.linalg.norm(header.np.array(cluster_centers[c]))
        dist_arr = [(sorted_separation_arr[i]-centroid) for i in range(len(sorted_separation_arr))]
        proj_r = [abs(header.np.dot(centroid_normal, i)) for i in dist_arr]
        normal_plane_mod = [header.np.linalg.norm(header.np.multiply(header.np.dot(centroid, i), i)) for i in sorted_separation_arr_unit]
        average_proj = header.np.average(proj_r)
        average_angle = header.np.rad2deg(header.np.average([header.np.arccos(round(i/header.np.linalg.norm(header.np.array(cluster_centers[c])), 4)) for i in normal_plane_mod]))  # s = r * \sin \theta
        avg_d_arr.append(average_proj)
        avg_a_arr.append(average_angle)
        var_arr.append(average_angle)

    self.rtol, self.atol, self.var = round(header.np.average(avg_d_arr), 2), round(header.np.average(avg_a_arr), 2), round(header.np.average(var_arr), 2)
    print("Suggested distance cutoff for polyhedron: ", self.rtol)
    print("Suggested angle cutoff for polyhedron: ", self.atol)
    # print(self.var)
        
    #*********************************************************************************

    group_arr = []
    c = 0
    for i in range(len(separation_arr_len)):
        sorted_arr = self.labels[c:c+separation_arr_len[i]]
        sorted_arr.sort()
        # print(c, c+separation_arr_len[i], sorted_arr.tolist())
        # print(sorted_arr.tolist())
        group_arr.append(sorted_arr.tolist())
        c = c+separation_arr_len[i]
    
    #*************************************************************************************
    # Getting a list of list 
    # Each sub-list consists of the points with similar environment among the considered system
    '''unique_arr = []
    for g in group_arr:
        if g not in unique_arr:
            unique_arr.append(g)

    count_arr = []
    for i in range(len(unique_arr)):
        count = 0
        for j in range(len(group_arr)):
            if unique_arr[i] == group_arr[j]:
                count = count + 1

        count_arr.append(count)

    raw_count_arr = count_arr[:]
    count_arr.sort(reverse=True)
    sorted_unique_arr = []
    for c in count_arr:
        index = [i for i, e in enumerate(raw_count_arr) if e == c]
        for k in index:
            sorted_unique_arr.append(unique_arr[k])
        if len(sorted_unique_arr) == len(unique_arr):
            break

    unique_arr = sorted_unique_arr[:]
    # print(unique_arr)
    # print("Number of unique environment :", len(unique_arr))
    
    chosen_particle_arr = []
    for g in range(len(group_arr)):
        if group_arr[g] == unique_arr[0]:
            chosen_particle_arr.append(g)

    particle_arr_env = []
    for i in unique_arr:
        particle_id_arr = []
        for j in range(len(group_arr)):
            if i == group_arr[j]:
                particle_id_arr.append(j)
        particle_arr_env.append(particle_id_arr)

    # print("Number of Environment : ", len(particle_arr_env))'''
    
    #*************************************************************************************
    # This thing migh needed, don't delete it
    # If two lists have c% commonality, then we will consider those as same list.
    # THIS PART IS OKAY. DON'T CHANGE IT : IMPORTANT

    #****************************************************************
    c = self.match
    unique_arr, count_arr, equiv_particle_arr = [], [], []
    particle_counter = 0
    for g in group_arr:
        if len(g) != 0:
            if len(unique_arr) == 0:
                unique_arr.append(g)
                count_arr.append(1)
                equiv_particle_arr.append([particle_counter])
            else:
                count = 0
                perm_arr = ['n' for _ in range(len(unique_arr))]
                for k in range(len(unique_arr)):
                    li = list(set(unique_arr[k]).intersection(list(set(g))))
                    if len(li)/len(g) < c:  # unique
                        count = count + 1
                    else:
                        perm_arr[k] = 'y'

                if count == len(unique_arr):   # unique
                    unique_arr.append(g)
                    count_arr.append(1)
                    equiv_particle_arr.append([particle_counter])
                else:
                    for k in range(len(unique_arr)):
                        if perm_arr[k] == 'y':
                            count_arr[k] = count_arr[k] + 1
                            equiv_particle_arr[k].append(particle_counter)

        else:
            if g not in unique_arr:
                unique_arr.append(g)
                count_arr.append(1)
                equiv_particle_arr.append([particle_counter])
            else:
                for k in range(len(unique_arr)):
                    if len(unique_arr[k]) == 0:
                        count_arr[k] = count_arr[k] + 1
                        equiv_particle_arr[k].append(particle_counter)

        particle_counter = particle_counter + 1

    max_count = header.np.max(count_arr)
    count_arr.sort(reverse=True)
    self.input_dec, done5 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter your choice (int) of environment \n id-\'0\' is preferred corresponding to max number of particles \n of single crystalline structure')
    index = [i for i, e in enumerate(count_arr) if e == count_arr[int(self.input_dec)]]
    unique_arr_max = unique_arr[index[0]]
    equiv_particles = equiv_particle_arr[index[0]]
    chosen_particle_arr = equiv_particles[:]
    self.chosen_particle_arr = chosen_particle_arr[:]
    self.original_chosen_particle_arr = []
    for z in range(len(chosen_particle_arr)):
        indi = [i for i, e in enumerate(self.original_particleids) if e == self.particleids[chosen_particle_arr[z]]][0]
        self.original_chosen_particle_arr.append(self.original_particleids[indi])

    particle_arr_env = [[] for _ in range(len(unique_arr))]
    for j in range(len(group_arr)):
        for k in range(len(unique_arr)):
            if group_arr[j] == unique_arr[k]:
                particle_arr_env[k].append(j)

    # print(len(chosen_particle_arr))
    # print(particle_arr_env)
    #*************************************************************************************
    # Save the configuration in different colors
    # Each color represents the points with similar kind of environment
    self.answer, done2 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Save Configuration? (y/n)') 

    answer = self.answer
    if answer == 'y' or answer == 'yes':
        options = header.QFileDialog.Options()
        options |= header.QFileDialog.DontUseNativeDialog
        fileName, _ = header.QFileDialog.getSaveFileName(self, 
            "Save File", "", "Image Files(*.png);;All Files(*)", options = options)

        # alpha, beta, gamma = 0, header.np.deg2rad(10), header.np.deg2rad(10)
        # self.quat = header.rowan.normalize(header.rowan.from_euler(alpha, beta, gamma, convention='zyx'))

        # Just handling of the color coding, nothing important !
        # Handling the noise
        modified_particle_arr_env = []
        defective_env_arr = []
        for t in range(len(particle_arr_env)):
            # if len(particle_arr_env[t]) > int(len(self.positions)*0.01):
            if len(particle_arr_env[t]) >= 0:
                modified_particle_arr_env.append(particle_arr_env[t])

            else:
                for l in range(len(particle_arr_env[t])):
                    defective_env_arr.append(particle_arr_env[t][l])
            
        if len(defective_env_arr) > 0:
            modified_particle_arr_env.append(defective_env_arr)

        # print(modified_particle_arr_env)
        # print(len(defective_env_arr))
        print("Number of Environment : ", len(modified_particle_arr_env))

        defect_code = "#000000"   # Defective particles
        hex_colors = ['#bb2e1b', '#52a50c', '#f43c85', '#0944ba', '#33723a', '#8f7c61', '#da51d8', '#3db5a7', '#b2eb39', '#bb00cd', '#f7258f', '#2df3e6', '#5c20fb', '#05167f', '#d97e11', '#764105', '#d0c770', '#d10a81', '#fffc05', '#2938f4', '#126e86', '#a29494', '#b49f27', '#e6b813', '#ca5f7c']
        self.hex_colors = hex_colors[:]
        # Random hex color_code generation
        # protocol 1
        N = len(modified_particle_arr_env) + 1
        colors = header.distinctipy.get_colors(N)
        added_hex_colors = [str(header.matplotlib.colors.to_hex(t)) for t in colors]
        for t in added_hex_colors:
            hex_colors.append(t)

        #*****************************************************************
        # protocol 2
        '''if self.env_count == 0:
            self.color_code_array = []
            N = len(modified_particle_arr_env) + 1
            for i in range(N):
                color_hex = "%06x" % header.random.randint(0, 0xFFFFFF)
                self.color_code_array.append('#'+color_hex)
                self.env_count = self.env_count + 1
                self.color_code_array_other = self.color_code_array[:]

        else:
            self.color_code_array_other = []
            N = len(modified_particle_arr_env) + 1
            for i in range(N):
                color_hex = "%06x" % header.random.randint(0, 0xFFFFFF)
                self.color_code_array_other.append('#'+color_hex)
                self.env_count = self.env_count + 1

        hex_colors = []
        for t in range(len(self.color_code_array_other)):
            if t < len(self.color_code_array):
                hex_colors.append(self.color_code_array[t])
            else:
                hex_colors.append(self.color_code_array_other[t])'''

        #*****************************************************************

        color_arr = [[] for t in range(len(modified_particle_arr_env))]
        if len(defective_env_arr) > 0:
            for t in range(len(modified_particle_arr_env)-1):
                for u in range(len(modified_particle_arr_env[t])):
                    rgba_color = header.matplotlib.colors.to_rgba(hex_colors[t])
                    color_arr[t].append(rgba_color)
                
            for u in range(len(modified_particle_arr_env[-1])):
                rgba_color = header.matplotlib.colors.to_rgba(defect_code)
                color_arr[t].append(rgba_color)

        else:
            for t in range(len(modified_particle_arr_env)):
                for u in range(len(modified_particle_arr_env[t])):
                    rgba_color = header.matplotlib.colors.to_rgba(hex_colors[t])
                    color_arr[t].append(rgba_color)
        
        particle_positions_arr = [[self.positions[t] for t in u] for u in modified_particle_arr_env]
        particle_orientations_arr = [[self.orientations[t] for t in u] for u in modified_particle_arr_env]

        env_positions = list(header.chain.from_iterable(particle_positions_arr))
        env_orientations = list(header.chain.from_iterable(particle_orientations_arr))
        env_colors = list(header.chain.from_iterable(color_arr))

        if len(self.verts) != 0:
            poly_info = header.draw1.ConvexPolyhedra(colors=env_colors, positions=env_positions, orientations=env_orientations, outline=0.01, vertices=self.verts, primitive_color_mix=0, roughness = 0.1, specular = 1.0, spec_trans=0.1)
        else:
            poly_info = header.draw1.Spheres(colors=env_colors, positions=env_positions, radii=self.sphereRadius)

        box_primitive = header.draw1.Box(Lx=self.box[0], Ly=self.box[1], Lz=self.box[2], xy=self.box[3], xz=self.box[4], yz=self.box[5], widths=0.3, colors=[0, 0, 0, 1], width=0.1, color=[0, 0, 0, 1])

        # High quality image
        '''scene = header.draw1.Scene((poly_info, box_primitive), rotation=q, size=(70, 70),  pixel_scale=100)
        scene.enable("ambient_light", 1.5)
        scene.enable("directional_light", [-1.5, 0, 0])
        scene.enable("antialiasing", 1.0)
        scene.enable("pathtracer", samples=128)
        scene.save(fileName + '.png')'''

        # # Standard quality image
        scene = header.draw1.Scene((poly_info, box_primitive), rotation=self.quat, size=(self.figsize, self.figsize),  pixel_scale=50)
        scene.enable("ambient_light", 1.5)
        scene.enable("directional_light", [-1.5, 0, 0])
        scene.enable("antialiasing", 1.0)
        scene.enable("pathtracer", samples=self.samples)
        scene.save(fileName + '.png')

        # BOD
        '''centers_positions = [header.np.array([cluster_centers[t] for t in u]) for u in unique_arr]

        # Plot bod
        figure_bod = header.Figure(figsize=(2.5, 2))
        ax_bod = figure_bod.add_subplot(projection="3d")

        for t in range(len(centers_positions)):
            ax_bod.scatter(centers_positions[t][:,0], centers_positions[t][:,1], centers_positions[t][:,2], c=hex_colors[t], s=0.5)

        # ax_bod.set_axis_off()

        options = header.QFileDialog.Options()
        options |= header.QFileDialog.DontUseNativeDialog
        fileName, _ = header.QFileDialog.getSaveFileName(self, 
            "Save File", "", "All Files(*);;Image Files(*.png)", options = options)
        
        view_angle = 0, 0
        ax_bod.view_init(*view_angle)
        figure_bod.savefig(fileName, dpi=300)
        header.plt.close()'''

    self.go_action = header.QAction("&Go", self)
    self.go_action.triggered.connect(lambda:env_separation_func(self))
    self.envsepMenu.addAction(self.go_action)

    print("Percentage of one kind of environment is : ", (len(self.chosen_particle_arr)*100)/len(self.positions))