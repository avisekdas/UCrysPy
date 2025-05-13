import header
from pyvista_interface import pyvista_interface_func
from pyvista_sphere import pyvista_sphere_func

def clear_plot_func(self):
    self.ty = 'None'

    # Removing the previous calculated analyses, RDF, BOD and K-means
    # Remove the previous kmeans
    self.grid.removeWidget(self.canvas_kmeans)
    self.canvas_kmeans.deleteLater()

    # Remove the previous bod
    self.grid.removeWidget(self.canvas_bod)
    self.canvas_bod.deleteLater()
    
    # Remove the previous rdf
    self.grid.removeWidget(self.canvas_rdf)
    self.canvas_rdf.deleteLater()
    
    # Remove snashot
    for p in self.real_added_mesh_arr:
        self.plotter.remove_actor(p)
    self.plotter.remove_actor(self.imag_added_mesh)

    self.plotter.remove_actor(self.added_box)

    # Plot the system
    if self.fileName_json:
        with open(self.fileName_json) as f:
            data = header.json.load(f)   # data per files

        self.verts = data["8_vertices"]   # vertices
        pyvista_interface_func(self)

    else:
        pyvista_sphere_func(self)
