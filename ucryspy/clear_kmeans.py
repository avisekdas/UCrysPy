import header

def clear_kmeans_func(self):
    # Remove the previous kmeans
    self.grid.removeWidget(self.canvas_kmeans)
    self.ax_kmeans.remove()
    self.canvas_kmeans.deleteLater()

    self.kmeans_satisfied = 0 # Allow KMeans to calculate
    # Deactivate environment separation menu as it is already activated
    if self.comp == "t":
        self.envdecMenu.clear()

    # Object for k-means clustering
    self.figure_kmeans = header.Figure(figsize=(self.w, self.h))
    self.canvas_kmeans = header.FigureCanvasQTAgg(self.figure_kmeans)
    self.canvas_kmeans.draw()

    self.grid.addWidget(self.canvas_kmeans, 1, 0)