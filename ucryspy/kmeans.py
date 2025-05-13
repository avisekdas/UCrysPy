# K-means clusteering is implemented using SciPy and Scikit-learn
# Activated once BOD calculation is done

import header
from env_detection import env_detection_func
from clear_envsep import clear_envsep_func

def kmeans_func(self):
    if self.bod_satisfied == 1 and self.kmeans_satisfied == 0:
        self.cluster_range = range(self.cmin, self.cmax)
        self.cluster_errors = []
        for num_clusters in self.cluster_range:
            clusters = header.KMeans(n_clusters=num_clusters,init='k-means++', n_init='auto', random_state=0)
            pred=clusters.fit_predict(self.position_arr)
            self.cluster_errors.append(clusters.inertia_)
            # print(num_clusters)

        #*************************************************************
        if self.canvas_kmeans:
            self.grid.removeWidget(self.canvas_kmeans)
            self.canvas_kmeans.deleteLater()
            self.figure_kmeans = header.Figure(figsize=(self.w, self.h))

        '''hist, edges = header.np.histogramdd(header.np.array(self.position_arr), bins=100)
        flat_hist = hist.ravel()
        peaks, _ = header.find_peaks(flat_hist, prominence=10)
        print(peaks)
        print(self.position_arr[peaks])'''

        # Canvas for displaying kmeans plot
        self.canvas_kmeans = header.FigureCanvasQTAgg(self.figure_kmeans)
        self.ax_kmeans = self.figure_kmeans.add_subplot(111)

        self.ax_kmeans.plot(self.cluster_range, header.np.sqrt(self.cluster_errors),'b')
        self.ax_kmeans.set_xlabel(r"$N_c$")
        self.ax_kmeans.set_ylabel("WCSS")
        self.ax_kmeans.set_title("kmeans clustering", fontsize=6)
        self.figure_kmeans.tight_layout()
        self.canvas_kmeans.draw()
        self.grid.addWidget(self.canvas_kmeans, 1, 0)
        #**********************************************************

        self.kmeans_satisfied = 1   # Kmeans is done

        # Zoom and pan
        ph = header.panhandler(self.figure_kmeans, button=3)  # pan with right mouse button
        header.zoom_factory(self.ax_kmeans)

        #******************************************************************************
        # Activate Environemnet separation menu
        if self.comp == "t" and self.kemans_state == 0:
            def get_elbow(a):
                self.elbow = int(a.text())

            self.elbow_submenu = self.envdecMenu.addMenu('elbow')

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

            def get_match(a):
                self.match = float(a.text())

            self.match_submenu = self.envdecMenu.addMenu('Matching')
            c = 0 
            start, end, width = 0.1, 1.05, 0.05
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
                if c_end > end:
                    c_end = end
                match_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.match_subsubmenu = self.match_submenu.addMenu(str(round(c_start, 2)) + " - " + str(round(match_arr[-1], 2)))
                for r in match_arr:
                    self.match_subsubmenu.addAction(str(r))
                self.match_subsubmenu.triggered[header.QAction].connect(get_match)
            

            self.go_action = header.QAction("&Go", self)
            self.go_action.triggered.connect(lambda:env_detection_func(self))
            self.envdecMenu.addAction(self.go_action)

            self.clear_action = header.QAction("&Clear", self)
            self.clear_action.triggered.connect(lambda:clear_envsep_func(self))
            self.envdecMenu.addAction(self.clear_action)

    else:
        raise Exception("WARNING : BOD is not calculated or please clear the current one moving forward")
