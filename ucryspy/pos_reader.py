import header
from plot_config import plot_config_func

def pos_reader_func(self):
    pos_reader = header.PosFileReader()
    pos_writer = header.PosFileWriter()
    with open(self.fileName_traj, 'r') as file:
        self.traj = pos_reader.read(file)
        self.traj.load_arrays()
    self.positions = self.traj[self.index].position
    self.original_positions = self.positions[:]
    # Types
    self.typeid_arr = self.traj[self.index].types
    self.raw_typeid_arr = self.typeid_arr[:]
    self.particle_typeid = list(set(self.typeid_arr))
    # Typeid
    self.typeid_arr_int = self.traj[self.index].typeid
    self.raw_typeid_arr_int = self.typeid_arr_int[:]
    self.typeid_arr_int = list(set(self.raw_typeid_arr_int))

    self.original_particleids = [i for i in range(len(self.original_positions))]
    self.particleids = self.original_particleids[:]

    if self.fileName_json != None:
        self.orientations = self.traj[self.index].orientation
        self.original_orientations = self.orientations[:]
    else:
        self.orientations = header.np.array([[1, 0, 0, 0] for _ in range(len(self.positions))])
        self.original_orientations = self.orientations[:]
        # raise Exception("JSON file with proper format not found") 
    self.frame_num = len(self.traj)
    self.box_info = self.traj[self.index].box
    self.box = self.box_info
    self.box_arr = header.freud.box.Box(Lx=self.box.Lx, Ly=self.box.Ly, Lz=self.box.Lz,
                            xy=self.box.xy, xz=self.box.xz, yz=self.box.yz, is2D=False)
    
    #**************************************************
    def get_typeval(a):
        self.typeval = int(a.text())
        # print(self.rmax)

    # Add type menu after loading pos file
    for t in range(len(self.typeid_arr_int)):
        self.id_submenu = self.typeMenu.addMenu('Type ' + str(self.typeid_arr_int[t]))
        self.id_submenu.addAction(str(self.typeid_arr_int[t]))
        self.id_submenu.triggered[header.QAction].connect(get_typeval)

    self.go_action = header.QAction("&Go", self)
    self.go_action.triggered.connect(lambda:plot_config_func(self, self.typeval))
    self.typeMenu.addAction(self.go_action)
    #**************************************************