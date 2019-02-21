import shutil
import numpy as np

# from https://stackoverflow.com/questions/37149933/how-to-set-max-output-width-in-numpy and
# https://gist.github.com/jtriley/1108174
def maximizeNumpyPrint(shrinkScale=1):
    maxcol = tuple(shutil.get_terminal_size())[0]
    np.set_printoptions(edgeitems=int(maxcol/(10*shrinkScale)),linewidth=maxcol)