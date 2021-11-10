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

"""Provides functions to create Terrain objects."""

import FreeCAD

from ..get import get_terrains, get_georigin
from ..objects.terrain import Terrain
from ..viewproviders.view_terrain import ViewProviderTerrain

def create(points=[], label="Terrain"):
    """
    Class construction method
    label - Optional. Name of new object.
    """
    get_georigin.get()
    terrains = get_terrains.get()
    obj=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Terrain")

    Terrain(obj)
    ViewProviderTerrain(obj.ViewObject)

    obj.Label = label
    terrains.addObject(obj)
    obj.Vectors = points

    return obj