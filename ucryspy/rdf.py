# Calculate Radial distribution function (RDF) using freud

import header
from bod import bod_func
from save_bod import save_bod_func
from clear_bod import clear_bod_func

# Function for RDF
def rdf_func(self):
    if self.rdf_satisfied == 0:
        self.RDF = header.freud.density.RDF(self.bins, self.rmax)  # RDF
        self.aq = header.freud.AABBQuery(self.box_arr, self.positions)
        self.RDF.compute(system=self.aq, reset=False)

        if self.canvas_rdf:
            self.grid.removeWidget(self.canvas_rdf)
            self.canvas_rdf.deleteLater()
            self.figure_rdf = header.Figure(figsize=(self.w, self.h))
            
        self.canvas_rdf = header.FigureCanvasQTAgg(self.figure_rdf)
        self.ax_rdf = self.figure_rdf.add_subplot(111)
        self.ax_rdf.plot(self.RDF.bin_centers, self.RDF.rdf)
        self.ax_rdf.set_xlabel("r")
        self.ax_rdf.set_ylabel("g(r)")
        self.ax_rdf.set_title("RDF", fontsize=6)
        self.figure_rdf.tight_layout()
        self.canvas_rdf.draw()

        self.grid.addWidget(self.canvas_rdf, 3, 0)
        self.rdf_satisfied = 1

        # Zoom and pan
        ph = header.panhandler(self.figure_rdf, button=3)  # pan with right mouse button
        header.zoom_factory(self.ax_rdf)

        #******************************************************************************
        # Deactivate file upload
        self.fileMenu.clear()

        # Deactivate rolling frames
        self.rollingMenu.clear()

        # Activate BOD
        if self.rdf_state == 0:
            def get_rmin(a):
                self.rmin = float(a.text())

            self.rmin_submenu = self.bodMenu.addMenu('rmin')
            # some  actions
            c = 0
            start, end, width = self.data["rmin_min"], self.data["rmin_max"], self.data["rmin_count"]   # Change the limit if necessary
            num = (end - start)/width
            per_submenu = 30
            num_submenu = int(num/per_submenu) + 1
            g = 100
            c_end = 0
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                rmin_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.rmin_subsubmenu = self.rmin_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(rmin_arr[-1],2)))
                for r in rmin_arr:
                    self.rmin_subsubmenu.addAction(str(r))
                self.rmin_subsubmenu.triggered[header.QAction].connect(get_rmin)

            def get_rcut(a):
                self.rcut = float(a.text())

            self.rcut_submenu = self.bodMenu.addMenu('rcut')
            # some  actions
            c = 0
            start, end, width = self.data["rcut_min"], self.data["rcut_max"], self.data["rcut_count"]  # Change the limit if necessary
            num = (end - start)/width
            per_submenu = 30
            num_submenu = int(num/per_submenu) + 1
            g = 100
            c_end = 0
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                rcut_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.rcut_subsubmenu = self.rcut_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(rcut_arr[-1],2)))
                for r in rcut_arr:
                    self.rcut_subsubmenu.addAction(str(r))
                self.rcut_subsubmenu.triggered[header.QAction].connect(get_rcut)

            def get_mind(a):
                self.min_r = float(a.text())

            self.go_action = header.QAction("&Go", self)
            self.go_action.triggered.connect(lambda:bod_func(self))
            self.bodMenu.addAction(self.go_action)

            self.save_action = header.QAction("&Save", self)
            self.save_action.triggered.connect(lambda:save_bod_func(self))
            self.bodMenu.addAction(self.save_action)

            self.clear_action = header.QAction("&Clear", self)
            self.clear_action.triggered.connect(lambda:clear_bod_func(self))
            self.bodMenu.addAction(self.clear_action)

            self.rdf_state = self.rdf_state + 1

            self.bod_state = 0

    else:
        raise Exception("WARNING : Please clear the current one moving forward")