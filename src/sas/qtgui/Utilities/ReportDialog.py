import os
import time
import logging
import webbrowser

from PyQt5 import QtCore, QtWidgets

import sas.qtgui.Utilities.GuiUtils as GuiUtils

from sas.qtgui.Utilities.UI.ReportDialogUI import Ui_ReportDialogUI


class ReportDialog(QtWidgets.QDialog, Ui_ReportDialogUI):
    """
    Class for stateless grid-like printout of model parameters for mutiple models
    """
    def __init__(self, parent = None, output_data=None):

        super(ReportDialog, self).__init__()
        self.setupUi(self)

        self.data = output_data
        self.parent = parent
        if hasattr(self.parent, "communicate"):
            self.communicate = parent.communicate

        # Fill in the table from input data
        self.setupDialog(output_data)

        # Command buttons
        self.cmdPrint.clicked.connect(self.onPrint)
        self.cmdSave.clicked.connect(self.onSave)

    def setupDialog(self, output=None):
        """
        """
        if output is not None:
            self.txtbrowser.setHtml(output)

    def onPrint(self):
        """
        """
        pass

    def onSave(self):
        """
        """
        pass

