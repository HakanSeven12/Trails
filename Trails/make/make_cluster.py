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

"""Provides functions to create Cluster objects."""

import FreeCAD

from ..get import get_georigin, get_clusters
from ..objects.cluster import Cluster
from ..viewproviders.view_cluster import ViewProviderCluster

def main_cluster():
    """
    Find the main Cluster object
    """
    # Return an existing instance of the same name, if found.
    obj = FreeCAD.ActiveDocument.getObject('Cluster')

    if obj:
        return obj

    obj = create(name="Main")

    return obj

def create(points=[], name='Cluster'):
    get_georigin.get()
    clusters = get_clusters.get()

    obj=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Cluster")
    Cluster(obj)
    ViewProviderCluster(obj.ViewObject)

    obj.Label = name
    obj.Vectors = points
    clusters.addObject(obj)

    FreeCAD.ActiveDocument.recompute()

    return obj