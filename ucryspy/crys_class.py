import header

from calc_equiv_points_poly import calc_equiv_points_poly_func
from symm import symm_func
from make_xyz import make_xyz_func

from scipy.spatial import ConvexHull, Delaunay, cKDTree
from collections import Counter, defaultdict, deque, namedtuple
from itertools import chain
from scipy.sparse.csgraph import connected_components

from get_posi_orien_local_frame import get_posi_orien_local_frame_func
from lattice_param import lattice_param_func
from get_uc import get_uc_func

from collections import Counter, defaultdict, deque, namedtuple
from itertools import chain


def convexHull(vertices, tol):
    """Compute the 3D convex hull of a set of vertices and merge coplanar faces.

    Args:
        vertices (list): List of (x, y, z) coordinates
        tol (float): Floating point tolerance for merging coplanar faces


    Returns an array of vertices and a list of faces (vertex
    indices) for the convex hull of the given set of vertice.

    .. note::
        This method uses scipy's quickhull wrapper and therefore requires scipy.

    """

    hull = ConvexHull(vertices);
    # Triangles in the same face will be defined by the same linear equalities
    dist = cKDTree(hull.equations);
    trianglePairs = dist.query_pairs(tol);

    connectivity = header.np.zeros((len(hull.simplices), len(hull.simplices)), dtype=header.np.int32);

    for (i, j) in trianglePairs:
        connectivity[i, j] = connectivity[j, i] = 1;

    # connected_components returns (number of faces, cluster index for each iheader.nput)
    (_, joinTarget) = connected_components(connectivity, directed=False);
    faces = defaultdict(list);
    norms = defaultdict(list);
    for (idx, target) in enumerate(joinTarget):
        faces[target].append(idx);
        norms[target] = hull.equations[idx][:3];

    # a list of sets of all vertex indices in each face
    faceVerts = [set(hull.simplices[faces[faceIndex]].flat) for faceIndex in sorted(faces)];
    # normal vector for each face
    faceNorms = [norms[faceIndex] for faceIndex in sorted(faces)];

    # polygonal faces
    polyFaces = [];
    for (norm, faceIndices) in zip(faceNorms, faceVerts):
        face = header.np.array(list(faceIndices), dtype=header.np.uint32);
        N = len(faceIndices);

        r = hull.points[face];
        rcom = header.np.mean(r, axis=0);

        # plane_{a, b}: basis vectors in the plane
        plane_a = r[0] - rcom;
        plane_a /= header.np.sqrt(header.np.sum(plane_a**2));
        plane_b = header.np.cross(norm, plane_a);

        dr = r - rcom[header.np.newaxis, :];

        thetas = header.np.arctan2(dr.dot(plane_b), dr.dot(plane_a));

        sortidx = header.np.argsort(thetas);

        face = face[sortidx];
        polyFaces.append(face);

    return (hull.points, polyFaces);

ConvexDecomposition = namedtuple('ConvexDecomposition', ['vertices', 'edges', 'faces'])

def convexDecomposition(vertices, tol):
    """Decompose a convex polyhedron specified by a list of vertices into
    vertices, faces, and edges. Returns a ConvexDecomposition object.
    """
    (vertices, faces) = convexHull(vertices, tol)
    edges = set()

    for face in faces:
        for (i, j) in zip(face, header.np.roll(face, -1)):
            edges.add((min(i, j), max(i, j)))

    return ConvexDecomposition(vertices, edges, faces)

def crys_class_func(self):
    if self.kmeans_satisfied == 1:
        # getting few entries, nothing serious, just variable change
        self.dist_cutoff = self.rtol
        self.angle_cutoff = self.atol
        self.n_clusters = self.elbow

        # Fitting the positions to the cluster
        model = header.KMeans(n_clusters=self.n_clusters, init='k-means++', n_init='auto', random_state=0)
        pred = model.fit_predict(self.position_arr)
        cluster_labels = pred
        # print(cluster_labels)
        centroid=model.cluster_centers_
        cluster_centers = centroid[:]
        cluster_centers = cluster_centers[:]
        inertia = model.inertia_
        labels =  model.labels_

        self.cluster_centers = header.np.array(cluster_centers)
        self.cluster_centers = self.cluster_centers.tolist()
        self.vertices_clusters = self.cluster_centers[:]

        #***********************************************************************

        # Write XYZ file with the positions with neighbors after detecting the center of clusters
        # Not required here
        # make_xyz_func(self.vertices_clusters)

        # Convex decomposition technique of 'Euclid packgae'
        # Get all the non-unit vectors joing the geometric center of the polyhedron and the vertcies, face mid-points and egde mid-points
        '''tol_arr = [1/i for i in range(10, 1000, 50)]
        edges_arr, faces_arr = [], []
        for tol in tol_arr:
            convex_decomp = convexDecomposition(self.vertices_clusters, tol)
            edges = convex_decomp[1]
            faces = convex_decomp[2]
            edges_arr.append(edges)
            faces_arr.append(faces)

        sum_fev_arr = [(len(list(edges_arr[t])) + len(faces_arr[t]) + len(self.vertices_clusters)) for t in range(len(edges_arr))]
        print(sum_fev_arr)
        sum_fev_arr_sorted = header.np.argsort(sum_fev_arr)
        self.faces, self.edges = faces_arr[sum_fev_arr_sorted[0]], edges_arr[sum_fev_arr_sorted[0]]
        self.tolerance = tol_arr[sum_fev_arr_sorted[0]]
        print(self.tolerance)'''

        tol = self.rtol
        convex_decomp = convexDecomposition(self.vertices_clusters, tol)
        self.edges = convex_decomp[1]
        self.faces = convex_decomp[2]

        '''poly = header.coxeter.shapes.ConvexPolyhedron(self.vertices_clusters)
        self.edges, self.faces = poly.edges, poly.faces'''

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

            # Deactivate Environment separation menu
            self.envsepMenu.clear()

            # Deactivate Crystal class submenu
            self.classMenu.clear()

            if self.counter == 0:
                # Activate UC detection
                def get_distc(a):
                    self.dist_cutoff = float(a.text())

                self.distc_submenu = self.ucMenu.addMenu('dist tol')
                c = 0
                start, end, width = self.data["distc_min"], self.data["distc_max"], self.data["distc_count"]  # Change the limit if necessary
                num = (end - start)/width
                per_submenu = 30
                num_submenu = int(num/per_submenu) + 1
                g = 100
                c_end = 0
                self.distc_subsubmenu = self.distc_submenu.addMenu('Ideal crystal')
                self.distc_subsubmenu.addAction(str(0.00001))
                self.distc_subsubmenu.triggered[header.QAction].connect(get_distc)
                for c in range(num_submenu):
                    if c == 0:
                        c_start = start
                    else:
                        c_start = c_end
                    c_end = round(c_start  + width*per_submenu, 2)
                    distc_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                    self.distc_subsubmenu = self.distc_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(distc_arr[-1],2)))
                    for r in distc_arr:
                        self.distc_subsubmenu.addAction(str(r))
                    self.distc_subsubmenu.triggered[header.QAction].connect(get_distc)

                def get_anglec(a):
                    self.angle_cutoff = float(a.text())

                self.anglec_submenu = self.ucMenu.addMenu('angle tol')
                c = 0
                start, end, width = self.data["anglec_min"], self.data["anglec_max"], self.data["anglec_count"]  # Change the limit if necessary
                num = (end - start)/width
                per_submenu = 10
                num_submenu = int(num/per_submenu) + 1
                g = 100
                c_end = 0
                self.anglec_subsubmenu = self.anglec_submenu.addMenu('Ideal crystal')
                self.anglec_subsubmenu.addAction(str(0.00001))
                self.anglec_subsubmenu.triggered[header.QAction].connect(get_anglec)
                for c in range(num_submenu):
                    if c == 0:
                        c_start = start
                    else:
                        c_start = c_end
                    c_end = round(c_start  + width*per_submenu, 2)
                    anglec_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                    self.anglec_subsubmenu = self.anglec_submenu.addMenu(str(round(anglec_arr[0],2)) + " - " + str(round(anglec_arr[-1],2)))
                    for r in anglec_arr:
                        self.anglec_subsubmenu.addAction(str(r))
                    self.anglec_subsubmenu.triggered[header.QAction].connect(get_anglec)

                def get_vfactor(a):
                    self.vf = float(a.text())

                self.vfactor_submenu = self.ucMenu.addMenu('v_factor')
                c = 0
                start, end, width = self.data["vfactor_min"], self.data["vfactor_max"], self.data["vfactor_count"]  # Change the limit if necessary
                num = (end - start)/width
                per_submenu = 10
                num_submenu = int(num/per_submenu) + 1
                g = 100
                c_end = 0
                for c in range(num_submenu):
                    if c == 0:
                        c_start = start
                    else:
                        c_start = c_end
                    c_end = round(c_start  + width*per_submenu, 2)
                    vfactor_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                    self.vfactor_subsubmenu = self.vfactor_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(vfactor_arr[-1],2)))
                    for r in vfactor_arr:
                        self.vfactor_subsubmenu.addAction(str(r))
                    self.vfactor_subsubmenu.triggered[header.QAction].connect(get_vfactor)

                self.go_action = header.QAction("&Go", self)
                self.go_action.triggered.connect(lambda:get_uc_func(self))
                self.ucMenu.addAction(self.go_action)

                self.counter = self.counter + 1

            else:
                print("WARNING : No crystal class has been detected !")
                print("**************************************************************************************************************")
                print("* DISCLAIMER : In case the detected crystal class is TRICLINIC, please try once by changing the tolerances ! *")
                print("**************************************************************************************************************")
                if self.enable_tol_func == False:
                    tol_func(self)
    else:
        raise Exception("Kmeans is not calculated")

        # Activate envsepMenu
        '''def get_decision(a):
            self.user_input_dec = str(a.text())

        avg_action = self.envsepMenu.addMenu("Continue")
        dec_arr = ['y', 'n']
        for dec in dec_arr:
                avg_action.addAction(str(dec))
        avg_action.triggered[header.QAction].connect(get_decision)

        self.go_action = header.QAction("&Go", self)
        self.go_action.triggered.connect(lambda:uc_detection_func(self))
        self.envsepMenu.addAction(self.go_action)'''

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

    self.enable_tol_func = True

# Unit cell detection function
def uc_detection_func(self):
    user_input_dec = self.user_input_dec
    if user_input_dec == 'n':
        print("WARNING : Please recalculate \"Environment separation\" with extarnal tolerance values")
        if self.enable_tol_func == False:
            tol_func(self)
    elif user_input_dec == 'y':
        print("Let's check whether any valid unit cells are obtained with these choices !")

        # Deactivate Environment separation menu
        self.envsepMenu.clear()

        # Deactivate Crystal class submenu
        self.classMenu.clear()

        if self.counter == 0:
            # Activate UC detection
            def get_distc(a):
                self.dist_cutoff = float(a.text())

            self.distc_submenu = self.ucMenu.addMenu('dist tol')
            c = 0
            start, end, width = self.data["distc_min"], self.data["distc_max"], self.data["distc_count"]  # Change the limit if necessary
            num = (end - start)/width
            per_submenu = 30
            num_submenu = int(num/per_submenu) + 1
            g = 100
            c_end = 0
            self.distc_subsubmenu = self.distc_submenu.addMenu('Ideal crystal')
            self.distc_subsubmenu.addAction(str(0.00001))
            self.distc_subsubmenu.triggered[header.QAction].connect(get_distc)
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                distc_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.distc_subsubmenu = self.distc_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(distc_arr[-1],2)))
                for r in distc_arr:
                    self.distc_subsubmenu.addAction(str(r))
                self.distc_subsubmenu.triggered[header.QAction].connect(get_distc)

            def get_anglec(a):
                self.angle_cutoff = float(a.text())

            self.anglec_submenu = self.ucMenu.addMenu('angle tol')
            c = 0
            start, end, width = self.data["anglec_min"], self.data["anglec_max"], self.data["anglec_count"]  # Change the limit if necessary
            num = (end - start)/width
            per_submenu = 10
            num_submenu = int(num/per_submenu) + 1
            g = 100
            c_end = 0
            self.anglec_subsubmenu = self.anglec_submenu.addMenu('Ideal crystal')
            self.anglec_subsubmenu.addAction(str(0.00001))
            self.anglec_subsubmenu.triggered[header.QAction].connect(get_anglec)
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                anglec_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.anglec_subsubmenu = self.anglec_submenu.addMenu(str(round(anglec_arr[0],2)) + " - " + str(round(anglec_arr[-1],2)))
                for r in anglec_arr:
                    self.anglec_subsubmenu.addAction(str(r))
                self.anglec_subsubmenu.triggered[header.QAction].connect(get_anglec)

            def get_vfactor(a):
                self.vf = float(a.text())

            self.vfactor_submenu = self.ucMenu.addMenu('v_factor')
            c = 0
            start, end, width = self.data["vfactor_min"], self.data["vfactor_max"], self.data["vfactor_count"]  # Change the limit if necessary
            num = (end - start)/width
            per_submenu = 10
            num_submenu = int(num/per_submenu) + 1
            g = 100
            c_end = 0
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                vfactor_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.vfactor_subsubmenu = self.vfactor_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(vfactor_arr[-1],2)))
                for r in vfactor_arr:
                    self.vfactor_subsubmenu.addAction(str(r))
                self.vfactor_subsubmenu.triggered[header.QAction].connect(get_vfactor)

            self.go_action = header.QAction("&Go", self)
            self.go_action.triggered.connect(lambda:get_uc_func(self))
            self.ucMenu.addAction(self.go_action)
            #**************************************************
            self.counter = self.counter + 1

        else:
            print("WARNING : No crystal class has been detected !")
            print("**************************************************************************************************************")
            print("* DISCLAIMER : In case the detected crystal class is TRICLINIC, please try once by changing the tolerances ! *")
            print("**************************************************************************************************************")
            if self.enable_tol_func == False:
                tol_func(self)
    else:
        raise Exception("Kmeans is not calculated")