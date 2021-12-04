# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 Joel Graff <monograff76@gmail.com>                 *
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

"""Provides functions to create Alignment objects."""

import FreeCAD

from . import make_regions
from ..get import get_georigin, get_alignments
from ..objects.alignment import Alignment
from ..viewproviders.view_alignment import ViewProviderAlignment

def create(geometry, label="Alignment", zero_reference=False):
    """
    Class construction method
    """

    if not geometry:
        print('No curve geometry supplied')
        return

    get_georigin.get()
    group = get_alignments.get()
    obj=FreeCAD.ActiveDocument.addObject(
        "App::DocumentObjectGroupPython", "Alignment")

    Alignment(obj, label)
    ViewProviderAlignment(obj.ViewObject)

    # Set geometry.
    obj.ModelKeeper = str(geometry)
    obj.Proxy.set_geometry(geometry, zero_reference)

    regions = make_regions.create()
    obj.addObject(regions)

    obj.Label = label
    group.addObject(obj)
    FreeCAD.ActiveDocument.recompute()

    return obj
