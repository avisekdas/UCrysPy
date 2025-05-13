import header

def clear_rdf_func(self):
    # Remove the previous rdf
    self.grid.removeWidget(self.canvas_rdf)
    self.ax_rdf.remove()
    self.canvas_rdf.deleteLater()

    # Deactivate BOD menu as it is already activated
    self.bodMenu.clear()

    self.rdf_state = 0
    self.rdf_satisfied = 0 # Allow to calculate RDF

    # Object for initializing RDF
    self.figure_rdf = header.Figure(figsize=(self.w, self.h))
    self.canvas_rdf = header.FigureCanvasQTAgg(self.figure_rdf)
    self.canvas_rdf.draw()
    self.grid.addWidget(self.canvas_rdf, 3, 0)