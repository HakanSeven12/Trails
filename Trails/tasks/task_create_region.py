# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2021 Hakan Seven <hakanseven12@gmail.com>               *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""Provides the general task panel code to select target object type."""

import FreeCAD, FreeCADGui

from libs import ui_path
from .task_panel import TaskPanel
from..make import make_region


class TaskCreateRegion(TaskPanel):

    def __init__(self,group):
        self.form = FreeCADGui.PySideUic.loadUi(ui_path + '/selector.ui')
        self.form.setWindowTitle('Select from ' + group.Label)
        self.form.setWindowIcon(group.ViewObject.Icon)
        self.list_targets(group)

    def list_targets(self, group):
        self.group_dict = {}
        for i in group.Group:
            self.group_dict[i.Label] = i

        keys = list(self.group_dict.keys())
        self.form.lw_objects.addItems(keys)

    def accept(self):
        alignment = self.form.lw_objects.selectedItems()[0]
        make_region.create(self.group_dict[alignment.text()])

        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()