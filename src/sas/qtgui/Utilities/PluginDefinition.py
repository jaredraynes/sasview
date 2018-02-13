# global
import sys
import os
import logging 

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import sas.qtgui.Utilities.GuiUtils as GuiUtils

from sas.qtgui.Utilities.UI.PluginDefinitionUI import Ui_PluginDefinition

# txtName
# txtDescription
# chkOverwrite
# tblParams
# tblParamsPD
# txtFunction

class PluginDefinition(QtWidgets.QDialog, Ui_PluginDefinition):
    """
    """
    def __init__(self, parent=None):
        super(PluginDefinition, self).__init__(parent)
        self.setupUi(self)

        # globals
        self.sasmodel = None

        self.addSignals()

    def addSignals(self):
        """
        Define slots for widget signals
        """
        self.txtName.editingFinished.connect(self.onPluginNameChanged)
        self.txtDescription.editingFinished.connect(self.onDescriptionChanged)
        self.tblParams.cellChanged.connect(self.onParamsChanged)
        self.tblParamsPD.cellChanged.connect(self.onParamsPDChanged)
        # QTextEdit doesn't have a signal for edit finish, so we respond to text changed.
        # Possibly a slight overkill.
        self.txtFunction.textChanged.connect(self.onFunctionChanged)
        self.chkOverwrite.toggled.connect(self.onOverwrite)

    def onPluginNameChanged(self):
        """
        Respond to changes in plugin name
        """
        logging.info("onPluginNameChanged TRIGGERED")
        pass

    def onDescriptionChanged(self):
        """
        Respond to changes in plugin description
        """
        logging.info("onDescriptionChanged TRIGGERED")
        pass

    def onParamsChanged(self, row, column):
        """
        Respond to changes in non-polydisperse parameter table
        """
        logging.info("onParamsChanged TRIGGERED")
        pass

    def onParamsPDChanged(self, row, column):
        """
        Respond to changes in non-polydisperse parameter table
        """
        logging.info("onParamsPDChanged TRIGGERED")
        pass

    def onFunctionChanged(self):
        """
        Respond to changes in function body
        """
        # keep in mind that this is called every time the text changes.
        # mind the performance!
        logging.info("onFunctionChanged TRIGGERED")
        pass

    def onOverwrite(self):
        """
        Respond to change in file overwrite checkbox
        """
        logging.info("onOverwrite TRIGGERED")
        pass