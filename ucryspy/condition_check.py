# Searches for the triplets with crystal class of the highest order

import header
from lattice_param import lattice_param_func
from final_check import final_check_func

def check_combin(self, i, combin, return_dict):
    arr, latt_arr = [], []
    category_arr, volume_arr, lattice_param_arr, combin_arr = [], [], [], []
    for comb in combin:
        bool = 0
        a = lattice_param_func(comb)
        a = [round(a[0], 3), round(a[1], 3), round(a[2], 3), round(a[3], 3), round(a[4], 3), round(a[5], 3)]
        if a not in latt_arr and len(a) != 0 and a[0] > self.dist_cutoff and a[1] > self.dist_cutoff and a[2] > self.dist_cutoff and a[3] > self.angle_cutoff and a[4] > self.angle_cutoff and a[5] > self.angle_cutoff and a[3] < (180-self.angle_cutoff) and a[4] < (180-self.angle_cutoff) and a[5] < (180-self.angle_cutoff):
            Lx, Ly, Lz, alpha, beta, gamma = a[0], a[1], a[2], header.np.deg2rad(a[3]), header.np.deg2rad(a[4]), header.np.deg2rad(a[5])
            sq = 1-header.np.cos(alpha)*header.np.cos(alpha) - header.np.cos(beta)*header.np.cos(beta) - header.np.cos(gamma)*header.np.cos(gamma) + (2*header.np.cos(alpha)*header.np.cos(beta)*header.np.cos(gamma))
            if sq >= 0:
                vol = round(Lx*Ly*Lz*header.np.sqrt(sq), 7)

                self.lv = a[:]
                pp = final_check_func(self)
                if pp != "NONE" and vol != 0:
                    a.append(vol)
                    lattice_param_arr.append(a[:-1])
                    volume_arr.append(a[-1])
                    a.append(pp)
                    arr.append(a)
                    latt_arr.append(a[:6])
                    category_arr.append(pp)
                    combin_arr.append(comb)
                    # print(a[:-2], pp)

                else:
                    bool = 1
            else:
                bool = 1
        else:
            bool = 1

        if bool == 1:
            lattice_param_arr.append([0, 0, 0, 0, 0, 0])
            volume_arr.append(0)
            a.append("")
            arr.append(a)
            latt_arr.append([0, 0, 0, 0, 0, 0])
            category_arr.append("")
            combin_arr.append([[], [], []])

    return_dict[i] = [lattice_param_arr[:], volume_arr[:], a[:], arr[:], latt_arr[:], category_arr[:], combin_arr[:]]

class Arrow3D(header.FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        header.FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = header.proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        header.FancyArrowPatch.draw(self, renderer)

def condition_check_func(self, combin):
    # multiprocess
    max_num_proc = 6  # Num processors
    num_comb = 0
    comb_arr = []
    for comb in combin:
        comb_arr.append(comb)
        num_comb = num_comb + 1

    # Distributing the jobs within the processors
    num_choices = num_comb
    per_proc_job = int(num_choices/(max_num_proc-1))
    modified_comb_arr = []
    initial_indices = [t for t in range(0, num_choices, per_proc_job)]
    if num_choices%max_num_proc == 0:
        modified_comb_arr = [comb_arr[t:(t+per_proc_job)] for t in initial_indices]
    else:
        modified_comb_arr = [comb_arr[t:(t+per_proc_job)] for t in initial_indices[:-1]]
        modified_comb_arr.append(comb_arr[initial_indices[-1]:num_choices])

    manager = header.multiprocess.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(len(modified_comb_arr)): # Calling the target function
        p = header.multiprocess.Process(target=check_combin, args=(self, i, modified_comb_arr[i], return_dict))
        p.start()
        jobs.append(p)

    for proc in jobs:
        proc.join()

    # serial_arr = ['CUBIC', 'HEXAGONAL', 'TETRAGONAL', 'RHOMBOHEDRAL', 'ORTHORHOMBIC', 'MONOCLINIC', 'TRICLINIC']
    lattice_param_arr, volume_arr, a, arr, latt_arr, category_arr, combin_arr = [], [], [], [], [], [], []

    values = list(return_dict.values())
    for t in range(len(values)):
        lattice_param_arr.append(values[t][0])
        volume_arr.append(values[t][1])
        a.append(values[t][2])
        arr.append(values[t][3])
        latt_arr.append(values[t][4])
        category_arr.append(values[t][5])
        combin_arr.append(values[t][6])

    lattice_param_arr, volume_arr, a, arr, latt_arr, category_arr, combin_arr = list(header.chain.from_iterable(lattice_param_arr)), list(header.chain.from_iterable(volume_arr)), list(header.chain.from_iterable(a)), list(header.chain.from_iterable(arr)), list(header.chain.from_iterable(latt_arr)), list(header.chain.from_iterable(category_arr)), list(header.chain.from_iterable(combin_arr))
    
    #*********************************************************************************
    # Single processor code
    '''arr, latt_arr = [], []
    category_arr, volume_arr, lattice_param_arr, combin_arr = [], [], [], []
    serial_arr = ['CUBIC', 'HEXAGONAL', 'TETRAGONAL', 'RHOMBOHEDRAL', 'ORTHORHOMBIC', 'MONOCLINIC', 'TRICLINIC']
    # get the lattice parameters for all lattice vectors
    for comb in combin:
        a = lattice_param_func(comb)
        a = [round(a[0], 3), round(a[1], 3), round(a[2], 3), round(a[3], 3), round(a[4], 3), round(a[5], 3)]
        if a not in latt_arr and len(a) != 0 and a[0] >= 0.01 and a[1] >= 0.01 and a[2] >= 0.01 and a[3] != 0 and a[4] != 0 and a[5] != 0 and a[3] != 180 and a[4] != 180 and a[5] != 180:
            Lx, Ly, Lz, alpha, beta, gamma = a[0], a[1], a[2], header.np.deg2rad(a[3]), header.np.deg2rad(a[4]), header.np.deg2rad(a[5])
            sq = 1-header.np.cos(alpha)*header.np.cos(alpha) - header.np.cos(beta)*header.np.cos(beta) - header.np.cos(gamma)*header.np.cos(gamma) + (2*header.np.cos(alpha)*header.np.cos(beta)*header.np.cos(gamma))
            if sq >= 0:
                vol = round(Lx*Ly*Lz*header.np.sqrt(sq), 7)

                self.lv = a[:]
                pp = final_check_func(self)
                if pp != "NONE" and vol != 0:
                    a.append(vol)
                    lattice_param_arr.append(a[:-1])
                    volume_arr.append(a[-1])
                    a.append(pp)
                    arr.append(a)
                    latt_arr.append(a[:6])
                    category_arr.append(pp)
                    combin_arr.append(comb)
                    # print(a[:-2], pp)'''

    #*********************************************************************************
    # Unit cell corresponding to the max symmetry and min volume
    # Not implemented, will be used for further studies
    '''self.LattVec = []
    self.LattParam = []
    for i in range(len(serial_arr)):
        indices = [t for t, e in enumerate(category_arr) if e == serial_arr[i]]
        if len(indices) > 0:
            sorted_combin_arr = [combin_arr[t] for t in indices]
            sorted_vol_arr = [volume_arr[t] for t in indices]
            sorted_lattice_param_arr = [lattice_param_arr[t] for t in indices]
            min_vol = header.np.min(sorted_vol_arr)
            index = [t for t, e in enumerate(sorted_vol_arr) if e == min_vol]   # Min volume
            #****************************************************************
            sorted_abc_abg = sorted_lattice_param_arr[index[0]]
            sorted_latt_vec = sorted_combin_arr[index[0]]
            print(sorted_lattice_param_arr[index[0]], min_vol, serial_arr[i])

            self.LattParam = sorted_abc_abg
            self.LattVec.append(sorted_latt_vec)
            self.ty = serial_arr[i]
            break'''

    #***************************************************************************************************************
    # Get the direction of the lattice vectors satisfying the crystal class of the highest order
    '''sorted_category_arr = list(set(category_arr[:]))
    for i in range(len(serial_arr)):
        if serial_arr[i] in sorted_category_arr:
            self.ty = serial_arr[i]
            break
    print("Detected crystal class is : ", self.ty)

    indices = [t for t, e in enumerate(category_arr) if e == self.ty]
    if len(indices) > 0:
        sorted_combin_arr = [combin_arr[t] for t in indices]
        self.LattVec = sorted_combin_arr[:]
        self.selected_arr = [latt_arr[t] for t in indices]'''

    sorted_combin_arr = [combin_arr[t] for t in range(len(combin_arr)) if volume_arr[t] != 0]
    self.LattVec = sorted_combin_arr[:]
    self.selected_arr = [latt_arr[t] for t in range(len(latt_arr)) if volume_arr[t] != 0]

    # Selecting the array which are elementwise different from others
    ttol = self.dist_cutoff
    if len(self.selected_arr) >= 1:
        distinct_list = []
        self.selected_arr = [sorted(t) for t in self.selected_arr]
        # print(self.selected_arr)
        numpy_list = [header.np.array(t) for t in self.selected_arr]
        distinct_list.append(numpy_list[0].tolist())
        id_arr = [0]
        for u in range(1, len(numpy_list)):
            counter = 0
            for v in range(len(distinct_list)):
                if header.np.allclose(header.np.array(distinct_list[v]), numpy_list[u], atol=ttol) == False:
                    counter =  counter + 1
            if counter == len(distinct_list):
                if numpy_list[u].tolist() not in distinct_list:
                    distinct_list.append(numpy_list[u].tolist()) 
                    id_arr.append(u)

        self.LattVec = [self.LattVec[t] for t in id_arr]  
        self.selected_arr = [self.selected_arr[t] for t in id_arr]

    # print(header.np.array(self.selected_arr))
    # print(header.np.array(self.LattVec))
    
    # print(self.LattVec)
    # Multiple triplets can be achieved corresponding to the crystal class with the highest order
    # print("Detected crystal class is : ", self.ty)
    # print("Number of possible choice of unit cells : ", len(self.LattVec))

    #********************************************************
    # In case, user wants to see the direction of basis vectors passing through faces, edges or vertices
    # Add arrows along \hat{a}, \hat{b}, \hat{c} in BOD
    '''if self.click_count == 0:
        x, y, z = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        u, v, w = [self.LattVec[0][0], self.LattVec[0][1], self.LattVec[0][2]]
        self.ax_bod.quiver(0, 0, 0, self.LattVec[0][0][0], self.LattVec[0][0][1], self.LattVec[0][0][2], lw=2, length=1.5, colors='r')
        self.ax_bod.quiver(0, 0, 0, self.LattVec[0][1][0], self.LattVec[0][1][1], self.LattVec[0][1][2], lw=2, length=1.5, colors='b')
        self.ax_bod.quiver(0, 0, 0, self.LattVec[0][2][0], self.LattVec[0][2][1], self.LattVec[0][2][2], lw=2, length=1.5, colors='g')

        self.vertices_clusters = header.np.array(self.vertices_clusters)
        # Polyhedron
        for s in self.faces:
            tri = header.Poly3DCollection([header.np.array([self.vertices_clusters[t] for t in s])])
            tri.set_color('darkgrey')
            tri.set_alpha(0.5)
            self.ax_bod.add_collection3d(tri)

        self.ax_bod.set_axis_off()
        self.figure_bod.tight_layout()
        self.canvas_bod.draw()
        self.ax_bod.set_box_aspect((self.rcut, self.rcut, self.rcut), zoom=1.3)
        # Zoom and pan
        ph = header.panhandler(self.figure_bod, button=3)  # pan with right mouse button
        header.zoom_factory(self.ax_bod)
        self.grid.addWidget(self.canvas_bod, 2, 0)

        self.click_count = self.click_count + 1

    elif self.click_count > 0:
        # Remove arrow widget
        self.grid.removeWidget(self.canvas_bod)
        self.ax_bod.remove()
        self.canvas_bod.deleteLater()

        self.figure_bod = header.Figure(figsize=(2.5, 2))
        self.ax_bod = self.figure_bod.add_subplot(111, projection="3d")
        self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)
        x, y, z = self.r_data[:,0], self.r_data[:,1], self.r_data[:,2]

        # Scatter plot in 3D
        self.ax_bod.scatter(x, y, z, c=self.c, s=7.0)
        self.ax_bod.set_box_aspect((self.rcut, self.rcut, self.rcut), zoom=1.3)

        # Polyhedron
        for s in self.faces:
            tri = header.Poly3DCollection([header.np.array([self.vertices_clusters[t] for t in s])])
            tri.set_color('darkgrey')
            tri.set_alpha(0.5)
            self.ax_bod.add_collection3d(tri)

        # Arrow
        x, y, z = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        u, v, w = [self.LattVec[0][0], self.LattVec[0][1], self.LattVec[0][2]]
        self.ax_bod.quiver(0, 0, 0, self.LattVec[0][0][0], self.LattVec[0][0][1], self.LattVec[0][0][2], lw=2, length=1.5, colors='r')
        self.ax_bod.quiver(0, 0, 0, self.LattVec[0][1][0], self.LattVec[0][1][1], self.LattVec[0][1][2], lw=2, length=1.5, colors='b')
        self.ax_bod.quiver(0, 0, 0, self.LattVec[0][2][0], self.LattVec[0][2][1], self.LattVec[0][2][2], lw=2, length=1.5, colors='g')

        self.ax_bod.set_axis_off()
        self.figure_bod.tight_layout()
        self.canvas_bod.draw()
        # Zoom and pan
        ph = header.panhandler(self.figure_bod, button=3)  # pan with right mouse button
        header.zoom_factory(self.ax_bod)
        self.grid.addWidget(self.canvas_bod, 2, 0)

        self.click_count = self.click_count + 1'''

    
