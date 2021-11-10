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

"""Provides the object code for Cluster objects."""

import Points
import copy

from libs import marker_dict
from ..get import get_georigin


class Cluster:
    """
    This class is about Cluster Object data features.
    """

    def __init__(self, obj):
        '''
        Set data properties.
        '''

        self.Type = 'Trails::Cluster'

        obj.addProperty(
            "App::PropertyStringList", "PointNames", "Base",
            "List of group points").PointNames = []

        obj.addProperty(
            "App::PropertyVectorList", "Vectors", "Base",
            "List of group points").Vectors = []

        obj.addProperty(
            "App::PropertyStringList", "Descriptions", "Base",
            "List of group points").Descriptions = []

        obj.addProperty(
            "App::PropertyEnumeration", "Marker", "Base",
            "List of point markers").Marker = [*marker_dict]

        obj.addProperty(
            "Points::PropertyPointKernel", "Points", "Base",
            "Point Kernel").Points = Points.Points()

        obj.Proxy = self

    def onChanged(self, obj, prop):
        '''
        Do something when a data property has changed.
        '''
        if prop == "Vectors":
            vectors = obj.getPropertyByName(prop)
            if vectors:
                origin = get_georigin.get(vectors[0])

                points = []
                for i in vectors:
                    point = copy.deepcopy(i)
                    points.append(point.sub(origin.Origin))

                obj.Points = Points.Points(points)

    def execute(self, obj):
        '''
        Do something when doing a recomputation. 
        '''
        return