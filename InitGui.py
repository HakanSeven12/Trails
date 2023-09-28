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

"""Initialization of the Trails workbench (GUI interface)."""

import FreeCADGui


class TrailsWorkbench(FreeCADGui.Workbench):
    """
    Class which gets initiated at startup of the GUI.
    """
    from trails_variables import icons_path

    MenuText = 'Trails'
    ToolTip = 'Transportation and Geomatics Engineering Workbench'
    Icon = icons_path + '/workbench.svg'

    def __init__(self):
        #dictionary key = name of command / command group.
        #'gui' - locations in gui where commands are accessed, (summed bitflags)
        #'cmd' - list of commands to display
        #'group' - Tuple containing the subgroup description and type.  None/undefined if no group

        self.menu = 1
        self.toolbar = 2
        self.context = 4
        self.group = 8

        self.command_ui = {
            'Cluster Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Create Cluster',
                    'Import Points',
                    'Export Points']},

            'Terrain Tools': {
                'gui': self.menu + self.toolbar + self.context,
                'cmd': ['Create Terrain',
                    'Add Data',
                    'Terrain Editor']},

            'Section Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Create Region',
                    'Create Sections',
                    'Compute Areas',
                    'Create Table']},

            'Pad Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Create Pad']},

            'Alignment': {
                'gui': self.menu + self.toolbar + self.context,
                'cmd': ['LandXML Importer']},

            'Coordinate System': {
                'gui': self.toolbar,
                'cmd': ['Geo Widget']},

            'Add Data': {
                'gui': self.group,
                'tooltip': 'Add Data',
                'type': 'Trails::Terrain',
                'cmd': ['Import Points',
                    'Add Cluster']},

            'Terrain Editor': {
                'gui': self.group,
                'tooltip': 'Edit Terrain',
                'type': 'Trails::Terrain',
                'cmd': ['Add Point',
                    'Delete Triangle',
                    'Swap Edge',
                    'Smooth Terrain']}
        }

    def GetClassName(self):
        """
        Return the workbench classname.
        """
        return 'Gui::PythonWorkbench'

    def Initialize(self):
        """
        Called when the workbench is first activated.
        """
        import DraftTools
        from trails_variables import CommandGroup
        from Trails.guitools import gui_cluster, gui_point_importer, gui_point_exporter,\
            gui_terrain, gui_terrain_data, gui_terrain_editor, gui_region, gui_sections,\
            gui_volume, gui_table, gui_pad, gui_landxml_importer, gui_geowidget

        for palette, tool in self.command_ui.items():
            if tool['gui'] & self.toolbar:
                self.appendToolbar(palette, tool['cmd'])

            if tool['gui'] & self.menu:
                self.appendMenu(palette, tool['cmd'])

            if tool['gui'] & self.group:
                FreeCADGui.addCommand(palette, CommandGroup(
                    tool['cmd'], tool['tooltip'], tool['type']))

    def Activated(self):
        """
        Called when switching to this workbench
        """
        if hasattr(FreeCADGui, "Snapper"):
            FreeCADGui.Snapper.show()
            import draftutils.init_draft_statusbar as dsb
            dsb.show_draft_statusbar()

    def Deactivated(self):
        """
        Called when switiching away from this workbench
        """
        if hasattr(FreeCADGui, "Snapper"):
            FreeCADGui.Snapper.hide()
            import draftutils.init_draft_statusbar as dsb
            dsb.hide_draft_statusbar()

    def ContextMenu(self, recipient):
        """
        Right-click menu options
        """
        # "recipient" will be either "view" or "tree"

        for _k, _v in self.fn.items():
            if _v['gui'] & self.context:
                self.appendContextMenu(_k, _v['cmds'])

FreeCADGui.addWorkbench(TrailsWorkbench())
