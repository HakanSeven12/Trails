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

"""Provides the task panel code for the Cluster Exporter tool."""

import FreeCAD, FreeCADGui
from PySide2 import QtWidgets

from trails_variables import ui_path
from .task_panel import TaskPanel
from ..get import get_clusters


class TaskClusterExport(TaskPanel):
    def __init__(self):
        # Set UI.
        self.form = FreeCADGui.PySideUic.loadUi(ui_path + '/export_points.ui')
        self.form.BrowseB.clicked.connect(self.file_destination)

        # Add point groups to QListWidget
        clusters = get_clusters.get()
        self.group_dict = {}
        for child in clusters.Group:
            if child.Proxy.Type == 'Trails::Cluster':
                self.group_dict[child.Label] = child
                self.form.PointGroupsLW.addItem(child.Label)

    def file_destination(self):
        """
        Get file destination.
        """
        # Select file
        parameter = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General")
        path = parameter.GetString("FileOpenSavePath")
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            None, 'Save File', path, Filter='*.txt')

        # Add ".txt" if needed
        if file_name[0][-4:] == ".txt":
            fn = file_name[0]
        else:
            fn = file_name[0] + ".txt"

        self.form.FileDestinationLE.setText(fn)

    def accept(self):
        """
        Export selected point group(s).
        """
        # Get user inputs
        line_edit = self.form.FileDestinationLE
        point_name = self.form.PointNameLE.text()
        northing = self.form.NorthingLE.text()
        easting = self.form.EastingLE.text()
        elevation = self.form.ElevationLE.text()
        description = self.form.DescriptionLE.text()

        if line_edit.text().strip() == "" or self.form.PointGroupsLW.count() < 1:
            return

        # Set delimiter
        if self.form.DelimiterCB.currentText() == "Space":
            delimiter = ' '
        elif self.form.DelimiterCB.currentText() == "Comma":
            delimiter = ','

        # Create point file
        try:
            file = open(line_edit.text(), 'w')
        except Exception:
            FreeCAD.Console.PrintMessage("Can't open file")

        counter = 1
        # Get selected point groups
        for selection in self.form.PointGroupsLW.selectedIndexes():
            group = self.group_dict[selection.data()]

            # Print points to the file
            for p in group.Vectors:
                index = group.Vectors.index(p)
                x = str(round(p.x/1000, 3))
                y = str(round(p.y/1000, 3))
                z = str(round(p.z/1000, 3))

                if group.PointNames:
                    pn = group.PointNames[index]
                else:
                    pn = counter
                    counter += 1

                des = ''
                if group.Descriptions:
                    des = group.Descriptions[index]

                format = [pn, x, y, z, des]
                file.write(delimiter.join(format) +"\n")
        file.close()
        FreeCADGui.Control.closeDialog()