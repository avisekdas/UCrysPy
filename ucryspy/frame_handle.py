import header

def frame_handle_func(self):
    # Frame handling
    if self.counter == 0:
        if self.index >= 0:
            self.frameMenu = self.mainMenu.addMenu('Frame ' + str(self.index) + "/" + str(self.frame_num-1))
        else:
            self.frameMenu = self.mainMenu.addMenu('Frame ' + str(self.frame_num-1) + "/" + str(self.frame_num-1))
    elif self.counter > 0:
        if self.index >= 0:
            self.frameMenu.deleteLater()
            self.frameMenu = self.mainMenu.addMenu('Frame ' + str(self.index) + "/" + str(self.frame_num-1))
        else:
            self.frameMenu.deleteLater()
            self.frameMenu = self.mainMenu.addMenu('Frame ' + str(self.frame_num+self.index) + "/" + str(self.frame_num-1))