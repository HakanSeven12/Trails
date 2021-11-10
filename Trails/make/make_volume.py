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

"""Provides functions to create Volume objects."""

import FreeCAD

from ..objects.volume import Volume
from ..viewproviders.view_volume import ViewProviderVolume

def create(volumes, sections, name='Volume'):
    obj=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Volume")
    volumes.addObject(obj)

    Volume(obj)
    ViewProviderVolume(obj.ViewObject)

    obj.Label = name
    obj.TopSections = sections[0]
    obj.BottomSections = sections[1]
    FreeCAD.ActiveDocument.recompute()

    return objimpo