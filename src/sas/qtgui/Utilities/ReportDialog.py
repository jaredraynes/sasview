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
    def __init__(self, parent = None, report_list=None):

        super(ReportDialog, self).__init__(parent._parent)
        self.setupUi(self)

        self.data = report_list
        self.parent = parent
        if hasattr(self.parent, "communicate"):
            self.communicate = parent.communicate

        # Fill in the table from input data
        self.setupDialog(self.data)

        # Command buttons
        self.cmdPrint.clicked.connect(self.onPrint)
        self.cmdSave.clicked.connect(self.onSave)

    def setupDialog(self, output=None):
        """
        """
        if output is not None:
            self.txtBrowser.setHtml(output)

    def onPrint(self):
        """
        """
        pass

    def onSave(self):
        """
        """
        pass

