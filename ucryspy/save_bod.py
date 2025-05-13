# Save the BOD figure
# If any changes regarding the format, quality or sizes etc., please change it from here.
# The changing features directly from the window is not implemented

import header

def save_bod_func(self):
    options = header.QFileDialog.Options()
    options |= header.QFileDialog.DontUseNativeDialog
    fileName, _ = header.QFileDialog.getSaveFileName(self, 
        "Save File", "", "Image Files(*.png);;All Files(*)", options = options)

    fig = header.plt.figure(figsize = (8, 8))
    ax = header.plt.axes(projection ="3d")
    # Creating plot
    ax.scatter3D(self.x, self.y, self.z, s=5)
    view_angle = 0, 0
    ax.view_init(*view_angle)
    # ax.set_axis_off()
    fig.savefig(fileName, dpi=300)
    header.plt.close()