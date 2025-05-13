import header
from plot_conf import plot_conf_func
from frame_handle import frame_handle_func
from gsd_reader import gsd_reader_func

def left_callback_func(self):
    self.frameMenu.deleteLater()
    if len(self.fileName_traj) >= 1:
        self.index = self.index - 1
        split_tup = header.os.path.splitext(self.fileName_traj)
        file_extension = split_tup[1]
        if file_extension == ".gsd":
            gsd_reader_func(self)
    
        plot_conf_func(self)
        frame_handle_func(self)
        # It records the total number of back and forth of the plot, i.e. how many times this thing is being plotted
        self.counter = self.counter + 1
    
    