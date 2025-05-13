import header

def diffraction_func(self):
    self.dp = header.freud.diffraction.DiffractionPattern(grid_size=self.gridsize, output_size=self.outputsize)
    self.dp.compute((self.box_arr, self.positions), view_orientation=[1, 0, 0, 0])
    # Plot diff
    self.figure_diff = header.Figure(figsize=(2.5, 2))
    self.ax_diff = self.figure_diff.add_subplot(111)
    self.canvas_diff = header.FigureCanvasQTAgg(self.figure_diff)
    self.dp.plot(self.ax_diff)
    self.ax_diff.set_axis_off()
    self.figure_diff.delaxes(self.figure_diff.axes[1])
    self.ax_diff.set_title("Diffraction pattern", fontsize=6)
    self.grid.addWidget(self.canvas_diff, 1, 0)

    # Zoom and pan
    ph = header.panhandler(self.figure_diff, button=3)  # pan with right mouse button
    header.zoom_factory(self.ax_diff)