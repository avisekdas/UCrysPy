import header

def save_fig_func(self):
    # selecting file path
    filePath, _ = header.QFileDialog.getSaveFileName(self, "Save Image", "",
                        "SVG(*.svg);;EPS(*.eps);;PS(*.ps);;PDF(*.pdf);;All Files(*.*) ")

    # if file path is blank return back
    if filePath == "":
        return
        
    # saving canvas at desired path
    self.plotter.save_graphic(filePath)