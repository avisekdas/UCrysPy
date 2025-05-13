# Bais ucryspy window handling
#**********************************************************************

import header
from menus import menus_func

class Ui_MainWindow(header.MainWindow):
    def __init__(self, parent=None, show=True):
        header.QtWidgets.QMainWindow.__init__(self, parent)
        menus_func(self)
        if show:
            self.show()

if __name__ == "__main__":
    cwd = header.os.path.dirname(header.os.path.abspath(__file__)) # Current directory
    p = cwd + '/'
    image = p+'images/'+'ucpy_logo.png'   # Logo of the package

    app = header.QtWidgets.QApplication(header.sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.setWindowTitle("UCrysPy")   # Title of the window
    MainWindow.resize(1100, 750)   # Size of the start-up window
    MainWindow.show()
    MainWindow.setWindowIcon(header.QIcon(image))

    # header.sys.exit(app.exec_())
    app.exec_()



    
