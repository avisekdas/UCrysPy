# Calculate the positional distribution in 3D of the neaighbors within cerain distance; i.e., BOD
# Will be effective once RDF is done

# INPUTS : all system coordinates, distance ~ minima of RDF, RDF values, RDF bin centers

import header
from kmeans import kmeans_func
from save_kmeans import save_kmeans_func
from clear_kmeans import clear_kmeans_func

def bod_func(self):
    """ Calculates the Bond orientational order diagram (BOD) based on the input particle cooridnates
        and simulation box

        It checks whether the RDF is calculated successfully and estimates the neighborlist of all 
        particles in the system within certain cutoff distance using Freud

        Activates the K-Means menu for the next step

        Return
        ------
        coor_num : int
                    Cooridnation number per particle

        position_arr : list ([NM X 3])
                     Relative position vectors within the cutoff distance with respect to each particle in the system
                     in a 2D-list
                     
        separation_arr : list ([N X M X 3])  
                     Relative position vectors within the cutoff distance with respect to each particle in the system
                     in a 3D-list per particle

        neighbor_li : list ([N X M])
                    Neighbor ids for each particle in a 2D-list
    
    """
    if self.rdf_satisfied == 1 and self.bod_satisfied == 0:
        # Coordiantion number; not much important in this context
        self.f_positions = []
        self.rdf_values  = []
        for i in range(len(self.RDF.bin_centers)):
            self.f_positions.append(self.RDF.bin_centers[i])
            self.rdf_values.append(self.RDF.rdf[i])

        j_end = 0
        for i in range(0, len(self.rdf_values)):
            if self.f_positions[i] <= self.rcut:
                continue
            else:
                j_end = i
                break

        j_start = 0
        for i in range(0, len(self.rdf_values)):
            if self.f_positions[i] <= self.rmin:
                continue
            else:
                j_start = i
                break

        self.rm = self.f_positions[j_end]   # distance of first minima
        self.coord_num = self.RDF.n_r[j_end] - self.RDF.n_r[j_start]  # Cordination number
        self.coord_num = round(self.coord_num)
        # print("Coordination number : ", self.coord_num)
        #************************************************
        
        # Relative positional vectors of all the neighbors of the points within the distance 
        self.position_arr = []
        self.query_result = self.aq.query(self.positions, dict(r_min=self.rmin, r_max=self.rcut, exclude_ii=True))
        # self.query_result = self.aq.query(self.positions, dict(num_neighbors=self.coord_num, exclude_ii=True))
        self.nlist = self.query_result.toNeighborList()
        self.separation_arr = [[] for _ in range(len(self.positions))]
        self.neighbor_li = [[] for _ in range(len(self.positions))]
        for (i, j) in self.nlist:
            vec = self.box_arr.wrap(self.positions[j] - self.positions[i])
            d = header.np.linalg.norm(vec)
            self.position_arr.append(vec)
            self.separation_arr[i].append(vec)
            self.neighbor_li[i].append(j)

        if self.env_sep_iteration == 0:
            self.original_position_arr = self.position_arr[:]
        self.position_arr = header.np.array(self.position_arr[:])
        x, y, z = self.position_arr[:,0], self.position_arr[:,1], self.position_arr[:,2]
        self.x, self.y, self.z = x, y, z
        #************************************************
        # Show bod on window
        if self.canvas_bod:
            self.grid.removeWidget(self.canvas_bod)
            self.canvas_bod.deleteLater()
            self.figure_bod = header.Figure(figsize=(self.w, self.h))

        self.ax_bod = self.figure_bod.add_subplot(111, projection="3d")
        self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)

        # Scatter plot in 3D
        '''self.ax_bod.scatter(x, y, z, c=self.c, s=0.5)
        self.ax_bod.set_axis_off()
        self.ax_bod.set_box_aspect((self.rcut, self.rcut, self.rcut), zoom=1.3)'''

        #*******************************************************************
        # Draw BOD on sphere
        n_bins_theta = 100
        n_bins_phi = 100
        bod = header.freud.environment.BondOrder((n_bins_theta, n_bins_phi))

        phi = header.np.linspace(0, header.np.pi, n_bins_phi)
        theta = header.np.linspace(0, 2 * header.np.pi, n_bins_theta)
        phi, theta = header.np.meshgrid(phi, theta)
        xx = header.np.sin(phi) * header.np.cos(theta)
        yy = header.np.sin(phi) * header.np.sin(theta)
        zz = header.np.cos(phi)

        # Define the colors
        colors = [(1, 1, 1, 0), (0.3, 0, 0, 0.85)]  # Transparent to dark-color

        # Create a custom colormap
        cmap = header.mcolors.LinearSegmentedColormap.from_list('mycmap', colors)

        self.bod_array = bod.compute(system=(self.box_arr, self.positions), neighbors={"r_min": self.rmin, "r_max": self.rcut, "exclude_ii": True}).bond_order
        self.bod_array = header.np.clip(self.bod_array, 0, header.np.percentile(self.bod_array, 95))
        self.ax_bod.plot_surface(xx, yy, zz, rstride=1, cstride=1, shade=False, facecolors=cmap(self.bod_array / header.np.max(self.bod_array)),  alpha=0.1)
        self.ax_bod.set_xlim(-1, 1)
        self.ax_bod.set_ylim(-1, 1)
        self.ax_bod.set_zlim(-1, 1)
        self.ax_bod.set_axis_off()
        self.ax_bod.set_aspect('equal')
        view_angle = 0, 45
        self.ax_bod.view_init(*view_angle)
        #*******************************************************************

        self.figure_bod.tight_layout()
        self.canvas_bod.draw()

        self.ax_bod.set_title("BOD", fontsize=6)
        self.grid.addWidget(self.canvas_bod, 2, 0)

        self.bod_satisfied = 1   # BOD is calculated

        # Zoom and pan
        ph = header.panhandler(self.figure_bod, button=3)  # pan with right mouse button
        header.zoom_factory(self.ax_bod)
        self.position_arr = [t.tolist() for t in self.position_arr]

        #******************************************************************************
        # Activate K-Means
        if self.bod_state == 0:
            def get_cmin(a):
                self.cmin = int(a.text())
            
            def get_cmax(a):
                self.cmax = int(a.text())

            self.cmin_submenu = self.kmeansMenu.addMenu('c_min')

            c = 0
            start, end, width = self.data["cmin_min"], self.data["cmin_max"], self.data["cmin_count"]   # Change the limit if necessary
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
                cmin_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.cmin_subsubmenu = self.cmin_submenu.addMenu(str(int(c_start)) + " - " + str(int(cmin_arr[-1])))
                for r in cmin_arr:
                    self.cmin_subsubmenu.addAction(str(int(r)))
                self.cmin_subsubmenu.triggered[header.QAction].connect(get_cmin)

            self.cmax_submenu = self.kmeansMenu.addMenu('c_max')
            c = 0
            start, end, width = self.data["cmax_min"], self.data["cmax_max"], self.data["cmax_count"]   # Change the limit if necessary
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
                cmax_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.cmax_subsubmenu = self.cmax_submenu.addMenu(str(int(c_start)) + " - " + str(int(cmax_arr[-1])))
                for r in cmax_arr:
                    self.cmax_subsubmenu.addAction(str(int(r)))
                self.cmax_subsubmenu.triggered[header.QAction].connect(get_cmax)

            self.go_action = header.QAction("&Go", self)
            self.go_action.triggered.connect(lambda:kmeans_func(self))
            self.kmeansMenu.addAction(self.go_action)

            self.save_action = header.QAction("&Save", self)
            self.save_action.triggered.connect(lambda:save_kmeans_func(self))
            self.kmeansMenu.addAction(self.save_action)

            self.clear_action = header.QAction("&Clear", self)
            self.clear_action.triggered.connect(lambda:clear_kmeans_func(self))
            self.kmeansMenu.addAction(self.clear_action)

            self.bod_state = self.bod_state + 1
            self.kemans_state = 0

    else:
        raise Exception("WARNING : RDF is not calculated or please clear the current one moving forward")

