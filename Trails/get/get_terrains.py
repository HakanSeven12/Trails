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

"""Provides functions to get Terrain group."""

import FreeCAD

from trails_variables import icons_path
from ..objects.group import Group
from ..viewproviders.view_group import ViewProviderGroup

def get():
    """
    Find the existing Terrain group.
    """
    # Return an existing instance of the same name, if found.
    obj = FreeCAD.ActiveDocument.getObject('Terrains')

    if obj:
        return obj

    obj = create()

    return obj

def create():
    """
    Factory method for Terrain group.
    """
    obj = FreeCAD.ActiveDocument.addObject(
        "App::DocumentObjectGroupPython", 'Terrains')

    Group(obj)
    ViewProviderGroup(obj.ViewObject)

    obj.Label = "Terrains"
    obj.Proxy.Type = "Trails::Terrains"
    obj.ViewObject.Proxy.Icon = icons_path + '/Surface.svg'
    FreeCAD.ActiveDocument.recompute()

    return obj