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

"""Provides functions to create Geo Origin objects."""

import FreeCAD

from ..objects.georigin import GeoOrigin
from ..viewproviders.view_georigin import ViewProviderGeoOrigin

def get(origin=FreeCAD.Vector()):
    """
    Find the existing Point Groups object
    """
    # Return an existing instance of the same name, if found.
    obj = FreeCAD.ActiveDocument.getObject('GeoOrigin')

    if obj:
        if obj.Origin == FreeCAD.Vector():
            obj.Origin = origin
            obj.Origin.z = 0
        return obj

    obj = create(origin)
    return obj

def create(origin):
    obj=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "GeoOrigin")
    GeoOrigin(obj)
    ViewProviderGeoOrigin(obj.ViewObject)

    obj.UtmZone = "Z1"
    obj.Origin = origin

    FreeCAD.ActiveDocument.recompute()

    return obj