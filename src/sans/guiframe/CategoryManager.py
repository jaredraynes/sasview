#!/usr/bin/python

"""
This software was developed by Institut Laue-Langevin as part of
Distributed Data Analysis of Neutron Scattering Experiments (DANSE).

Copyright 2012 Institut Laue-Langevin

"""


import wx
import sys
import os
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from collections import defaultdict
import cPickle as pickle
from sans.guiframe.events import ChangeCategoryEvent
from sans.guiframe.CategoryInstaller import CategoryInstaller
IS_MAC = (sys.platform == 'darwin')

""" Notes
The category manager mechanism works from 3 data structures used:
- self.master_category_dict: keys are the names of categories, 
the values are lists of tuples,
the first being the model names (the models belonging to that 
category), the second a boolean
of whether or not the model is enabled
- self.by_model_dict: keys are model names, values are a list 
of categories belonging to that model
- self.model_enabled_dict: keys are model names, values are 
bools of whether the model is enabled
use self._regenerate_model_dict() to create the latter two 
structures from the former
use self._regenerate_master_dict() to create the first 
structure from the latter two

The need for so many data structures comes from the fact 
sometimes we need fast access 
to all the models in a category (eg user selection from the gui) 
and sometimes we need access to all the categories 
corresponding to a model (eg user modification of model categories)

"""



class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, 
                    ListCtrlAutoWidthMixin):
    """
    Taken from
    http://zetcode.com/wxpython/advanced/
    """

    def __init__(self, parent, callback_func):
        """
        Initialization
        :param parent: Parent window
        :param callback_func: A function to be called when
        an element is clicked
        """
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT \
                                 | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

        self.callback_func = callback_func
        
    def OnCheckItem(self, index, flag):
        """
        When the user checks the item we need to save that state
        """
        self.callback_func(index, flag)
    

class CategoryManager(wx.Frame):
    """
    A class for managing categories
    """
    def __init__(self, parent, win_id, title):
        """
        Category Manager Dialog class
        :param win_id: A new wx ID
        :param title: Title for the window
        """
        
        # make sure the category file is where it should be
        self.performance_blocking = False

        self.master_category_dict = defaultdict(list)
        self.by_model_dict = defaultdict(list)
        self.model_enabled_dict = defaultdict(bool)

        wx.Frame.__init__(self, parent, win_id, title, size=(660, 400))

        panel = wx.Panel(self, -1)
        self.parent = parent

        self._read_category_info()


        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(panel, -1)
        right_panel = wx.Panel(panel, -1)

        self.cat_list = CheckListCtrl(right_panel, self._on_check)
        self.cat_list.InsertColumn(0, 'Model', width = 280)
        self.cat_list.InsertColumn(1, 'Category', width = 240)

        self._fill_lists()  
        self._regenerate_model_dict()
        self._set_enabled()      

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        sel = wx.Button(left_panel, -1, 'Enable All', size=(100, -1))
        des = wx.Button(left_panel, -1, 'Disable All', size=(100, -1))
        modify_button = wx.Button(left_panel, -1, 'Modify', 
                                  size=(100, -1))
        ok_button = wx.Button(left_panel, -1, 'OK', size=(100, -1))
        cancel_button = wx.Button(left_panel, -1, 'Cancel', 
                                  size=(100, -1))        

        

        self.Bind(wx.EVT_BUTTON, self._on_selectall, 
                  id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_deselectall, 
                  id=des.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_apply, 
                  id = modify_button.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_ok, 
                  id = ok_button.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_cancel, 
                  id = cancel_button.GetId())

        vbox2.Add(modify_button, 0, wx.TOP, 10)
        vbox2.Add((-1, 20))
        vbox2.Add(sel)
        vbox2.Add(des)
        vbox2.Add((-1, 20))
        vbox2.Add(ok_button)
        vbox2.Add(cancel_button)

        left_panel.SetSizer(vbox2)

        vbox.Add(self.cat_list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))


        right_panel.SetSizer(vbox)

        hbox.Add(left_panel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(right_panel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)
        self.performance_blocking = True


        self.Centre()
        self.Show(True)

        # gui stuff finished

    def _on_check(self, index, flag):
        """
        When the user checks an item we need to immediately save that state.
        :param index: The index of the checked item
        :param flag: True or False whether the item was checked
        """
        if self.performance_blocking:
            # for computational reasons we don't want to 
            # call this function every time the gui is set up
            model_name = self.cat_list.GetItem(index, 0).GetText()
            self.model_enabled_dict[model_name] = flag
            self._regenerate_master_dict()


    def _fill_lists(self):
        """
        Expands lists on the GUI
        """
        self.cat_list.DeleteAllItems()
        model_name_list = [model for model in self.by_model_dict]
        model_name_list.sort()

        for model in model_name_list:
            index = self.cat_list.InsertStringItem(sys.maxint, model)
            self.cat_list.SetStringItem(index, 1, \
                                            str(self.by_model_dict[model]).\
                                            replace("'","").\
                                            replace("[","").\
                                            replace("]",""))


            
    def _set_enabled(self):
        """
        Updates enabled models from self.model_enabled_dict
        """
        num = self.cat_list.GetItemCount()
        for i in range(num):
            model_name = self.cat_list.GetItem(i, 0).GetText()
            self.cat_list.CheckItem(i, 
                                    self.model_enabled_dict[model_name] )
                                    


    def _on_selectall(self, event):
        """
        Callback for 'enable all'
        """
        self.performance_blocking = False
        num = self.cat_list.GetItemCount()
        for i in range(num):
            self.cat_list.CheckItem(i)
        for model in self.model_enabled_dict:
            self.model_enabled_dict[model] = True
        self._regenerate_master_dict()
        self.performance_blocking = True

    def _on_deselectall(self, event):
        """
        Callback for 'disable all'
        """
        self.performance_blocking = False
        num = self.cat_list.GetItemCount()
        for i in range(num):
            self.cat_list.CheckItem(i, False)
        for model in self.model_enabled_dict:
            self.model_enabled_dict[model] = False
        self._regenerate_master_dict()
        self.performance_blocking = True

    def _on_apply(self, event):
        """
        Call up the 'ChangeCat' dialog for category editing
        """

        if self.cat_list.GetSelectedItemCount() == 0:
            wx.MessageBox('Please select a model', 'Error',
                          wx.OK | wx.ICON_EXCLAMATION )

        else:
            selected_model = \
                self.cat_list.GetItem(\
                self.cat_list.GetFirstSelected(), 0).GetText()


            modify_dialog = ChangeCat(self, selected_model, 
                                      self._get_cat_list(),
                                      self.by_model_dict[selected_model])
            
            if modify_dialog.ShowModal() == wx.ID_OK:
                if not IS_MAC:
                    self.dial_ok(modify_dialog, selected_model)

    def dial_ok(self, dialog=None, model=None):
        """
        modify_dialog onclose
        """
        self.by_model_dict[model] = dialog.get_category()
        self._regenerate_master_dict()
        self._fill_lists()
        self._set_enabled()


    def _on_ok(self, event):
        """
        Close the manager
        """
        self._save_state()
        evt = ChangeCategoryEvent()
        wx.PostEvent(self.parent, evt)

        self.Destroy()

    def _on_cancel(self, event):
        """
        On cancel
        """
        self.Destroy()

    def _save_state(self):
        """
        Serializes categorization info to file
        """

        self._regenerate_master_dict()

        cat_file = open(CategoryInstaller.get_user_file(), 'wb')

        pickle.dump( self.master_category_dict, cat_file )
        
        cat_file.close()
   
    def _read_category_info(self):
        """
        Read in categorization info from file
        """
        try:
    		file = CategoryInstaller.get_user_file()
    		if os.path.isfile(file):
	            cat_file = open(file, 'rb')
	            self.master_category_dict = pickle.load(cat_file)
	        else:
	        	cat_file = open(CategoryInstaller.get_default_file(), 'rb')
        		self.master_category_dict = pickle.load(cat_file)
        	cat_file.close()
        except IOError:
            print 'Problem reading in category file. Please review'


        self._regenerate_model_dict()

    def _get_cat_list(self):
        """
        Returns a simple list of categories
        """
        cat_list = list()
        for category in self.master_category_dict.iterkeys():
            if not category == 'Uncategorized':
                cat_list.append(category)
    
        return cat_list

    def _regenerate_model_dict(self):
        """
        regenerates self.by_model_dict which has each model 
        name as the key
        and the list of categories belonging to that model
        along with the enabled mapping
        """
        self.by_model_dict = defaultdict(list)
        for category in self.master_category_dict:
            for (model, enabled) in self.master_category_dict[category]:
                self.by_model_dict[model].append(category)
                self.model_enabled_dict[model] = enabled

    def _regenerate_master_dict(self):
        """
        regenerates self.master_category_dict from 
        self.by_model_dict and self.model_enabled_dict
        """
        self.master_category_dict = defaultdict(list)
        for model in self.by_model_dict:
            for category in self.by_model_dict[model]:
                self.master_category_dict[category].append\
                    ((model, self.model_enabled_dict[model]))
    


class ChangeCat(wx.Dialog):
    """
    dialog for changing the categories of a model
    """

    def __init__(self, parent, title, cat_list, current_cats):
        """
        Actual editor for a certain category
        :param parent: Window parent
        :param title: Window title
        :param cat_list: List of all categories
        :param current_cats: List of categories applied to current model
        """
        wx.Dialog.__init__(self, parent, title = 'Change Category: '+title, size=(485, 425))

        self.current_cats = current_cats
        if str(self.current_cats[0]) == 'Uncategorized':
            self.current_cats = []
        self.parent = parent
        self.selcted_model = title
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.add_sb = wx.StaticBox(self, label = "Add Category")
        self.add_sb_sizer = wx.StaticBoxSizer(self.add_sb, wx.VERTICAL)
        gs = wx.GridSizer(3, 2, 5, 5)
        self.cat_list = cat_list
        
        self.cat_text = wx.StaticText(self, label = "Current categories: ")
        self.current_categories = wx.ListBox(self, 
                                             choices = self.current_cats
                                             , size=(300, 100))
        self.existing_check = wx.RadioButton(self, 
                                             label = 'Choose Existing')
        self.new_check = wx.RadioButton(self, label = 'Create new')
        self.exist_combo = wx.ComboBox(self, style = wx.CB_READONLY, 
                                       size=(220,-1), choices = cat_list)
        self.exist_combo.SetSelection(0)
        
        
        self.remove_sb = wx.StaticBox(self, label = "Remove Category")
        
        self.remove_sb_sizer = wx.StaticBoxSizer(self.remove_sb, 
                                                 wx.VERTICAL)

        self.new_text = wx.TextCtrl(self, size=(220, -1))
        self.ok_button = wx.Button(self, wx.ID_OK, "Done")
        self.add_button = wx.Button(self, label = "Add")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)
        self.remove_button = wx.Button(self, label = "Remove Selected")
        self.remove_button.Bind(wx.EVT_BUTTON, self.on_remove)

        self.existing_check.Bind(wx.EVT_RADIOBUTTON, self.on_existing)
        self.new_check.Bind(wx.EVT_RADIOBUTTON, self.on_newcat)
        self.existing_check.SetValue(True)

        vbox.Add(self.cat_text, flag = wx.LEFT | wx.TOP | wx.ALIGN_LEFT, 
                 border = 10)
        vbox.Add(self.current_categories, flag = wx.ALL | wx.EXPAND, 
                 border = 10  )

        gs.AddMany( [ (self.existing_check, 5, wx.ALL),
                      (self.exist_combo, 5, wx.ALL),
                      (self.new_check, 5, wx.ALL),
                      (self.new_text, 5, wx.ALL ),
                      ((-1,-1)),
                      (self.add_button, 5, wx.ALL | wx.ALIGN_RIGHT) ] )

        self.add_sb_sizer.Add(gs, proportion = 1, flag = wx.ALL, border = 5)
        vbox.Add(self.add_sb_sizer, flag = wx.ALL | wx.EXPAND, border = 10)

        self.remove_sb_sizer.Add(self.remove_button, border = 5, 
                                 flag = wx.ALL | wx.ALIGN_RIGHT)
        vbox.Add(self.remove_sb_sizer, 
                 flag = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 
                 border = 10)
        vbox.Add(self.ok_button, flag = wx.ALL | wx.ALIGN_RIGHT, 
                 border = 10)
        
        if self.current_categories.GetCount() > 0:
        	self.current_categories.SetSelection(0)
        self.new_text.Disable()
        self.SetSizer(vbox)
        self.Centre()
        self.Show(True)
        if IS_MAC:
            self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok_mac)

    def on_ok_mac(self, event):
        """
        On OK pressed (MAC only)
        """
        event.Skip()
        self.parent.dial_ok(self, self.selcted_model)
        self.Destroy()

    def on_add(self, event):
        """
        Callback for new category added
        """
        new_cat = ''
        if self.existing_check.GetValue():
            new_cat = str(self.exist_combo.GetValue())
        else:
            new_cat = str(self.new_text.GetValue())
            if new_cat in self.cat_list:
                wx.MessageBox('%s is already a model' % new_cat, 'Error',
                              wx.OK | wx.ICON_EXCLAMATION )
                return

        if new_cat in self.current_cats:
            wx.MessageBox('%s is already included in this model' \
                              % new_cat, 'Error',
                          wx.OK | wx.ICON_EXCLAMATION )
            return

        self.current_cats.append(new_cat)
        self.current_categories.SetItems(self.current_cats)
            
        
    def on_remove(self, event):
        """
        Callback for a category removed
        """
        if self.current_categories.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox('Please select a category to remove', 'Error',
                          wx.OK | wx.ICON_EXCLAMATION )
        else:
            self.current_categories.Delete( \
                self.current_categories.GetSelection())
            self.current_cats = self.current_categories.GetItems()

        

    def on_newcat(self, event):
        """
        Callback for new category added
        """
        self.new_text.Enable()
        self.exist_combo.Disable()


    def on_existing(self, event):    
        """
        Callback for existing category selected
        """
        self.new_text.Disable()
        self.exist_combo.Enable()

    def get_category(self):
        """
        Returns a list of categories applying to this model
        """
        if not self.current_cats:
            self.current_cats.append("Uncategorized")

        ret = list()
        for cat in self.current_cats:
            ret.append(str(cat))
        return ret

if __name__ == '__main__':
        
    
    if(len(sys.argv) > 1):
        app = wx.App()
        CategoryManager(None, -1, 'Category Manager', sys.argv[1])
        app.MainLoop()
    else:
        app = wx.App()
        CategoryManager(None, -1, 'Category Manager', sys.argv[1])
        app.MainLoop()

