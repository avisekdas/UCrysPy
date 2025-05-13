import header

def clear_bod_func(self):
    # Remove the previous bod
    self.grid.removeWidget(self.canvas_bod)
    self.ax_bod.remove()
    self.canvas_bod.deleteLater()

    # Deactivate KMeans menu as it is already activated
    self.kmeansMenu.clear()
    self.bod_state = 0

    self.bod_satisfied = 0 # Allow BOD to calculate

    # Object for bond order diagram (BOD)
    self.figure_bod = header.Figure(figsize=(self.w, self.h))
    self.canvas_bod = header.FigureCanvasQTAgg(self.figure_bod)
    self.canvas_bod.draw()
    self.grid.addWidget(self.canvas_bod, 2, 0)