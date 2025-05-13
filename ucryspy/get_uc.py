# This scripts calculates the eight corner points according to the direction of the lattice vectors
# Get all the lattice sistes of the unit cell
# Calcuate equivalent lattice sites
# determine the space group using Spglib package.
#*********************************MOST IMPORTANT CODE**********************************

# It will give you the option in case multiple triplets are found for the crystal class with highest order
# The user should choose the accepeted triplet accoring to their own choice, by providing a integer value 
#**************************************************************************************

import header
import lattice_param
from lattice_param import lattice_param_func
from final_check import final_check_func
from vol_scaling_poly import vol_scaling_poly_func
import get_posi_orien_local_frame
from save_uc import save_uc_func
from save_basis import save_basis_func
from clear_plot import clear_plot_func
from screenshot import save_screenshot_func
from symm import symm_func
from calc_equiv_points_poly import calc_equiv_points_poly_func

def tol_func(self):
    def get_rtol(a):
        self.rtol = float(a.text())

    self.rtol_submenu = self.envsepMenu.addMenu('r_tol')
    c = 0
    start, end, width = self.data["rtol_min"], self.data["rtol_max"], self.data["rtol_count"]   # Change the limit if necessary
    num = (end - start)/width
    per_submenu = 30
    num_submenu = int(num/per_submenu) + 1
    g = 100
    c_end = 0
    self.rtol_subsubmenu = self.rtol_submenu.addMenu('Ideal crystal')
    self.rtol_subsubmenu.addAction(str(0.00001))
    self.rtol_subsubmenu.triggered[header.QAction].connect(get_rtol)
    for c in range(num_submenu):
        if c == 0:
            c_start = start
        else:
            c_start = c_end
        c_end = round(c_start  + width*per_submenu, 2)
        rtol_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
        self.rtol_subsubmenu = self.rtol_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(rtol_arr[-1],2)))
        for r in rtol_arr:
            self.rtol_subsubmenu.addAction(str(r))
        self.rtol_subsubmenu.triggered[header.QAction].connect(get_rtol)

    def get_atol(a):
        self.atol = float(a.text())

    self.atol_submenu = self.envsepMenu.addMenu('a_tol')
    c = 0
    start, end, width = self.data["atol_min"], self.data["atol_max"], self.data["atol_count"]   # Change the limit if necessary
    num = (end - start)/width
    per_submenu = 10
    num_submenu = int(num/per_submenu) + 1
    g = 100
    c_end = 0
    self.atol_subsubmenu = self.atol_submenu.addMenu('Ideal crystal')
    self.atol_subsubmenu.addAction(str(0.00001))
    self.atol_subsubmenu.triggered[header.QAction].connect(get_atol)
    for c in range(num_submenu):
        if c == 0:
            c_start = start
        else:
            c_start = c_end
        c_end = round(c_start  + width*per_submenu, 2)
        atol_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
        self.atol_subsubmenu = self.atol_submenu.addMenu(str(round(atol_arr[0],2)) + " - " + str(round(atol_arr[-1],2)))
        for r in atol_arr:
            self.atol_subsubmenu.addAction(str(r))
        self.atol_subsubmenu.triggered[header.QAction].connect(get_atol)

    self.go_action = header.QAction("&Go", self)
    self.go_action.triggered.connect(lambda:get_uc_func(self))
    self.envsepMenu.addAction(self.go_action)

    self.enable_tol_func = True

def calc_crysClass(self):
    # getting few entries, nothing serious, just variable change
    self.dist_cutoff = self.rtol
    self.angle_cutoff = self.atol
    self.n_clusters = self.elbow

    # Trying to detect the point group symmetry of BOD  
    self.tolerance = self.atol
    # self.tolerance = float(input("Enter the tolerance for BOD : "))
    sorted_mod_positions_all, self.vertices_direc_arr, self.faces_direc_arr, self.edges_direc_arr = calc_equiv_points_poly_func(self, self.vertices_clusters, self.faces, self.edges)   # Convex decomposition

    if self.ty != 'NONE' and self.ty != 'TRICLINIC':
        # print("Number of faces and edges of the constructed polyehdron is : ", len(self.edges), len(self.faces))
        # print(len(sorted_mod_positions_all))
        # sorted_posi = sorted_mod_positions_all[:]
        #***************************************************************
        # Decorating the axes
        sorted_mod_positions_dec = []
        sorted_mod_positions_dec.append(sorted_mod_positions_all[0])

        dic = {}
        angle_arr = []
        for t in range(1, len(sorted_mod_positions_all)):
            angle = header.np.rad2deg(header.np.arccos(round(header.np.dot(sorted_mod_positions_all[0]/header.np.linalg.norm(sorted_mod_positions_all[0]), sorted_mod_positions_all[t]/header.np.linalg.norm(sorted_mod_positions_all[t])), 3)))
            dic[t]=angle    

        vec_id, angle_arr = list(dic.keys()), list(dic.values())
        counetr_angle_arr = header.Counter(angle_arr)
        angles_sorted = list(counetr_angle_arr.keys())
        for a in range(len(angles_sorted)):
            indi = [i for i, e in enumerate(angle_arr) if e == angles_sorted[a]]
            for t in indi:
                sorted_mod_positions_dec.append(sorted_mod_positions_all[t])

        sorted_posi = sorted_mod_positions_dec[:]
        #******************************************************************************
        # self.center = header.np.mean(header.np.array([self.mm_positions[i] for i in range(len(self.mm_positions))]), axis=0).tolist()
        symm_func(self, sorted_posi)
    
        # print("Detected crystal class is : ", self.ty)
        print("Number of possible choice of unit cells : ", len(self.LattVec))

    self.user_input_dec, done4 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Continue? (y/n)')

    user_input_dec = self.user_input_dec
    if user_input_dec == 'n':
        print("WARNING : Please recalculate \"Environment separation\" with extarnal tolerance values")
        if self.enable_tol_func == False:
            tol_func(self)
    elif user_input_dec == 'y':
        print("Let's check whether any valid unit cells are obtained with these choices !")

# Calculating the vertices for updated polyhedron with volume scaling factor
def calculate_the_vertices(self, particles_positions):
    dim = 3
    inverse_dim = 1.0/float(dim)
    modified_particles_positions = [[(particles_positions[i][j]) * header.np.power((self.increased_volume/self.volume), inverse_dim) for j in range(len(particles_positions[i]))] for i in range(len(particles_positions))]

    return modified_particles_positions

# Get the nearest point along a particluar direction with respect to the reference point
def get_particle_along_a_direction(self, num_particles, ref_position, director, a, dist_cutoff):
    dist_arr, p_arr = [], []
    for j in range(num_particles):
        vec = self.box_arr.wrap(self.positions[j] - ref_position)
        d = header.np.linalg.norm(vec)
        if d != 0:
            unit_vec = vec/d
            angle = header.np.rad2deg(header.np.arccos(round(header.np.dot(director, unit_vec), 2)))
            if angle <= self.angle_cutoff:
                dist_arr.append(d)  
                p_arr.append(j)  # Store the particles' id

    if len(dist_arr) >= 1:
        min_d = header.np.min(dist_arr)   # Nearest point
        if (a-dist_cutoff) <= min_d <= (a+dist_cutoff):
            # print(min_d)
            index = [i for i, e in enumerate(dist_arr) if e == min_d]

            return p_arr[index[0]]
        else:
            return -1
    else:
        return -1

    return index


# If no point is achieved along a particluar direction in the system due to the noise, a dummy coordinate is provided along that particluar direction and at the particular distance.
def get_points_instead_particles(self, num_particles, ref_position, director, a, dist_cutoff):
    point = self.box_arr.wrap(ref_position + a*header.np.array(director))  # Dummy position

    return point

# Get the point-4, 5, 6, 7 by translating along the direction of the lattice vectors.
# Follow the instructions in the documentation
def get_another_particles(self, particle_arr, particle_positions, num_particles):
    pp = particle_arr[3]
    got_particle = get_particle_along_a_direction(self, num_particles, self.positions[pp], self.modified_matrix[0], self.abc[0], self.dist_cutoff)
    if got_particle != -1 and got_particle not in particle_arr:
        particle_arr.append(got_particle)    #4 particle
        particle_positions.append(self.positions[got_particle].tolist())
    
    else:
        point = get_points_instead_particles(self, num_particles, self.positions[pp], self.modified_matrix[0], self.abc[0], self.dist_cutoff)
        particle_positions.append(point)
        particle_arr.append(-1)

    pp = particle_arr[3]
    got_particle = get_particle_along_a_direction(self, num_particles, self.positions[pp], self.modified_matrix[1], self.abc[1], self.dist_cutoff)
    if got_particle != -1 and got_particle not in particle_arr:
        particle_arr.append(got_particle)    #5 particle
        particle_positions.append(self.positions[got_particle].tolist())

    else:
        point = get_points_instead_particles(self, num_particles, self.positions[pp], self.modified_matrix[1], self.abc[1], self.dist_cutoff)
        particle_positions.append(point)
        particle_arr.append(-1)

    # print(len(particle_arr))
    pp = particle_arr[2]
    got_particle = get_particle_along_a_direction(self, num_particles, self.positions[pp], self.modified_matrix[0], self.abc[0], self.dist_cutoff)
    if got_particle != -1 and got_particle not in particle_arr:
        particle_arr.append(got_particle)  #6 particle
        particle_positions.append(self.positions[got_particle].tolist())

    else:
        point = get_points_instead_particles(self, num_particles, self.positions[pp], self.modified_matrix[0], self.abc[0], self.dist_cutoff)
        particle_positions.append(point)
        particle_arr.append(-1)

    pp_positions = particle_positions[5]
    got_particle = get_particle_along_a_direction(self, num_particles, pp_positions, self.modified_matrix[0], self.abc[0], self.dist_cutoff)
    if got_particle != -1 and got_particle not in particle_arr:
        particle_arr.append(got_particle)  #7 particle
        particle_positions.append(self.positions[got_particle].tolist())

    else:
        point = get_points_instead_particles(self, num_particles, pp_positions, self.modified_matrix[0], self.abc[0], self.dist_cutoff)
        particle_positions.append(point)
        particle_arr.append(-1)

    # print(particle_arr)
    return particle_arr, particle_positions

def final_check_bravais_nonbravais(self, center, particle_positions, particles_arr, particles_posi, modified_particles_positions):
    others_wrt_center = [(header.np.array(t) - center) for t in particles_posi] 
    nonbrav_particles = []
    for g in range(len(others_wrt_center)):
        if others_wrt_center[g].tolist() not in particle_positions:
            posi = others_wrt_center[g]
            c = header.Delaunay(modified_particles_positions).find_simplex(posi)
            if c >= 0:
                particle_positions.append(posi.tolist())
                particles_arr.append(g)
                nonbrav_particles.append(g)

    # Now the ids of all the points inside the chosen unit cell are known, all the positions are in the local frame of UC
    basic_set_positions = particle_positions[:]

    return basic_set_positions, particles_arr, nonbrav_particles

def check_bravais(self, center, particle_positions, particles_posi, vol, modified_particles_positions, particle_arr, count, successful_v):
    # Check for the points within the convex hull formed by the corner particles
    # Use Scipy Delaunay
    others_wrt_center = [(header.np.array(particles_posi[t]) - center) for t in range(len(particles_posi)) if t not in particle_arr] 
    for g in range(len(others_wrt_center)):
        if others_wrt_center[g].tolist() not in particle_positions:
            posi = others_wrt_center[g]
            c = header.Delaunay(modified_particles_positions).find_simplex(posi)
            if c >= 0:
                particle_positions.append(posi.tolist())

    # Now the ids of all the points inside the chosen unit cell are known, all the positions are in the local frame of UC
    basic_set_positions = particle_positions[:]

    # print(self.L, self.ty, round(vol, 4), len(equiv_pts), round((vol - total_particle_vol), 4))
    equiv_pts = equivalent_points(self, particle_positions)
    # print(self.L, self.ty, len(equiv_pts), vol)

    Latt_param = [round(float(self.L[0]), 3), round(float(self.L[1]), 3), round(float(self.L[2]), 3), round(float(self.L[3]), 3), round(float(self.L[4]), 3), round(float(self.L[5]), 3)]
    #******************************************************************
    # Check the Bravais lattice satisfied by the lattice vectors
    if self.ty == "TRICLINIC" and len(equiv_pts) == 1:  # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p

    elif self.ty == "MONOCLINIC" and len(equiv_pts) == 2: # B
        other_particles_except_corner = [header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[3], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[2], particle_positions[6], particle_positions[7], particle_positions[5]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[2], particle_positions[6], particle_positions[1]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[3], particle_positions[5], particle_positions[7], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[1], particle_positions[4], particle_positions[7], particle_positions[6]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[3], particle_positions[5], particle_positions[2]]), axis=0)]
        
        distance_all = [header.np.linalg.norm(header.np.array(t)-header.np.array(equiv_pts[1])) for t in other_particles_except_corner]
        small_dists = [t for t in distance_all if t <= self.dist_cutoff]
        if len(small_dists) == 1:
            print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
            p = 'passed'
            self.bravais_count = self.bravais_count + 1
            return p
        else:
            print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
            return -1
        
    elif self.ty == "MONOCLINIC" and len(equiv_pts) == 1: # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p
    
    elif self.ty == "ORTHORHOMBIC" and len(equiv_pts) == 1: # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p
    
    elif self.ty == "ORTHORHOMBIC" and len(equiv_pts) == 2: # B/I
        other_particles_except_corner = [header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[3], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[2], particle_positions[6], particle_positions[7], particle_positions[5]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[2], particle_positions[6], particle_positions[1]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[3], particle_positions[5], particle_positions[7], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[1], particle_positions[4], particle_positions[7], particle_positions[6]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[3], particle_positions[5], particle_positions[2]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[2], particle_positions[3],
                                                                           particle_positions[4], particle_positions[5], particle_positions[6], particle_positions[7]]), axis=0)]
        distance_all = [header.np.linalg.norm(header.np.array(t)-header.np.array(equiv_pts[1])) for t in other_particles_except_corner]
        small_dists = [t for t in distance_all if t <= self.dist_cutoff]
        if len(small_dists) == 1:
            print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
            p = 'passed'
            self.bravais_count = self.bravais_count + 1
            return p
        else:
            print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
            return -1

    elif self.ty == "ORTHORHOMBIC" and len(equiv_pts) == 4:  # F
        other_particles_except_corner = [header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[3], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[2], particle_positions[6], particle_positions[7], particle_positions[5]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[2], particle_positions[6], particle_positions[1]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[3], particle_positions[5], particle_positions[7], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[1], particle_positions[4], particle_positions[7], particle_positions[6]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[3], particle_positions[5], particle_positions[2]]), axis=0)]
        
        distance_all = [[header.np.linalg.norm(header.np.array(t)-header.np.array(equiv_pts[u])) for t in other_particles_except_corner] for u in range(1, 4)]
        small_dists = [[t for t in distance_all[u] if t <= self.dist_cutoff] for u in range(3)]
        flatten_dist = list(header.chain.from_iterable(small_dists))
        if len(flatten_dist) == 3:
            print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
            p = 'passed'
            self.bravais_count = self.bravais_count + 1
            return p
        else:
            print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
            return -1

    elif self.ty == "TETRAGONAL" and len(equiv_pts) == 1: # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p
    
    elif self.ty == "TETRAGONAL" and len(equiv_pts) == 2: # I
        other_particles_except_corner = [header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[2], particle_positions[3],
                                                                           particle_positions[4], particle_positions[5], particle_positions[6], particle_positions[7]]), axis=0)]
        distance_all = [header.np.linalg.norm(header.np.array(t)-header.np.array(equiv_pts[1])) for t in other_particles_except_corner]
        small_dists = [t for t in distance_all if t <= self.dist_cutoff]
        if len(small_dists) == 1:
            print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
            p = 'passed'
            self.bravais_count = self.bravais_count + 1
            return p
        else:
            print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
            return -1
        
    elif self.ty == "RHOMBOHEDRAL" and len(equiv_pts) == 1: # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p
    
    elif self.ty == "HEXAGONAL" and len(equiv_pts) == 1: # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p

    elif self.ty == "CUBIC" and len(equiv_pts) == 1: # P
        print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
        p = 'passed'
        self.bravais_count = self.bravais_count + 1
        return p
    
    elif self.ty == "CUBIC" and len(equiv_pts) == 2: # I
        other_particles_except_corner = [header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[2], particle_positions[3],
                                                                           particle_positions[4], particle_positions[5], particle_positions[6], particle_positions[7]]), axis=0)]
        distance_all = [header.np.linalg.norm(header.np.array(t)-header.np.array(equiv_pts[1])) for t in other_particles_except_corner]
        small_dists = [t for t in distance_all if t <= self.dist_cutoff]
        if len(small_dists) == 1:
            print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
            p = 'passed'
            self.bravais_count = self.bravais_count + 1
            return p
        else:
            print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
            return -1
        
    elif self.ty == "CUBIC" and len(equiv_pts) == 4: # F
        other_particles_except_corner = [header.np.average(header.np.array([particle_positions[0], particle_positions[1], particle_positions[3], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[2], particle_positions[6], particle_positions[7], particle_positions[5]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[2], particle_positions[6], particle_positions[1]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[3], particle_positions[5], particle_positions[7], particle_positions[4]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[1], particle_positions[4], particle_positions[7], particle_positions[6]]), axis=0),
                                         header.np.average(header.np.array([particle_positions[0], particle_positions[3], particle_positions[5], particle_positions[2]]), axis=0)]
        
        distance_all = [[header.np.linalg.norm(header.np.array(t)-header.np.array(equiv_pts[u])) for t in other_particles_except_corner] for u in range(1, 4)]
        small_dists = [[t for t in distance_all[u] if t <= self.dist_cutoff] for u in range(3)]
        flatten_dist = list(header.chain.from_iterable(small_dists))
        if len(flatten_dist) == 3:
            print(Latt_param, self.ty, len(equiv_pts), successful_v, ' --> passed ')
            p = 'passed'
            self.bravais_count = self.bravais_count + 1
            return p
        else:
            print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
            return -1
    else:
        # print(Latt_param, self.ty, len(equiv_pts), ' --> failed')
        return -1
        
def get_uc_particles(self):
    self.vol_scaling_factor = self.vf   # volume factor which the box will be increased by
    self.free_vol_arr = []
    num_particles = len(self.positions)
    # print(len(self.LattVec))
    LattVec_index = [i for i in range(len(self.LattVec))]
    LattVec_dummy_store = []
    uc_particles_positions, uc_particles_arr, LattVec_arr, uc_vol, center_arr, self.basis_id_arr = [], [], [], [], [], []
    acc_id_lattvec, lattice_vec_array = [], []

    # The space group number limit according to the International table
    # https://en.wikipedia.org/wiki/List_of_space_groups
    dic = {"CUBIC": [195, 230], "HEXAGONAL": [168, 194], "RHOMBOHEDRAL": [143, 167], "TETRAGONAL": [75, 142], "ORTHORHOMBIC": [16, 74], "MONOCLINIC": [3, 15], "TRICLINIC": [1, 2]}
    self.keys, self.values = list(dic.keys()), list(dic.values())
    self.sg_values = dic[self.ty]
    self.cutoff_list = []
    c = 0
    check_counter = 0
    check_bool = 0
    lattice_vec_count = 0
    successful_v = 0
    random_particle = -1
    check_tol = 50
    self.global_particle_arr = []
    print(len(self.chosen_particle_arr))
    while len(LattVec_dummy_store) != len(LattVec_index) or len(acc_id_lattvec)==0:
        # Choosing a random particle near the center, not from the surface area
        random_particle = header.np.random.randint(0, len(self.positions))
        # print(random_particle)
        dist = header.np.linalg.norm(self.box_arr.wrap(self.positions[random_particle]))
        while dist > self.box_arr.Lx*0.25:
            random_particle = header.np.random.randint(0, len(self.positions))
            dist = header.np.linalg.norm(self.box_arr.wrap(self.positions[random_particle]))
            
        # 'random_particle' is chosen, now the search will begin in order to find out the points connected via
        # \hat{a}, \hat{b} and \hat{c} direction at the minimum distances
        for v in range(len(self.LattVec)):
            if v not in LattVec_dummy_store or len(acc_id_lattvec)==0:
                v0 = [t/header.np.linalg.norm(t) for t in self.LattVec[v]]   # Unit lattice vectors
                particle_arr = [random_particle]
                particle_positions = [self.positions[random_particle].tolist()]
                
                # Collect three particles connected via lattice translational vectors \hat{a}, \hat{b} and \hat{c} direction at the minimum distances
                lattice_vec_arr, original_lattice_vec = [], []
                for director in range(len(v0)):
                    dummy_particle_arr = [j for j in range(num_particles) if j != random_particle]
                    vec_arr = [self.box_arr.wrap(self.positions[j] - self.positions[random_particle]) for j in range(num_particles) if j != random_particle]
                    d_arr = [header.np.linalg.norm(t) for t in vec_arr]
                    unit_vec_arr = [vec_arr[t]/d_arr[t] for t in range(len(vec_arr))]
                    selected_d_arr = [d_arr[t] for t in range(len(unit_vec_arr)) if header.np.rad2deg(header.np.arccos(round(header.np.dot(v0[director], unit_vec_arr[t]), 2))) <= self.angle_cutoff]
                    selected_vec_arr = [vec_arr[t] for t in range(len(unit_vec_arr)) if header.np.rad2deg(header.np.arccos(round(header.np.dot(v0[director], unit_vec_arr[t]), 2))) <= self.angle_cutoff]
                    selected_particle_arr = [dummy_particle_arr[t] for t in range(len(unit_vec_arr)) if header.np.rad2deg(header.np.arccos(round(header.np.dot(v0[director], unit_vec_arr[t]), 2))) <= self.angle_cutoff]

                    if len(selected_d_arr) >= 1:
                        min_d = header.np.min(selected_d_arr)
                        index = [i for i, e in enumerate(selected_d_arr) if e == min_d][0]
                        lattice_vec_arr.append(v0[director])
                        particle_arr.append(selected_particle_arr[index])
                        original_lattice_vec.append(selected_vec_arr[index])
                        particle_positions.append(self.positions[selected_particle_arr[index]].tolist())

                # print("Running !")
                check_counter = check_counter + 1
                if check_counter >= check_tol :
                    self.user_dec, done5 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Stop? (y/n)')
                    user_dec = self.user_dec
                    if user_dec == 'y':
                        check_bool = 1
                        break
                    else:
                        check_counter = 0

                # We get four corner points upto this step, now we will go for seraching other corner points
                if len(lattice_vec_arr) == 3 and len(particle_arr) == 4:
                    self.array = lattice_vec_arr[:]
                    self.modified_matrix = [t/header.np.linalg.norm(t) for t in self.array]
                    co = lattice_param_func(original_lattice_vec)
                    Lx, Ly, Lz, alpha, beta, gamma = co[0], co[1], co[2], co[3], co[4], co[5]
                    lattice_parameter = [Lx, Ly, Lz, alpha, beta, gamma]
                    lattice_parameter_print = [round(float(Lx), 3), round(float(Ly), 3), round(float(Lz), 3), round(float(alpha), 3), round(float(beta), 3), round(float(gamma), 3)]
                    self.abc = [Lx, Ly, Lz]
                    a = lattice_param.lattice_param_func_hoomd(original_lattice_vec)
                    self.uc_box_arr = header.freud.box.Box(Lx=a[0], Ly=a[1], Lz=a[2],
                                                        xy=a[6], xz=a[7], yz=a[8], is2D=False)
                    # Dummy print
                    print(random_particle, lattice_parameter_print, "Running ......")

                    # Checking the space group for each accepted vectors triplet
                    self.lv = lattice_parameter[:]
                    c = final_check_func(self)   # Check for crystal class
                    Lx, Ly, Lz, alpha, beta, gamma = self.lv[0], self.lv[1], self.lv[2], header.np.deg2rad(self.lv[3]), header.np.deg2rad(self.lv[4]), header.np.deg2rad(self.lv[5])
                    sq = 1-header.np.cos(alpha)*header.np.cos(alpha) - header.np.cos(beta)*header.np.cos(beta) - header.np.cos(gamma)*header.np.cos(gamma) + (2*header.np.cos(alpha)*header.np.cos(beta)*header.np.cos(gamma))
                    vol = round(Lx*Ly*Lz*header.np.sqrt(sq), 3)
                    # print(c)

                    if c == self.ty:
                        if v not in LattVec_dummy_store or len(acc_id_lattvec)==0:
                            particle_arr, particle_positions = get_another_particles(self, particle_arr, particle_positions, num_particles)   # All the particle for convex hull
                            self.global_particle_arr_per_lattvec = []
                            for p in particle_arr:
                                if p != -1:
                                    self.global_particle_arr_per_lattvec.append(self.chosen_particle_arr[p])
                                else:
                                    self.global_particle_arr_per_lattvec.append(-1)
                            if len(particle_positions) == 8:  # all corner particles are detected
                                center = header.np.average(header.np.array(particle_positions), axis=0)
                                positions_wrt_center = [(header.np.array(t) - center) for t in particle_positions]  # Translation in the local frame of UC

                                particle_positions = positions_wrt_center[:]
                                hull = header.ConvexHull(particle_positions)
                                self.volume = hull.volume
                                # Increase the volume little bit so that we can handle the noise in crystal 
                                self.increased_volume = self.volume + self.volume*self.vf  # Don't change it from 0.3, it is moderate
                                modified_particles_positions = calculate_the_vertices(self, particle_positions)

                                uc_particles_positions.append(particle_positions)  # Basic corner particles positions
                                uc_particles_arr.append(particle_arr)  # basic corner particles id
                                # LattVec_dummy_store.append(v)
                                center_arr.append(center)
                                self.global_particle_arr.append(self.global_particle_arr_per_lattvec)

                                self.arr = [header.np.array(particle_positions[t]) - header.np.array(particle_positions[0]) for t in range(1, 4)]
                                self.L = lattice_param_func(self.arr)
                                lattice_vec_array.append(self.arr)
                                # print(self.L, self.ty)
                                # Get the actual lattic evectors
                                self.abc = [self.L[0], self.L[1], self.L[2]]
                                lattice_vec = self.LattVec[v]  # Actual lattice vectors
                                # Get the unit cell vector
                                self.V_unit = header.np.array([lattice_vec[i]/header.np.linalg.norm(lattice_vec[i]) for i in range(len(lattice_vec))])
                                matrix = header.np.array(self.V_unit)

                                LattVec_arr.append(lattice_vec)
                                uc_vol.append(vol)

                                particle_positions = [t.tolist() for t in particle_positions]
                                particles_posi = self.positions[:] # Check for Bravais lattice --> positions of all particles in the Bravais lattice only
                                p = check_bravais(self, center, particle_positions, particles_posi, vol, modified_particles_positions, particle_arr, v, successful_v)
                                # Strictly it should pass the Bravais-chack, otherwise the algorithm will not move forward
                                if p != -1:
                                    LattVec_dummy_store.append(v)
                                    acc_id_lattvec.append(successful_v)

                                # acc_id_lattvec.append(successful_v) # Doesn't care structly whether it passes the Bravais-check or not
                                successful_v = successful_v +1

                                lattice_vec_count = lattice_vec_count + 1

        if check_bool == 1:
            break

    if len(uc_particles_positions) >= 1:
        return uc_particles_positions, uc_particles_arr, LattVec_arr, uc_vol, acc_id_lattvec, center_arr, lattice_vec_array, self.global_particle_arr

    else:
        print("WARNING : Please change the tolerance values in \"Global symmetry\" menu")
        return [], [], [], [], [], [], []

def get_uc_func(self):
    uc_particles_positions, uc_particles, lvector, ucvol, acc_id_lattvec, center_arr, lattice_vec_array, global_particle_arr = get_uc_particles(self)
    # choice = int(input("Enter your choice (int) :  "))   # The choise of the user for the particular triplet
    # particle_arr_positions, particles_arr, lv  = uc_particles_positions[choice], uc_particles[choice], lvector[choice]

    # Space group check of non-Bravais lattice with passed lattice vectors producing successful Bravais lattice
    particle_positions_uc, particles_arr_uc, basis_positions_uc = [], [], []
    acc_counter = 0
    if len(uc_particles_positions) >= 1:
        # print("Unit cells have been detected !")

        self.user_input_dec, done6 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Continue? (y/n)')

        user_input_dec = self.user_input_dec
        if user_input_dec == 'n':
            print("WARNING : Please recalculate \"Environment separation\" with extarnal tolerance values")
            if self.enable_tol_func == False:
                tol_func(self)

        elif user_input_dec == 'y':
            self.user_input, done7 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'UC choice? (int)')

            user_input = int(self.user_input)
            m1 = user_input
            self.test = 'test'  # when the choice of the triplet is not confirmed
            particle_arr_positions, particles_arr, lattice_vec, vol, center, self.lattice_vec_raw, global_particle_arr  = uc_particles_positions[m1], uc_particles[m1], lvector[m1], ucvol[m1], center_arr[m1], lattice_vec_array[m1], global_particle_arr[m1]


            # Check for the non-Bravais lattice
            hull = header.ConvexHull(particle_arr_positions)
            self.volume = hull.volume
            # Increase the volume little bit so that we can handle the noise in crystal 
            self.increased_volume = self.volume + self.volume*self.vf  # Don't change it from 0.3, it is moderate
            modified_particles_positions = calculate_the_vertices(self, particle_arr_positions)

            particle_arr_positions = [t.tolist() for t in particle_arr_positions]
            particles_posi = self.original_positions[:] # positions of all particles in the inital structure (either Bravais/non-Bravais)
            particle_arr_positions, particles_arr, nonbrav_particles = final_check_bravais_nonbravais(self, center, particle_arr_positions, particles_arr, particles_posi, modified_particles_positions) 

            for p in global_particle_arr:
                particles_arr_uc.append(p)
            for p in nonbrav_particles:
                particles_arr_uc.append(p)

            print("Unit cell particle ids : ", particles_arr_uc)
            self.particles_arr = particles_arr_uc[:]

            #**********************************************************************************
            '''self.particles_positions = [self.original_positions[t] for t in self.particles_arr]
            self.particles_positions = [(header.np.array(t) - header.np.average(header.np.array(self.particles_positions[:8]), axis=0)) for t in self.particles_positions]  # Reference frame  of UC'''
            self.particles_positions = particle_arr_positions[:]
            self.particles_verts = []
            self.particles_orientations = []
            self.particle_types = []
            for p in self.particles_arr:
                if p != -1:
                    self.particles_orientations.append(self.original_orientations[p])
                    self.particle_types.append(self.raw_typeid_arr_int[p])
                    if len(self.verts) != 0:
                        self.particles_verts.append(self.original_verts[p])
                    else:
                        self.particles_verts.append(header.np.array(self.r)) # Dummy speher radius
                else:
                    self.particles_orientations.append(header.np.array([1, 0, 0, 0]))
                    self.particle_types.append(len(self.typeid_arr_int))  # Imaginary particle id
                    if len(self.verts) != 0:
                        self.particles_verts.append(self.original_verts[p])
                    else:
                        self.particles_verts.append(header.np.array(self.r)) # Dummy speher radius

            # Categorizing the imaginary and real particles
            self.cat_particles_positions, self.cat_particles_orientations, self.cat_verts = [], [], []
            for t in range(len(self.particle_types)):
                indices = [g for g, e in enumerate(self.particle_types) if e == self.particle_types[t]]
                if len(indices) > 1:
                    sub_posi = [header.np.array(self.particles_positions[t]) for t in indices]
                    sub_orien = [self.particles_orientations[t] for t in indices]
                    self.cat_particles_positions.append(sub_posi)
                    self.cat_particles_orientations.append(sub_orien) 
                    if len(self.verts) != 0:
                        sub_verts = [self.particles_verts[t] for t in indices]  
                        self.cat_verts.append(sub_verts)

            if len(self.verts) != 0:
                # print(self.cat_verts)
                pass
            #*****************************************************************
            # Get the unit cell vector
            V_unit = header.np.array([lattice_vec[i]/header.np.linalg.norm(lattice_vec[i]) for i in range(len(lattice_vec))])
            matrix = header.np.array(V_unit)
            print("\n")
            print("*********************** Details of basis vectors ", acc_counter, "*****************************************")
            print(" ")
            print("Directions of the basis vectors : ", V_unit)
            print(" ")

            # print(matrix)
            # MATH : Global = Rot*Local; Rot = Global*Local^-1
            # Local = Rot^-1 * Global
            # I have to go from global to local frame
            base_matrix = header.np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            self.R = header.np.matmul(base_matrix, header.np.linalg.inv(matrix))
            self.q = header.rowan.from_matrix(self.R, require_orthogonal=False)
            print("Quaternion required to transform local to global frame : ", self.q)

            box_matrix = self.box_arr.to_matrix()
            #*****************************************************************
            # print(particle_arr_positions)
            # print(len(self.LattVec))
            arr = []
            if len(self.particles_positions) != 0:
                # print(real_particles_positions)
                arr = [self.box_arr.wrap(header.np.array(self.particles_positions[t]) - header.np.array(self.particles_positions[0])) for t in range(1, 4)]
                # print(arr)
                L = lattice_param_func(arr)
                print("Lattice parameters : ", L, "and Crystal class : ", self.ty)
                print(" ")
                abc = [L[0], L[1], L[2]]
                self.event_uc = None
                # print("Unit cell detected ......")

                #*************************SPACE GROUP INFORMATION***********************************"

                # This is to tackle the tolerances of spglib, otherwsie these loops do nothing
                sym_tol, angle_tol = [i/100 for i in range(1, 70, 1)], [i for i in range(1, 50, 1)]
                # the space group
                bool_a = 0
                bool_c = 0
                for s in sym_tol:
                    self.sym_tolerance = s
                    for a in angle_tol:
                        self.angle_tolerance = a
                        c1, c2, original_basis_positions = sg_spglib(self, self.particles_arr, self.particles_positions, V_unit, abc, L, arr) 
                        if self.sg_values[0] <= c1 <= self.sg_values[1]:
                            # print(c1)
                            bool_a = 1
                            break
                    if bool_a == 1:
                        bool_c = 1
                        break

                self.test = 'final'
                # the space group
                c1, c2, original_basis_positions = sg_spglib(self, self.particles_arr, self.particles_positions, V_unit, abc, L, arr)
                if c1 == 0:
                    print("No space group is detected")
                    print(" ")
                particle_positions_uc.append(self.particles_positions)
                # particles_arr_uc.append(particles_arr)
                basis_positions_uc.append(original_basis_positions)

                acc_counter = acc_counter + 1

            #************************************************************************************************
            self.sorted_color_arr = self.color_arr[:len(self.typeid_arr_int)]
            self.sorted_color_arr.append(header.pv.Color('0xbebebe', opacity=0.5)) # Color for imag particle
            self.sorted_types = list(set(self.particle_types))

            # Remove existing snapshot
            # Remove snapshot
            for p in self.added_mesh_arr:
                self.plotter.remove_actor(p) 
            
            self.plotter.remove_actor(self.sim_added_box)

            # Plot Unit cell
            self.added_mesh_arr = []
            if len(self.verts) != 0:
                for a in range(len(self.sorted_types)):
                    self.v_arr = []
                    self.poly_verts, self.spehere_posi, self.spehere_radius, self.part_types = [], [], [], []
                    for t1 in range(len(self.cat_particles_orientations[a])):
                        if isinstance(self.verts[t1], list) : # polyhedron
                            self.v_arr.append(header.np.array(self.cat_particles_positions[a][t1]) + header.rowan.rotate(self.cat_particles_orientations[a][t1], self.verts[t1]))
                            self.poly_verts.append(self.verts[t1])
                            self.part_types.append(self.original_typeid[t1])
                        elif isinstance(self.verts[t1], int) : # sphere
                            self.spehere_posi.append(self.cat_particles_positions[a][t1])
                            self.spehere_radius.append(self.verts[t1])

                    points = list(header.chain.from_iterable(self.v_arr))
                    polyhedron_connectivity = []
                    for i in range(len(self.v_arr)):
                        sub_arr = []
                        poly = header.coxeter.shapes.ConvexPolyhedron(self.poly_verts[i])
                        faces = poly.faces
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
                    celltypes = [header.pv.CellType.POLYHEDRON for _ in range(len(self.v_arr))]
                    self.ungrid = header.pv.UnstructuredGrid(cells, celltypes, points)
                    self.added_mesh = self.plotter.add_mesh(self.ungrid, show_edges=True, line_width=1, color=self.sorted_color_arr[a], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                    self.added_mesh_arr.append(self.added_mesh)

                if len(self.spehere_posi) > 1:
                    self.added_mesh = self.plotter.add_points(self.spehere_posi, render_points_as_spheres=True, point_size=self.spehere_radius[0], color=header.pv.Color('0x3ba099'), lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                    self.added_mesh_arr.append(self.added_mesh)

            else:
                for a in range(len(self.sorted_types)):
                    self.added_mesh = self.plotter.add_points(header.np.array(self.cat_particles_positions[a]), render_points_as_spheres=True, point_size=5*self.r, color=self.color_arr[a], lighting=True, specular=1.0, specular_power=1.0, ambient=0.5)
                    self.added_mesh_arr.append(self.added_mesh)

            #******************************************************
            # Unit cell box info
            box_points = header.np.array(self.particles_positions[:8])
            box_faces = [[0, 1, 4, 3], [1, 6, 7, 4], [6, 2, 5, 7], [2, 0, 3, 5], [0, 1, 6, 2], [3, 4, 7, 5]]
            modified_box_faces = []
            for b in box_faces:
                modified_box_faces.append(len(b))
                for a in b:
                    modified_box_faces.append(a)

            self.mesh = header.pv.PolyData(box_points, modified_box_faces)
            visibleEdges = self.mesh.extract_feature_edges()
            self.added_box = self.plotter.add_mesh(visibleEdges, color='k', line_width=5)
            # light = header.pv.Light(color=self.c, light_type='headlight')
            # self.plotter.add_light(light)
            self.plotter.reset_camera()
            self.plotter.update()
            #*****************************************************************

            # BOD
            # Remove arrow widget
            self.grid.removeWidget(self.canvas_bod)
            self.ax_bod.remove()
            self.canvas_bod.deleteLater()

            self.figure_bod = header.Figure(figsize=(2.5, 2))
            self.ax_bod = self.figure_bod.add_subplot(111, projection="3d")
            self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)

            self.position_arr = header.np.array(self.original_position_arr[:])

            x, y, z = self.r_data[:,0], self.r_data[:,1], self.r_data[:,2]
            # Scatter plot in 3D
            self.ax_bod.scatter(x, y, z, c='r', s=7.0)

            # Polyhedron
            for s in self.faces:
                tri = header.Poly3DCollection([header.np.array([self.r_data[t] for t in s])])
                tri.set_color('darkgrey')
                tri.set_alpha(0.5)
                self.ax_bod.add_collection3d(tri)

            x, y, z = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            u, v, w = [lattice_vec[0], lattice_vec[1], lattice_vec[2]]
            self.ax_bod.quiver(0, 0, 0, lattice_vec[0][0], lattice_vec[0][1], lattice_vec[0][2], lw=2, length=1.5, colors='r')
            self.ax_bod.quiver(0, 0, 0, lattice_vec[1][0], lattice_vec[1][1], lattice_vec[1][2], lw=2, length=1.5, colors='b')
            self.ax_bod.quiver(0, 0, 0, lattice_vec[2][0], lattice_vec[2][1], lattice_vec[2][2], lw=2, length=1.5, colors='g')

            self.ax_bod.set_axis_off()
            self.ax_bod.set_title("BOD", fontsize=6)
            view_angle = 0, 0   # View from elevation=0 and azimuthal=0 
            self.ax_bod.view_init(*view_angle)
            self.ax_bod.set_box_aspect((self.rcut, self.rcut, self.rcut), zoom=1.3)
            self.figure_bod.tight_layout()
            self.canvas_bod.draw()

            # Zoom and pan
            ph = header.panhandler(self.figure_bod, button=3)  # pan with right mouse button
            header.zoom_factory(self.ax_bod)

            self.grid.addWidget(self.canvas_bod, 2, 0)

            # Quick screenshot
            self.sshot_action = header.QtWidgets.QAction('Quick screenshot', self)
            self.sshot_action.triggered.connect(lambda:save_screenshot_func(self))
            self.fileMenu.addAction(self.sshot_action)

            #********************* Save as speheres *****************************************
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

            '''self.save_action = header.QAction("&Save UC", self)
            self.save_action.triggered.connect(lambda:save_uc_func(self))
            self.ucMenu.addAction(self.save_action)'''

            self.savebasis_action = header.QAction("&Save effective sites", self)
            self.savebasis_action.triggered.connect(lambda:save_basis_func(self))
            self.ucMenu.addAction(self.savebasis_action)

            self.clear_action = header.QAction("&Clear", self)
            self.clear_action.triggered.connect(lambda:clear_plot_func(self))
            self.ucMenu.addAction(self.clear_action)

    else:
        print("WARNING : No unit cell is detected. Please enter valid inputs and recalculate !")

# Equivalent lattice sites
def equivalent_points(self, uc_pts):
    if len(uc_pts) > 8:
        corner_pts = uc_pts[:8]
        # Decorating the non-corner ponits based on distance from a reference point
        noncorner_pts = uc_pts[8:]
        corner_pts_wrt_ref = [header.np.array(corner_pts[t]) - header.np.array(uc_pts[0]) for t in range(0, len(corner_pts))]
        noncorner_pts_wrt_ref = [header.np.array(noncorner_pts[t]) - header.np.array(uc_pts[0]) for t in range(0, len(noncorner_pts))]
        center_wrt_ref = header.np.average(header.np.array(corner_pts_wrt_ref), axis=0)
        dist_arr = [header.np.linalg.norm(header.np.array(noncorner_pts_wrt_ref[t]) - header.np.array(uc_pts[0])) for t in range(0, len(noncorner_pts_wrt_ref))]
        unsorted_dist_arr = dist_arr[:]
        dist_arr.sort() # smaller to larger distance
        modified_noncorner_pts = []
        for t in range(len(dist_arr)):
            indices = [i for i, e in enumerate(unsorted_dist_arr) if e == dist_arr[t]]
            for u in indices:
                if len(modified_noncorner_pts) != len(noncorner_pts_wrt_ref):
                    modified_noncorner_pts.append(noncorner_pts_wrt_ref[u].tolist())

        angle_tol = self.angle_cutoff
        # Choosing the basis
        basis_positions = [corner_pts_wrt_ref[0].tolist()]
        basis_ids = [0]
        connected_positions = []
    
        posi = modified_noncorner_pts[:]
        if len(posi) > 0:
            for i in range(len(posi)):
                count = 0
                for j in range(len(basis_positions)):
                    vec = header.np.array(basis_positions[j]) - header.np.array(posi[i])
                    if header.np.linalg.norm(vec) != 0:
                        unit_vec = vec/header.np.linalg.norm(vec)
                        d = header.np.linalg.norm(vec)
                        angle0 = header.np.rad2deg(header.np.arccos(round(header.np.dot(self.V_unit[0], unit_vec), 3)))
                        angle1 = header.np.rad2deg(header.np.arccos(round(header.np.dot(self.V_unit[1], unit_vec), 3)))
                        angle2 = header.np.rad2deg(header.np.arccos(round(header.np.dot(self.V_unit[2], unit_vec), 3)))

                        counter = 0
                        if angle0 <= angle_tol or angle0>= (180-angle_tol) or angle1 <= angle_tol or angle1>= (180-angle_tol) or angle2 <= angle_tol or angle2>= (180-angle_tol):
                            if  (self.abc[0]-self.dist_cutoff) < d <= (self.abc[0]+self.dist_cutoff) or (self.abc[1]-self.dist_cutoff) < d <= (self.abc[1]+self.dist_cutoff) or (self.abc[2]-self.dist_cutoff) < d <= (self.abc[2]+self.dist_cutoff):
                                continue
                            else:
                                counter = counter + 1
                        else:
                            counter = counter + 1

                        if counter == 1:
                            count = count + 1
                if count == len(basis_positions):
                    '''if posi[i] not in basis_positions:
                        #***************************************************************************
                        count = 0
                        for j in range(len(connected_positions)):
                            vec = header.np.array(connected_positions[j]) - header.np.array(posi[i])
                            unit_vec = vec/header.np.linalg.norm(vec)
                            d = header.np.linalg.norm(vec)
                            angle0 = header.np.rad2deg(header.np.arccos(round(header.np.dot(self.V_unit[0], unit_vec), 3)))
                            angle1 = header.np.rad2deg(header.np.arccos(round(header.np.dot(self.V_unit[1], unit_vec), 3)))
                            angle2 = header.np.rad2deg(header.np.arccos(round(header.np.dot(self.V_unit[2], unit_vec), 3)))

                            counter = 0
                            if angle0 <= angle_tol or angle0>= (180-angle_tol) or angle1 <= angle_tol or angle1>= (180-angle_tol) or angle2 <= angle_tol or angle2>= (180-angle_tol):
                                if  (self.abc[0]-self.dist_cutoff) < d <= (self.abc[0]+self.dist_cutoff) or (self.abc[1]-self.dist_cutoff) < d <= (self.abc[1]+self.dist_cutoff) or (self.abc[2]-self.dist_cutoff) < d <= (self.abc[2]+self.dist_cutoff):
                                    counter = counter + 1
                            if counter == 1:
                                break
                            else:
                                count = count + 1
                        if count == len(connected_positions):         
                            basis_positions.append(posi[i])'''
                        
                    #***************************************************************************
                    basis_positions.append(posi[i])
                '''else:
                    connected_positions.append(posi[i])'''

    else:
        corner_pts = uc_pts[:8]
        corner_pts_wrt_ref = [header.np.array(corner_pts[t]) - header.np.array(uc_pts[0]) for t in range(0, len(corner_pts))]
        center_wrt_ref = header.np.average(header.np.array(corner_pts_wrt_ref), axis=0)
        basis_positions = [corner_pts_wrt_ref[0].tolist()]

    equiv_pts = [(header.np.array(t)-center_wrt_ref).tolist() for t in basis_positions]

    return equiv_pts

# Space group indfo using spglib package
def sg_spglib(self, particles_arr, particle_arr_positions, V_unit, abc, L, arr):
    angle_tol = self.angle_cutoff

    # Choosing the basis
    if len(particle_arr_positions) > 8:
        corner_pts = particle_arr_positions[:8]
        noncorner_pts = particle_arr_positions[8:]
        # Decorating the non-corner ponits based on distance from a reference point
        corner_pts_wrt_ref = [header.np.array(corner_pts[t]) - header.np.array(particle_arr_positions[0]) for t in range(0, len(corner_pts))]
        noncorner_pts_wrt_ref = [header.np.array(noncorner_pts[t]) - header.np.array(particle_arr_positions[0]) for t in range(0, len(noncorner_pts))]
        center_wrt_ref = header.np.average(header.np.array(corner_pts_wrt_ref), axis=0)
        dist_arr = [header.np.linalg.norm(header.np.array(noncorner_pts_wrt_ref[t]) - header.np.array(particle_arr_positions[0])) for t in range(0, len(noncorner_pts_wrt_ref))]
        unsorted_dist_arr = dist_arr[:]
        unsorted_noncorner_ids = [self.raw_typeid_arr_int[m] for m in self.particles_arr[8:]]
        dist_arr.sort() # smaller to larger distance
        modified_noncorner_pts, sorted_noncorner_ids = [], []
        for t in range(len(dist_arr)):
            indices = [i for i, e in enumerate(unsorted_dist_arr) if e == dist_arr[t]]
            for u in indices:
                if len(modified_noncorner_pts) != len(noncorner_pts_wrt_ref):
                    modified_noncorner_pts.append(noncorner_pts_wrt_ref[u].tolist())
                    sorted_noncorner_ids.append(unsorted_noncorner_ids[u])

        angle_tol = self.angle_cutoff
        # Choosing the basis
        posi = modified_noncorner_pts[:]
    
        # some modifications of positions
        self.all_uc_positions = [t for t in corner_pts_wrt_ref]
        for t in noncorner_pts_wrt_ref:
            self.all_uc_positions.append(t)

        self.all_uc_positions_wrt_center = self.all_uc_positions - center_wrt_ref

        # print(sorted_noncorner_ids)

        basis_positions = [corner_pts_wrt_ref[0].tolist()]
        self.basis_id = [self.raw_typeid_arr_int[self.particles_arr[0]]]
        connected_positions = []
        if len(posi) > 0:
            for i in range(len(posi)):
                count = 0
                for j in range(len(basis_positions)):
                    vec = header.np.array(basis_positions[j]) - header.np.array(posi[i])
                    if header.np.linalg.norm(vec) != 0:
                        unit_vec = vec/header.np.linalg.norm(vec)
                        d = header.np.linalg.norm(vec)
                        angle0 = header.np.rad2deg(header.np.arccos(round(header.np.dot(V_unit[0], unit_vec), 3)))
                        angle1 = header.np.rad2deg(header.np.arccos(round(header.np.dot(V_unit[1], unit_vec), 3)))
                        angle2 = header.np.rad2deg(header.np.arccos(round(header.np.dot(V_unit[2], unit_vec), 3)))

                        counter = 0
                        if angle0 <= angle_tol or angle0>= (180-angle_tol) or angle1 <= angle_tol or angle1>= (180-angle_tol) or angle2 <= angle_tol or angle2>= (180-angle_tol):
                            if  (abc[0]-self.dist_cutoff) < d <= (abc[0]+self.dist_cutoff) or (abc[1]-self.dist_cutoff) < d <= (abc[1]+self.dist_cutoff) or (abc[2]-self.dist_cutoff) < d <= (abc[2]+self.dist_cutoff):
                                continue
                            else:
                                counter = counter + 1
                        else:
                            counter = counter + 1

                        if counter == 1:
                            count = count + 1
                if count == len(basis_positions):
                    basis_positions.append(posi[i])
                    self.basis_id.append(sorted_noncorner_ids[i])
            
    else:
        corner_pts = particle_arr_positions[:8]
        corner_pts_wrt_ref = [header.np.array(corner_pts[t]) - header.np.array(particle_arr_positions[0]) for t in range(0, len(corner_pts))]
        center_wrt_ref = header.np.average(header.np.array(corner_pts_wrt_ref), axis=0)
        basis_positions = [corner_pts_wrt_ref[0].tolist()]
        self.basis_id = [self.particles_arr[0]]

    # print(basis_id)

    original_basis_positions = [(header.np.array(t)-center_wrt_ref).tolist() for t in basis_positions]
    self.original_basis_positions = original_basis_positions[:]
    # Basis
    self.basis_positions = [(header.np.array(t)-header.np.array(basis_positions[0])) for t in basis_positions]
    a, b, c, alpha, beta, gamma = L[0], L[1], L[2], header.np.deg2rad(L[3]), header.np.deg2rad(L[4]), header.np.deg2rad(L[5])

    arr = [t.tolist() for t in arr]
    # Lattice
    lattice = header.np.matrix(arr)
    # Bais fractional coordinates
    positions = [header.np.matmul(header.np.linalg.inv(lattice.T), t).tolist() for  t in basis_positions]
    positions = [t[0] for t in positions]   # important
    # print(len(positions))
    lattice = [t[0].tolist() for t in lattice]   # important
    lattice = [t[0] for t in lattice]   # important
    # numbers = [0 for i in range(len(positions))]
    numbers = self.basis_id[:]
    cell = (lattice, positions, numbers)
    # All crystallographic symmetry including translation can be achieved by SPGLIB package
    symmetry = header.spglib.get_symmetry(cell, symprec=self.sym_tolerance, angle_tolerance=self.angle_tolerance)
    # print(symmetry)
    # print(len(symmetry['rotations']) + len(symmetry['translations']))
    # Spacegroup using SPGLIB
    if symmetry != None:
        # cell = header.spglib.standardize_cell(cell, to_primitive=False, no_idealize=True, symprec=self.sym_tolerance, angle_tolerance=self.angle_tolerance)
        if cell != None:
            lattice = list(cell)[0]
            spacegroup = header.spglib.get_spacegroup_type_from_symmetry(rotations=symmetry['rotations'], translations=symmetry['translations'], lattice=lattice)
            # print(positions)
            # print(symmetry)
            # print(len(symmetry['rotations']) + len(symmetry['translations']))
            if self.test == 'final':
                if self.sg_values[0] <= spacegroup['number'] <= self.sg_values[1]:
                    print("Lattice vectors : ", lattice)
                    print(" ")
                    # print("Equiv points : ", positions)
                    print("Number of effective particles : ", len(positions))
                    print(" ")
                    print("Spacegroup : ", spacegroup['number'], spacegroup['international_short'])
                    print(" ")
                    # print(len(symmetry['rotations']))
                    # print(len(symmetry['rotations']) + len(symmetry['translations']))
                else:
                    print("No space group is detected")

            return spacegroup['number'], len(positions), original_basis_positions    
        else:
            # print("No space group is detected")
            return 0, 0, []
    else:
        # print("No space group is detected")
        return 0, len(positions), original_basis_positions