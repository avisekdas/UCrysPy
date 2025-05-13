# This script considers the centroid of the cluster in BOD
# Calcuates the face mid-points and edge mid-points

import header
from calc_equiv_points_poly import calc_equiv_points_poly_func
from symm import symm_func
from get_posi_orien_local_frame import get_posi_orien_local_frame_func
from make_xyz import make_xyz_func
from lattice_param import lattice_param_func
from get_uc import get_uc_func

from scipy.spatial import ConvexHull, Delaunay
from collections import Counter, defaultdict, deque, namedtuple
from itertools import chain

def tol_func(self):
    def get_rtol(a):
        self.rtol = float(a.text())

    self.rtol_submenu = self.gsMenu.addMenu('r_tol')
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

    self.atol_submenu = self.gsMenu.addMenu('a_tol')
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
        print("WARNING : Please recalculate \"Global symmetry\" with extarnal tolerance values")
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
            #***************************************************

            def get_decision(a):
                self.user_dec = str(a.text())

            answer_action = self.ucMenu.addMenu("Stop")
            dec_arr = ['y', 'n']
            for dec in dec_arr:
                    answer_action.addAction(str(dec))
            answer_action.triggered[header.QAction].connect(get_decision)
            #***************************************************

            def continue_decision(a):
                self.user_input_dec = str(a.text())

            continue_action = self.ucMenu.addMenu("Continue")
            dec_arr = ['y', 'n']
            for dec in dec_arr:
                    continue_action.addAction(str(dec))

            continue_action.triggered[header.QAction].connect(continue_decision)
            #***************************************************

            def choice_decision(a):
                self.user_input = int(a.text())

            self.choice_submenu = self.ucMenu.addMenu("Choice of uc")
            start, end, width = self.data["choice_min"], self.data["choice_max"], self.data["choice_count"]
            num = (end - start)/width
            per_submenu = 20
            num_submenu = int(num/per_submenu) + 1
            g = 100
            c_end = 0
            for c in range(num_submenu):
                if c == 0:
                    c_start = start
                else:
                    c_start = c_end
                c_end = round(c_start  + width*per_submenu, 2)
                choice_arr = [i/g for i in range(int(c_start*g), int(c_end*g), int(width*g))]
                self.choice_subsubmenu = self.choice_submenu.addMenu(str(round(c_start,2)) + " - " + str(round(choice_arr[-1],2)))
                for r in distc_arr:
                    self.choice_subsubmenu.addAction(str(r))
                self.choice_subsubmenu.triggered[header.QAction].connect(choice_decision)

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
