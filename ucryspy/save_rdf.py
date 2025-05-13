# Save the RDF plot
# If any changes regarding the format, quality or sizes etc., please change it from here.
# The changing features directly from the window is not implemented

import header

def save_rdf_func(self):
    options = header.QFileDialog.Options()
    options |= header.QFileDialog.DontUseNativeDialog
    fileName, _ = header.QFileDialog.getSaveFileName(self, 
        "Save File", "", "Image Files(*.png);;All Files(*)", options = options)

    fig = header.plt.figure(figsize=(1.5, 1.5), dpi=600)
    header.plt.plot(self.RDF.bin_centers, self.RDF.rdf, linewidth=1)
    header.plt.xlabel("r", fontsize=8)
    header.plt.ylabel("g(r)", fontsize=8)
    header.plt.xticks(fontsize=6)
    header.plt.yticks(fontsize=6)
    header.plt.tick_params(axis='both', direction='in', length=3)
    header.plt.locator_params(axis='x', nbins=4)
    header.plt.locator_params(axis='y', nbins=4)
    header.plt.tight_layout()
    header.plt.savefig(fileName, dpi=300)
    header.plt.close()