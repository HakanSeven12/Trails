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

"""Provides the task panel code for the Cluster Importer tool."""

import FreeCAD, FreeCADGui
from PySide2 import QtCore, QtWidgets
import csv, os

from libs import ui_path
from .task_panel import TaskPanel
from ..get import get_clusters, get_georigin
from ..make import make_cluster


class TaskClusterImport(TaskPanel):
    """
    Command to import point file which includes survey data.
    """

    def __init__(self):
        """
        Constructor
        """
        # Get *.ui file(s)
        self.form = FreeCADGui.PySideUic.loadUi(ui_path + "/import_points.ui")

        # UI connections
        self.form.AddB.clicked.connect(self.add_file)
        self.form.RemoveB.clicked.connect(self.remove_file)
        self.form.SelectedFilesLW.itemSelectionChanged.connect(self.preview)
        self.form.PointGroupChB.stateChanged.connect(self.pg_selection)
        self.form.CreateGroupB.clicked.connect(self.load_newpg_ui)

        # Get or create 'Point Groups'.
        get_georigin.get()
        clusters = get_clusters.get()

        # Add point groups to QComboBox
        self.group_dict = {}
        for cluster in clusters.Group:
            if cluster.Proxy.Type == 'Trails::Cluster':
                self.group_dict[cluster.Label] = cluster
                self.form.SubGroupListCB.addItem(cluster.Label)

    def add_file(self):
        """
        Add point files to importer
        """
        # Get selected point file(s) and add them to QListWidget
        parameter = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General")
        path = parameter.GetString("FileOpenSavePath")
        file_name = QtWidgets.QFileDialog.getOpenFileNames(
                        None, "Select one or more files to open",
                        path, 'All Files (*.*)')
        self.form.SelectedFilesLW.addItems(file_name[0])

    def remove_file(self):
        """
        Remove point files from importer
        """
        # Get selected point file(s) and remove them from QListWidget
        for item in self.form.SelectedFilesLW.selectedItems():
            self.form.SelectedFilesLW.takeItem(self.form.SelectedFilesLW.row(item))

    def pg_selection(self):
        """
        Enable or disable 'Create Point Group' feature
        """
        #If check box status changed, enable or disable combo box and push button.
        if self.form.PointGroupChB.isChecked():
            self.form.SubGroupListCB.setEnabled(True)
            self.form.CreateGroupB.setEnabled(True)
        else:
            self.form.SubGroupListCB.setEnabled(False)
            self.form.CreateGroupB.setEnabled(False)

    def load_newpg_ui(self):
        """
        Load 'Create Point Group' UI.
        """
        # Set and show 'Create Point Group' UI
        subpanel = FreeCADGui.PySideUic.loadUi(ui_path + "/create_pg.ui")
        subpanel.setParent(self.form)
        subpanel.setWindowFlags(QtCore.Qt.Window)
        subpanel.show()

        # UI connections
        self.subpanel = subpanel
        subpanel.OkB.clicked.connect(self.create_pg)
        subpanel.CancelB.clicked.connect(subpanel.close)

    def create_pg(self):
        """
        Create new point group
        """
        # Create new point group and add it to QComboBox
        group_name = self.subpanel.PointGroupNameLE.text()
        new_group = make_cluster.create(name=group_name)
        self.group_dict[new_group.Label] = new_group
        self.form.SubGroupListCB.addItem(new_group.Label)
        self.subpanel.close()

    def file_reader(self, file, operation):
        """
        Read file points and show them to user or add them to point group
        """
        # Get user inputs
        names = []
        vectors = []
        descriptions = []

        counter = 1
        point_name = self.form.PointNameLE.text()
        northing = self.form.NorthingLE.text()
        easting = self.form.EastingLE.text()
        elevation = self.form.ElevationLE.text()
        description = self.form.DescriptionLE.text()

        # Set delimiter
        combobox = self.form.DelimiterCB

        if combobox.currentText() == "Space":
            reader = csv.reader(file, delimiter=' ',
                skipinitialspace=True)

        if combobox.currentText() == "Comma":
            reader = csv.reader(file, delimiter=',')

        if combobox.currentText() == "Tab":
            reader = csv.reader(file, delimiter='\t')

        table_widget = self.form.PreviewTW

        # Read files
        for row in reader:
            pn = int(point_name) - 1
            n = int(northing) - 1
            e = int(easting) - 1
            z = int(elevation) - 1
            d = int(description) - 1

            # Show point file data in QTableView
            if operation == "Preview":
                numRows = table_widget.rowCount()
                table_widget.insertRow(numRows)

                try:
                    table_widget.setItem(
                        numRows, 0, QtWidgets.QTableWidgetItem(row[pn]))
                except Exception:
                    pass

                try:
                    table_widget.setItem(
                        numRows, 1, QtWidgets.QTableWidgetItem(row[e]))
                except Exception:
                    pass

                try:
                    table_widget.setItem(
                        numRows, 2, QtWidgets.QTableWidgetItem(row[n]))
                except Exception:
                    pass

                try:
                    table_widget.setItem(
                        numRows, 3, QtWidgets.QTableWidgetItem(row[z]))
                except Exception:
                    pass

                try:
                    table_widget.setItem(
                        numRows, 4, QtWidgets.QTableWidgetItem(row[d]))
                except Exception:
                    pass

                if counter == 500:
                    break
                else:
                    counter += 1

            # Add points to point group
            elif operation == "Import":
                try: name = row[pn]
                except Exception: name = ""

                try: des = row[d]
                except Exception: des = ""

                names.append(name)
                descriptions.append(des)
                vector = FreeCAD.Vector(float(row[e]), float(row[n]), float(row[z]))
                vectors.append(vector.multiply(1000))

        return names, vectors, descriptions

    def preview(self):
        """
        Show a preview for selected point file
        """
        # Get selected file
        selected_file = self.form.SelectedFilesLW.selectedItems()

        # Separate path and file name
        if selected_file:
            head, tail = os.path.split(selected_file[0].text())
            self.form.PreviewL.setText("Preview: " + tail)
            self.form.PreviewTW.setRowCount(0)

            # Send selected point file to preview
            file = open(selected_file[0].text(), 'r')
            self.file_reader(file, "Preview")

    def accept(self):
        """
        Import added files to selected point group
        """
        # Get user inputs
        text = self.form.SubGroupListCB.currentText()

        # If check box is checked get selected item in QComboBox
        if self.form.PointGroupChB.isChecked():
            group = self.group_dict[text]
        else:
            # Get or create 'Points'.
            group = make_cluster.main_cluster()

        # Read Points from file
        list_widget = self.form.SelectedFilesLW
        if list_widget.count() < 1:
            FreeCAD.Console.PrintMessage("No Files selected")
            return

        items = []
        for i in range(list_widget.count()):
            items.append(list_widget.item(i))
        file_paths = [i.text() for i in items]
        names = group.PointNames.copy()
        points = group.Vectors.copy()
        descriptions = group.Descriptions.copy()

        for path in file_paths:
            file = open(path, 'r')
            names, vectors, descriptions =self.file_reader(file, "Import")
            names.extend(names)
            points.extend(vectors)
            descriptions.extend(descriptions)

        group.PointNames = names
        group.Vectors = points
        group.Descriptions = descriptions
        group.recompute()
        FreeCADGui.Control.closeDialog()

    def needsFullSpace(self):
        return True
