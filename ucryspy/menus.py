import header
from ucpy_homepage import upload_traj_func, load_traj_func
from save_config import save_config_func
from plot_conf import plot_conf_func
from right_callback import right_callback_func
from left_callback import left_callback_func
from up_callback import up_callback_func
from down_callback import down_callback_func
from screenshot import save_screenshot_func
from plot_config import plot_config_func

def menus_func(self):
    # Define basic parameters and initialization
    self.bins = 0
    self.rmax = 0
    self.coord = 0
    self.r_min = 0.0
    self.r_cut = 0.0
    self.n_bins = 0
    self.r_max = 0.0
    self.coord_num = 0
    self.r = 15.0   # Initialize the raius of the sphere
    self.frame_num = 0
    self.figure_rdf = None
    self.figure_bod = None
    self.added_box = None
    self.fileName_json = None
    self.rdf_satisfied = 0
    self.bod_satisfied = 0
    self.kmeans_satisfied = 0
    self.verts = []
    self.c = 'slateblue'   # Initial color 
    self.index = -1   # which frame to read initially; by default the last frame
    self.env_count = 0
    self.comp = "t"
    self.file_upload_state = 0
    self.env_sep_iteration = 0
    self.bravais_count = 0
    # Save fig spheres
    self.sphereRadius = 0.5
    self.figsize = 70
    self.samples = 32
    alpha, beta, gamma = 0, header.np.deg2rad(10), header.np.deg2rad(10)
    self.quat = header.rowan.normalize(header.rowan.from_euler(alpha, beta, gamma, convention='zyx'))
    self.click_count = 0
    self.enable_tol_func = False
    self.id = 0
    self.LattVec = []  # initialization of lattice vectors
    self.avg_input = "s"
    self.color_original = ["#e3677c", "#58b871", "#0693a1", "#7e44ac", "#a74b7a", "#5a5930", '#4ba79c', '#5b53bf', '#53bf86', '#bfb053', '#e43763', '#9af5cf', '#db2585', '#9157ea', '#ce3852', '#4c4cf7', '#41fafd', '#eb5e49', '#8e9e36', '#b2d409', '#1650ef', '#3ba8dc', '#166252', '#41f58e', '#23b021', '#665544', '#e8d678', '#35f596', '#251fb6', '#cf59e7', '#4e3f22', '#211b92', '#09dd04', '#82c2a1', '#30b7c0', '#9231f3', '#0cbcfd', '#69acc8', '#f2be83', '#bf66e3', '#a01145', '#5b1907', '#1ef826', '#b25370', '#e6b031', '#c56dbb', '#a9501b', '#05b83e', '#14e4ad', '#ea4295', '#180f04', '#fd1f31', '#e2b3d4', '#0ff069', '#0ec261', '#021457', '#ebb385', '#111455', '#0d59ed', '#700590', '#6fdd6b', '#37eab9', '#ea51d5', '#95a91a', '#2851be', '#dfbab3', '#e7e7ee', '#af20c0', '#037c11', '#b8b7dd', '#171828', '#f55b18', '#833507', '#910495', '#a8cc90', '#18622e', '#f63fa7', '#4db81e', '#eb8c86', '#32dd5b', '#2756bb', '#d93105', '#1e669d', '#b92399', '#4defdf', '#2b564e', '#90be11', '#41c465', '#b07730', '#fc6cdd', '#1a8992', '#c0dc0b', '#f1172d', '#857f1c', '#8270f0', '#8e5765', '#f34d59', '#0606d3', '#ad1f4d', '#f7e7a6', '#e03639', '#d8eccc', '#6f04df', '#ec7401', '#44025b', '#08add8', '#b20a03', '#139c62', '#edf1ad', '#c11104', '#159771', '#5d62a1', '#cf91a4', '#a82ee4', '#4b8198', '#03ae8b', '#77919d', '#e2d838', '#1ff733', '#18ed69', '#68dde4', '#d33bff', '#831c1e', '#bdf3cd', '#6b6724', '#e696ac', '#489a81', '#d75fd0', '#2d13d4', '#a4f57f', '#c0c6af', '#c61351', '#f8a098', '#66bcfa', '#2f034c', '#66578d', '#f878ba', '#f26bcd', '#31117e', '#4136e7', '#1e58ab', '#d6a61f', '#d8dc03', '#2026f1', '#3531e7', '#a0f5de', '#255c61', '#83c865', '#08a669', '#29fc13', '#4ca1cb', '#9e0033', '#e6d4f3', '#9261c4', '#24b4a1', '#7fbb6c', '#906113', '#b802d1', '#b16e05', '#1e5837', '#fd4953', '#6c5854', '#4ea1cc', '#1ff49f', '#023437', '#eb9f91', '#6fe05c', '#ebac05', '#1a816a', '#fb3d2d', '#ba61c7', '#497f07', '#215d8f', '#c43cde', '#9a8bdb', '#e74c11', '#56dd2a', '#3b9169', '#5858d2', '#0141c5', '#bca5e4', '#28c786', '#9f52b8', '#c921ab', '#9c4906', '#6833f7', '#e2152c', '#99fb5f', '#0e26b7', '#1dc387', '#fc8323', '#272ec5', '#ec13e6', '#0268cf', '#602c40', '#1097c9', '#4a0e55', '#d88248', '#a8f859', '#f6055e', '#b65aa3', '#670625', '#52f594', '#d81c56', '#08763c', '#bb4270', '#234717', '#60687c', '#d61e6a', '#23c361', '#8a645b', '#a98abd', '#b3c8b8', '#16b1ce', '#8af216', '#7153e4', '#119a7a', '#797810', '#2181e3', '#98e00f', '#11c13d', '#38c5dd', '#a99ee0', '#47b009', '#9a4133', '#fe5f9c', '#3b0194', '#2d0d87', '#1b66f1', '#48803d', '#f2fb5b', '#75c636', '#41fd63', '#8d52f3', '#0adc62', '#81801b', '#ce8f31', '#673fd1', '#9b086b', '#419930', '#3d2ed3', '#6f2a69', '#4f4278', '#455a5b', '#942d7d', '#f29094', '#9393f6', '#0e4fa2', '#dd4851', '#73cf08', '#a07d5c', '#414a18', '#012bf3', '#17fb40', '#da4338', '#ccd5a1', '#3ca76a', '#4c158b', '#ebc968', '#7625e9', '#74f8f2', '#8daddc', '#464607', '#cd4623', '#fae4e6', '#780fcd', '#51a8bf', '#db0c6d', '#e89f74', '#7dfaf6', '#363d28', '#51fd41', '#0501d9', '#3d7281', '#271981', '#e87cd1', '#fcee20', '#709acc', '#71f629', '#c54906', '#d1b22a', '#885d38', '#4ed393', '#08fd09', '#4a45b5', '#ea4fd3', '#5bd370', '#f668c2', '#aabff3', '#caae57', '#4251d3', '#da873c', '#1010a9', '#81bbf3', '#cbf26f', '#5eef83', '#c46346', '#289536', '#fd3c60', '#4d3299']
    self.color_arr = [header.pv.Color('0x3cafa0'), header.pv.Color('0xe97138'), header.pv.Color('0x138fc2'), header.pv.Color('0x11ab14'), header.pv.Color('0xff5733'), header.pv.Color('0xab9d11'), header.pv.Color('0x3ba099'), header.pv.Color('0x6c3ba0'), header.pv.Color('0xa03b80')]

    # create the frame
    self.frame = header.QtWidgets.QFrame()
    self.hlayout = header.QtWidgets.QHBoxLayout()
    self.grid = header.QGridLayout()

    self.counter = 0
    # add the pyvista interactor object
    self.plotter = header.QtInteractor(self.frame)
    # self.plotter.enable_ssao()
    self.plotter.set_background("white")
    # header.pv.set_plot_theme('dark')
    header.pv.global_theme.axes.show = True
    self.hlayout.addWidget(self.plotter.interactor, 80)
    self.signal_close.connect(self.plotter.close)

    # Upload the self.data file for trajectory
    traj_action = header.QAction("&Load file", self)
    traj_action.triggered.connect(lambda:upload_traj_func(self))

    # simple menus
    self.mainMenu = self.menuBar()
    self.mainMenu.setNativeMenuBar(False)
    self.fileMenu = self.mainMenu.addMenu('File')
    self.fileMenu.addAction(traj_action)

    # Quick screenshot
    self.sshot_action = header.QtWidgets.QAction('Quick screenshot', self)
    self.sshot_action.triggered.connect(lambda:save_screenshot_func(self))
    self.fileMenu.addAction(self.sshot_action)

    self.save_menu = self.fileMenu.addMenu('Save configure')
    self.save_sphere_params = self.save_menu.addMenu('Sphere')

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

    self.save_action = header.QAction("&Save", self)
    self.save_action.triggered.connect(lambda:save_config_func(self))
    self.fileMenu.addAction(self.save_action)

    header.cwd = header.os.path.dirname(header.os.path.abspath(__file__)) # Current directory
    header.p = header.cwd + '/'
    input_param_json = "param_file.json"
    with open(input_param_json) as f:
        self.data = header.json.load(f)

    #*****************************************************
    
    # Rolling frames
    forward_action = header.QAction("&Forward", self)
    forward_action.triggered.connect(lambda:right_callback_func(self))

    backword_action = header.QAction("&Backword", self)
    backword_action.triggered.connect(lambda:left_callback_func(self))

    up_action = header.QAction("&Last frame", self)
    up_action.triggered.connect(lambda:up_callback_func(self))

    down_action = header.QAction("&First frame", self)
    down_action.triggered.connect(lambda:down_callback_func(self))

    self.rollingMenu = self.mainMenu.addMenu('Rolling frames')
    self.rollingMenu.addAction(forward_action)
    self.rollingMenu.addAction(backword_action)
    self.rollingMenu.addAction(up_action)
    self.rollingMenu.addAction(down_action)

    #****************************************************************
    # Identity separation
    self.typeMenu = self.mainMenu.addMenu('Identity separation')
    self.typeMenu.setLayoutDirection(header.Qt.LeftToRight)

    #****************************************************************
    # RDF
    self.rdfMenu = self.mainMenu.addMenu('RDF')
    self.rdfMenu.setLayoutDirection(header.Qt.LeftToRight)

    #**********************************************************
    # BOD
    self.bodMenu = self.mainMenu.addMenu('BOD')
    self.bodMenu.setLayoutDirection(header.Qt.LeftToRight)

    #*******************************************************
    # Kmeans clustering
    self.kmeansMenu = self.mainMenu.addMenu('KMeans')
    self.kmeansMenu.setLayoutDirection(header.Qt.LeftToRight)

    #*******************************************************
    # Environment detection menu
    self.envdecMenu = self.mainMenu.addMenu('Environment detection')
    self.envdecMenu.setLayoutDirection(header.Qt.LeftToRight)

    #*******************************************************
    # Environment separation menu
    self.envsepMenu = self.mainMenu.addMenu('Environment separation')
    self.envsepMenu.setLayoutDirection(header.Qt.LeftToRight)

     #*******************************************************
    # Global symmetry
    self.classMenu = self.mainMenu.addMenu('Crystal class')
    self.classMenu.setLayoutDirection(header.Qt.LeftToRight)
    
    #*******************************************************
    # Unit cell
    self.ucMenu = self.mainMenu.addMenu('Unit cell')
    self.ucMenu.setLayoutDirection(header.Qt.LeftToRight)
    #****************************************************************

    self.frame.setLayout(self.hlayout)
    self.setCentralWidget(self.frame)

    #**********************************************************
    # Just for GUI purpose
    # Initializing the object for different analyses

    cwd = header.os.path.dirname(header.os.path.abspath(__file__)) # Current directory
    p = cwd + '/'
    self.image = p+'images/'+'menu_logo_transparent.png'   # Image of the package

    self.w, self.h = 2.5, 2

    # Object for initializing RDF
    self.figure_rdf = header.Figure(figsize=(self.w, self.h))
    self.canvas_rdf = header.FigureCanvasQTAgg(self.figure_rdf)
    self.canvas_rdf.draw()

    # Object for bond order diagram (BOD)
    self.figure_bod = header.Figure(figsize=(self.w, self.h))
    self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)
    self.canvas_bod.draw()

    # Object for k-means clustering
    self.figure_kmeans = header.Figure(figsize=(self.w, self.h))
    self.canvas_kmeans = header.FigureCanvasQTAgg(self.figure_kmeans)
    self.canvas_kmeans.draw()

    # Object for 1D RDF, not implemented
    '''self.figure_onedrdf = header.Figure()
    self.canvas_onedrdf = header.FigureCanvasQTAgg(self.figure_onedrdf)
    self.canvas_onedrdf.draw()'''

    # Define the position of 'UCPy' logo for the image axes
    '''self.figure_onedrdf = header.Figure(figsize=(self.w, self.h))
    self.ax_image = self.figure_onedrdf.add_subplot(111)
    
    image = header.Image.open(self.image) # Open the image
    image_array = header.np.array(image)

    # Display the image
    self.ax_image.imshow(image_array)
    self.ax_image.axis('off')  # Remove axis of the image
    
    self.canvas_onedrdf = header.FigureCanvasQTAgg(self.figure_onedrdf)
    self.canvas_onedrdf.draw()'''

    # self.avg_input, done1 = header.QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Average over frames? (y/n)') 

    # Add the widgets
    # self.grid.addLayout(self.canvas_onedrdf, 0, 0)
    self.grid.addWidget(self.canvas_kmeans, 1, 0)
    self.grid.addWidget(self.canvas_bod, 2, 0)
    self.grid.addWidget(self.canvas_rdf, 3, 0)
    self.hlayout.addLayout(self.grid, 20)