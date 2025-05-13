import header

def save_screenshot_func(self):
    options = header.QFileDialog.Options()
    options |= header.QFileDialog.DontUseNativeDialog
    fileName, _ = header.QFileDialog.getSaveFileName(self, 
        "Save File", "", "Image Files(*.png);;All Files(*)", options = options)

    self.plotter.screenshot(fileName + '_screenshot.png')