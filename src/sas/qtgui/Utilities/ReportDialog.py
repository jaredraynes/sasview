import os
import time
import logging
import webbrowser

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtPrintSupport

import sas.qtgui.Utilities.GuiUtils as GuiUtils

from sas.qtgui.Utilities.UI.ReportDialogUI import Ui_ReportDialogUI


class ReportDialog(QtWidgets.QDialog, Ui_ReportDialogUI):
    """
    Class for stateless grid-like printout of model parameters for mutiple models
    """
    def __init__(self, parent = None, report_list=None):

        super(ReportDialog, self).__init__(parent._parent)
        self.setupUi(self)

        assert(isinstance(report_list, list))
        assert(len(report_list) == 3)

        self.data_html, self.data_txt, self.data_images = report_list
        self.parent = parent
        if hasattr(self.parent, "communicate"):
            self.communicate = parent.communicate

        # Fill in the table from input data
        self.setupDialog(self.data_html)

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
        # Define the printer
        printer = QtPrintSupport.QPrinter()

        # Display the print dialog
        dialog = QtPrintSupport.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print")
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        try:
            self.txtBrowser.document().print(printer)
        except Exception as ex:
            logging.error("Print report failed with: " + str(ex))

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
            ext =  extension[extension.find("(")+2:extension.find(")")]
        except IndexError as ex:
            # (ext) not found...
            logging.error("Error while saving report. " + str(ex))
            return
        basename, extension = os.path.splitext(filename)
        if not extension:
            filename = '.'.join((filename, ext))

        pictures = self.getPictures(basename)

        # translate png references int html from in-memory name to on-disk name
        # TODO: fix for Qt5 - replace "data:image/png..." with basename+'_img.png'
        html = self.data_html.replace("memory:img_fit", basename+'_img')

        if ext.lower() == ".txt":
            self.onTXTSave(self.data_txt, filename)
        if ext.lower() == ".html":
            self.onHTMLSave(html, filename)
        if ext.lower() == ".pdf":
            pdf_success = self.HTML2PDF(html, filename)
            # delete images used to create the pdf
            for pic_name in pictures:
                os.remove(pic_name)
            #open pdf viewer
            if pdf_success:
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(filename)
                    elif sys.platform == "darwin":  # Mac
                        os.system("open %s" % filename)
                except Exception as exc:
                    # cannot open pdf
                    logging.error(str(exc))

    def getPictures(self, basename):
        """
        Returns list of saved MPL figures
        """
        # save figures
        pictures = []
        for num, image in enumerate(self.data_images):
            pic_name = basename + '_img%s.png' % num
            # save the image for use with pdf writer
            image.savefig(pic_name)
            pictures.append(pic_name)
        return pictures

    def onTXTSave(self, data, filename):
        """
        Simple txt file serializatio
        """
        with open(filename, 'w') as f:
            f.write(data)

    def onHTMLSave(self, html, filename):
        """
        HTML file write
        """
        with open(filename, 'w') as f:
            f.write(html)

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
            return pisaStatus.err
        except Exception as ex:
            logging.error("Error creating pdf: %s" % str(ex))
        return False


