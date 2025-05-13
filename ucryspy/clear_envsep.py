import header

def clear_envsep_func(self):
    # Deactivate Environment separation menu
    self.envsepMenu.clear()

    # If "s" is pressed in the previous step then activate RDF menu again, as it is already inactive.
    if self.comp == "s":
        # Removing the previous calculated analyses, RDF, BOD and K-means
        # Remove the previous kmeans
        self.grid.removeWidget(self.canvas_kmeans)
        self.canvas_kmeans.deleteLater()
        self.ax_kmeans.remove()

        # Remove the previous bod
        self.grid.removeWidget(self.canvas_bod)
        self.ax_bod.remove()
        self.canvas_bod.deleteLater()
        
        # Remove the previous rdf
        self.grid.removeWidget(self.canvas_rdf)
        self.ax_rdf.remove()
        self.canvas_rdf.deleteLater()
        
        # Remove snashot
        self.plotter.remove_actor(self.sim_added_box)
        self.plotter.remove_actor(self.added_mesh)

        # Deactivate gsMenu as it is already activated
        self.gsMenu.clear()

    if self.comp == "c":
        # Deactivate RDF menu
        self.rdfMenu.clear()

    if self.comp == "s" or self.comp == "c":
        from pyvista_interface import pyvista_interface_func
        from pyvista_sphere import pyvista_sphere_func

        self.positions = self.original_positions[:]
        self.orientations = self.original_orientations[:]

        # Plot the system
        if self.fileName_json:
            with open(self.fileName_json) as f:
                data = header.json.load(f)   # data per files

            self.verts = data["8_vertices"]   # vertices
            pyvista_interface_func(self)

        else:
            pyvista_sphere_func(self)