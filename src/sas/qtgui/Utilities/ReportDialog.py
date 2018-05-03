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
        Display the HTML content in the browser.
        """
        if output is not None:
            self.txtBrowser.setHtml(output)

    def onPrint(self):
        """
        Display the print dialog and send the report to printer
        """
        pass

    def onSave(self):
        """
        Display the Save As... prompt and save the report if instructed so
        """
        # choose user's home directory
        location = os.path.expanduser('~')
        default_name = os.path.join(location, 'fitting_report.pdf')
        kwargs = {
            'parent': self,
            'caption'   : 'Save Report',
            'directory': default_name,
            'filter': 'PDF file (*.pdf);;HTML file (*.html);;Text file (*.txt)',
            'options': QtWidgets.QFileDialog.DontUseNativeDialog}
        # Query user for filename.
        filename_tuple = QtWidgets.QFileDialog.getSaveFileName(**kwargs)
        filename = filename_tuple[0]
        if not filename:
            return
        extension = filename_tuple[1]
        try:
            ext =  extension[extension.find("(")+1:extension.find(")")]
        except IndexError as ex:
            # (ext) not found...
            logging.error("Error while saving report. " + str(ex))
            return
        _, extension = os.path.splitext(filename)
        if not extension:
            filename = '.'.join((filename, ext))

        if ext.lower() == ".txt":
            onTXTSave(self.data, filename)
        if ext.lower() == ".pdf":
            self.HTML2PDF(self.data, filename)


    def HTML2PDF(self, data, filename):
        """
        Create a PDF file from html source string.
        Returns True is the file creation was successful.
        : data: html string
        : filename: name of file to be saved
        """
        try:
            from xhtml2pdf import pisa
            # open output file for writing (truncated binary)
            resultFile = open(filename, "w+b")
            # convert HTML to PDF
            pisaStatus = pisa.CreatePDF(data, dest=resultFile)
            # close output file
            resultFile.close()
            self.Update()
            return pisaStatus.err
        except Exception:
            logging.error("Error creating pdf: %s" % sys.exc_value)
        return False


