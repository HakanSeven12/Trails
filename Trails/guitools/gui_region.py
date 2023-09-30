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

"""Provides GUI tools to create Region objects."""

import FreeCAD, FreeCADGui

from trails_variables import icons_path
from ..make import make_region
from ..get import get_alignments
from ..tasks import task_set_parent


class CreateRegion:
    """
    Command to create a new Region object for selected alignment
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return {
            'Pixmap': icons_path + '/CreateRegion.svg',
            'MenuText': "Create Region",
            'ToolTip': "Create Region for selected alignment"
            }

    def IsActive(self):
        """
        Define tool button activation situation
        """
        # Check for document
        if FreeCAD.ActiveDocument:
            return True
        return False

    def Activated(self):
        """
        Command activation method
        """
        # Check for selected object
        try:
            if selection[-1].Proxy.Type == 'Trails::Alignment':
                selection = FreeCADGui.Selection.getSelection()
                make_region.create(selection[-1])

        except Exception:
            alignments = get_alignments.get()
            panel = task_set_parent.TaskSetParent(alignments, make_region)
            FreeCADGui.Control.showDialog(panel)

FreeCADGui.addCommand('Create Region', CreateRegion())
