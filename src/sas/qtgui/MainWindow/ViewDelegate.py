from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import sas.qtgui.Utilities.GuiUtils as GuiUtils

class CategoryViewDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate for appearance and behavior control of the polydispersity view
    """

    combo_updated = QtCore.pyqtSignal(str, int)
    filename_updated = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Overwrite generic constructor to allow for some globals
        """
        super(QtWidgets.QStyledItemDelegate, self).__init__()

        self.model_name = 1
        self.model_category = 2

    def editableParameters(self):
        return [self.model_enable, self.model_category]

    # def createEditor(self, widget, option, index):
    #     # Remember the current choice
    #     if not index.isValid():
    #         return 0
    #     elif index.column() in self.editableParameters():
    #         self.editor = QtGui.QLineEdit(widget)
    #         validator = QtGui.QDoubleValidator()
    #         self.editor.setValidator(validator)
    #         return self.editor
    #     else:
    #         QtGui.QStyledItemDelegate.createEditor(self, widget, option, index)

    # def paint(self, painter, option, index):
    #     """
    #     Overwrite generic painter for certain columns
    #     """
    #     if index.column() in (self.model_enable):
    #         # Units - present in nice HTML
    #         options = QtGui.QStyleOptionViewItemV4(option)
    #         self.initStyleOption(options,index)
    #
    #         style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
    #
    #         # Prepare document for inserting into cell
    #         doc = QtGui.QTextDocument()
    #
    #         # Convert the unit description into HTML
    #         text_html = GuiUtils.convertUnitToHTML(str(options.text))
    #         doc.setHtml(text_html)
    #
    #         # delete the original content
    #         options.text = ""
    #         style.drawControl(QtGui.QStyle.CE_ItemViewItem, options, painter, options.widget);
    #
    #         context = QtGui.QAbstractTextDocumentLayout.PaintContext()
    #         textRect = style.subElementRect(QtGui.QStyle.SE_ItemViewItemText, options)
    #
    #         painter.save()
    #         painter.translate(textRect.topLeft())
    #         painter.setClipRect(textRect.translated(-textRect.topLeft()))
    #         # Draw the QTextDocument in the cell
    #         doc.documentLayout().draw(painter, context)
    #         painter.restore()
    #     else:
    #         # Just the default paint
    #         QtGui.QStyledItemDelegate.paint(self, painter, option, index)
