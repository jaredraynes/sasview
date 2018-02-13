# global
import sys
import os
import types
import webbrowser

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import sas.qtgui.Utilities.GuiUtils as GuiUtils

from sas.qtgui.Utilities.UI.TabbedModelEditor import Ui_TabbedModelEditor
from sas.qtgui.Utilities.PluginDefinition import PluginDefinition
from sas.qtgui.Utilities.ModelEditor import ModelEditor

class TabbedModelEditor(QtWidgets.QDialog, Ui_TabbedModelEditor):
    """
    Model editor "container" class describing interaction between
    plugin definition widget and model editor widget.
    Once the model is defined, it can be saved as a plugin.
    """
    # Signals for intertab communication plugin -> editor
    sasmodelChangedSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(TabbedModelEditor, self).__init__()

        self.parent = parent

        self.setupUi(self)

        # globals
        self.sasmodel = None

        self.addTabs()

        self.addSignals()

    def addTabs(self):
        """
        Populate tabs with widgets
        """
        # Add tabs
        # Plugin definition widget
        self.plugin_widget = PluginDefinition(self)
        self.tabWidget.addTab(self.plugin_widget, "Plugin Definition")

        self.editor_widget = ModelEditor(self)
        self.tabWidget.addTab(self.editor_widget, "Model editor")
        
    def addSignals(self):
        """
        Define slots for common widget signals
        """
        # buttons
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Help).clicked.connect(self.onHelp)
        # custom signals
        self.sasmodelChangedSignal.connect(self.updateSasModel)

    def onHelp(self):
        """
        Bring up the Model Editor Documentation whenever
        the HELP button is clicked.
        Calls Documentation Window with the path of the location within the
        documentation tree (after /doc/ ....".
        """
        location = "/user/sasgui/perspectives/fitting/plugin.html"
        self.parent.showHelp(location)

    def updateSasModel(self, model=None):
        """
        Respond to sasmodel update in one of the tabs
        """
        assert(model)
        pass

        

