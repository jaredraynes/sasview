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
    Class describing the "simple" plugin editor.
    This is a simple series of widgets allowing for specifying
    model form and parameters.
    """
    modelModified = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(PluginDefinition, self).__init__(parent)
        self.setupUi(self)

        # globals
        # model - internal representation of the new model plugin
        #self.model = {}
        self.initializeModel()
        # internal representation of the parameter list
        # {<row>: (<parameter>, <value>)}
        self.parameter_dict = {}

        # Initialize signals
        self.addSignals()

        # Initialize widgets
        self.addWidgets()

    def addWidgets(self):
        """
        Initialize various widgets in the dialog
        """
        # Initial text in the function table
        text =\
"""y = x

return y
"""
        self.txtFunction.insertPlainText(text)

        # Validators
        #rx = QtCore.QRegExp(r'^[\w,\s-]+$')
        #rx = QtCore.QRegExp("[a-z-A-Z_]+")
        rx = QtCore.QRegExp("^[A-Za-z0-9_]*$")

        txt_validator = QtGui.QRegExpValidator(rx)
        self.txtName.setValidator(txt_validator)

    def initializeModel(self):
        """
        Define the dictionary for internal data representation
        """
        # Define the keys
        self.model = {
            'filename':'',
            'overwrite':False,
            'description':'',
            'parameters':{},
            'pd_parameters':{},
            'text':''}

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
        self.model['filename'] = self.txtName.text()
        self.modelModified.emit()

    def onDescriptionChanged(self):
        """
        Respond to changes in plugin description
        """
        self.model['description'] = self.txtDescription.text()
        self.modelModified.emit()

    def onParamsChanged(self, row, column):
        """
        Respond to changes in non-polydisperse parameter table
        """
        param = value = None
        if self.tblParams.item(row, 0):
            param = self.tblParams.item(row, 0).data(0)
        if self.tblParams.item(row, 1):
            value = self.tblParams.item(row, 1).data(0)

        # If modified, just update the dict
        self.parameter_dict[row] = (param, value)
        self.model['parameters'] = self.parameter_dict

        # Check if the update was Value for last row. If so, add a new row
        if column == 1 and row == self.tblParams.rowCount()-1:
            # Add a row
            self.tblParams.insertRow(self.tblParams.rowCount())
        self.modelModified.emit()

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
        self.model['text'] = self.txtFunction.toPlainText().lstrip().rstrip()
        self.modelModified.emit()

    def onOverwrite(self):
        """
        Respond to change in file overwrite checkbox
        """
        self.model['overwrite'] = self.chkOverwrite.isChecked()
        self.modelModified.emit()

    def getModel(self):
        """
        Return the current plugin model
        """
        return self.model
