# global
import sys
import os
import logging 

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from sas.qtgui.Perspectives.Fitting import ModelUtilities

from sas.qtgui.Utilities.UI.PluginManagerUI import Ui_PluginManagerUI


class PluginManager(QtWidgets.QDialog, Ui_PluginManagerUI):
    """
    Class describing the model plugin manager.
    This is a simple list widget allowing for viewing/adding/deleting custom models.
    """
    def __init__(self, parent=None):
        super(PluginManager, self).__init__()
        self.setupUi(self)

        self.parent = parent

        # globals
        self.readModels()

        # internal representation of the parameter list
        # {<row>: (<parameter>, <value>)}
        self.plugin_dict = {}

        # Initialize signals
        self.addSignals()

        # Initialize widgets
        self.addWidgets()

    def readModels(self):
        """
        Read in custom models from the default location
        """
        plugins = ModelUtilities._find_models()
        models = list(plugins.keys())
        self.lstModels.addItems(models)

    def addSignals(self):
        """
        Define slots for widget signals
        """
        self.cmdOK.clicked.connect(self.accept)
        self.cmdDelete.clicked.connect(self.onDelete)
        #self.tblParams.cellChanged.connect(self.onParamsChanged)

    def addWidgets(self):
        """
        Initialize various widgets in the dialog
        """
        pass

    def onDelete(self):
        """
        Remove the file containing the selected plugin
        """
        plugins_to_delete = [s.data() for s in self.lstModels.selectionModel().selectedRows()]

        delete_msg = "Are you sure you want to remove the selected plugins?"
        reply = QtWidgets.QMessageBox.question(
            self,
            'Warning',
            delete_msg,
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No)

        # Exit if no
        if reply == QtWidgets.QMessageBox.No:
            return

        for plugin in plugins_to_delete:
            name = os.path.join(ModelUtilities.find_plugins_dir(), plugin + ".py")
            os.remove(name)

        self.parent.communicate.customModelDirectoryChanged.emit()
