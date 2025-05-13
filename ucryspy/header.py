# UCRYSPY ---> A pythod based project to visualize unit cell of crystal with hard polyhedra including particles' orientations
# Written by Sumitava Kundu
# References : #

# Please see the manual for detail instructions
#******************************************************************************************
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib.text import Annotation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os
import time, sys
import concurrent.futures
from matplotlib.figure import Figure
import types

from garnett.reader import PosFileReader
from garnett.writer import PosFileWriter
from garnett.reader import GSDHOOMDFileReader
import numpy as np, types
from numpy import eye, asarray, dot, sum, diag
from numpy.linalg import svd
import freud, coxeter
import json, math, sys
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import gsd
import math,os,sys,re,shutil,glob
import argparse,json,subprocess,shlex
import random
import rowan
import os.path
import scipy.stats
from itertools import chain
import scipy
from scipy.spatial import ConvexHull, distance, Delaunay
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from collections import Counter
from itertools import combinations
import time
from pathlib import Path
import copy
from mpl_interactions import ioff, panhandler, zoom_factory
from sklearn.cluster import MeanShift, estimate_bandwidth
# from distinctipy import distinctipy
import multiprocess

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qtpy import QtWidgets
import pyvistaqt
from pyvistaqt import QtInteractor, MainWindow, BackgroundPlotter
import pyvista as pv
# os.environ["QT_API"] = "pyqt5"
os.environ["QT_API"] = "pyside2"
from Geometry3D import *
import itertools
import spglib
# import plato
# import plato.draw.fresnel as draw1
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from sklearn.mixture import GaussianMixture
from PIL import Image
from scipy import stats as st
from scipy.signal import find_peaks
import matplotlib.colors as mcolors

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)