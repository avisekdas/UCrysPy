import header
from plot_config import plot_config_func

def gsd_reader_func(self):
    self.traj = header.gsd.hoomd.open(name=self.fileName_traj, mode='r')
    self.frame_num = len(self.traj)
    self.snap = self.traj[self.index]
    self.type_shapes = self.snap.particles.type_shapes
    self.type_shapes = [self.type_shapes[0]]
    self.unique_type_shapes = self.type_shapes[:]
    self.typeid = self.snap.particles.typeid
    self.original_typeid = self.typeid[:]
    self.type_shapes_keys = [list(self.type_shapes[self.original_typeid[t]].values()) for t in range(len(self.snap.particles.position))]
    self.verts, self.orientations = [], []
    for t in range(len(self.type_shapes_keys)):
        if "ConvexPolyhedron" in self.type_shapes_keys[t]:
            self.verts.append(self.type_shapes[self.original_typeid[t]]["vertices"])
            self.orientations.append(self.snap.particles.orientation[t])
        elif "Sphere" in self.type_shapes_keys[t]:
            self.verts.append(self.type_shapes[self.original_typeid[t]]["radius"])
            self.orientations.append([1, 0, 0, 0])
        else:
            self.orientations.append([1, 0, 0, 0])

    if len(self.verts) != 0:
        self.original_verts = self.verts[:]
    
    self.original_orientations = self.orientations[:]
    self.box_info = self.snap.configuration.box
    self.box = self.box_info
    self.box_arr = header.freud.box.Box(Lx=self.box[0], Ly=self.box[1], Lz=self.box[2],
                            xy=self.box[3], xz=self.box[4], yz=self.box[5], is2D=False)
    
    self.positions = self.snap.particles.position
    self.original_positions = self.positions[:]
    self.diameter = self.snap.particles.diameter
    self.radii = self.diameter/2.0
    self.original_radii = self.radii[:]
    self.typeid_arr = self.snap.particles.types   # Types
    self.typeid_arr_int = self.snap.particles.typeid  # Typeid
    self.raw_typeid_arr_int = self.typeid_arr_int[:]
    self.typeid_arr_int = list(set(self.raw_typeid_arr_int))
    self.particle_typeid = list(set(self.typeid_arr))
    self.original_particleids = [i for i in range(len(self.original_positions))]
    self.particleids = self.original_particleids[:]

    '''if len(self.verts) != 0:
        self.orientations = self.snap.particles.orientation
        self.original_orientations = self.orientations[:]
    else:
        self.orientations = header.np.array([[1, 0, 0, 0] for _ in range(len(self.original_positions))])
        self.original_orientations = self.orientations[:]'''
        # raise Exception("JSON file with proper format not found") 

    #**************************************************