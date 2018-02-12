import sys
import numpy as np
import unittest
import webbrowser

from unittest.mock import MagicMock

from PyQt5 import QtGui, QtWidgets

# set up import paths
import path_prepare

from sas.sascalc.fit.AbstractFitEngine import FitEngine
from sas.sascalc.fit.AbstractFitEngine import FResult
#from sasmodels.sasview_model import core_shell_ellipsoid
from sasmodels.sasview_model import load_standard_models
from sas.qtgui.Plotting.PlotterData import Data1D

import sas.qtgui.Utilities.GuiUtils as GuiUtils
# Local
from sas.qtgui.Utilities.GridPanel import BatchOutputPanel

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

class BatchOutputPanelTest(unittest.TestCase):
    '''Test the batch output dialog'''
    def setUp(self):
        '''Create the dialog'''
        # dummy perspective
        class dummy_manager(object):
            def communicator(self):
                return GuiUtils.Communicate()
            def communicate(self):
                return GuiUtils.Communicate()
        # dummy parameter set
        m = None
        for m in load_standard_models():
            if m.name == "core_shell_ellipsoid":
                model = m()
        #model = core_shell_ellipsoid()
        self.assertIsNotNone(m)
        data = Data1D(x=[1,2], y=[3,4], dx=[0.1, 0.1], dy=[0.,0.])
        param_list = ['sld_shell', 'sld_solvent']
        output = FResult(model=model, data=data, param_list=param_list)
        output.theory = np.array([0.1,0.2])
        output.residuals = np.array([0.01, 0.02])
        output.fitter_id = 200
        output_data = [[output],[output]]
        self.widget = BatchOutputPanel(parent=dummy_manager(), output_data=output_data)

    def tearDown(self):
        '''Destroy the GUI'''
        self.widget.close()
        self.widget = None

    def testDefaults(self):
        '''Test the GUI in its default state'''
        self.assertIsInstance(self.widget, QtWidgets.QMainWindow)
        # Default title
        self.assertEqual(self.widget.windowTitle(), "Grid Panel")

        # modal window
        self.assertTrue(self.widget.isModal())

