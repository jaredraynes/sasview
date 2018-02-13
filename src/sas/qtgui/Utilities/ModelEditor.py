# global
import sys
import os
import types
import webbrowser

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import sas.qtgui.Utilities.GuiUtils as GuiUtils

from sas.qtgui.Utilities.UI.ModelEditor import Ui_ModelEditor

class ModelEditor(QtWidgets.QDialog, Ui_ModelEditor):
    """
    """
    def __init__(self, parent=None):
        super(ModelEditor, self).__init__(parent)
        self.setupUi(self)
