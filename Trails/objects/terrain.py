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

"""Provides the object code for Terrain objects."""

import FreeCAD
import Mesh, Part

from trails_variables import icons_path
from ..functions.terrain_functions import DataFunctions
from ..get import get_georigin


class Terrain(DataFunctions):
    """
    This class is about Terrain Object data features.
    """

    def __init__(self, obj):
        '''
        Set data properties.
        '''
        self.Type = 'Trails::Terrain'

        obj.addProperty(
            'App::PropertyPlacement', "Placement", "Base",
            "Placement").Placement = FreeCAD.Placement()

        # Triangulation properties.
        obj.addProperty(
            'App::PropertyLinkList', "Clusters", "Triangulation",
            "List of Point Groups").Clusters = []

        obj.addProperty(
            "App::PropertyVectorList", "Vectors", "Triangulation",
            "List of Terrain points").Vectors = []

        obj.addProperty(
            "App::PropertyIntegerList", "Delaunay", "Triangulation",
            "Index of Delaunay vertices", 4).Delaunay = []

        obj.addProperty(
            "Mesh::PropertyMeshKernel", "Mesh", "Triangulation",
            "Mesh object of triangulation").Mesh = Mesh.Mesh()

        obj.addProperty(
            "App::PropertyLength", "MaxLength", "Triangulation",
            "Maximum length of triangle edge").MaxLength = 500000

        obj.addProperty(
            "App::PropertyAngle","MaxAngle","Triangulation",
            "Maximum angle of triangle edge").MaxAngle = 180

        obj.addProperty("Part::PropertyPartShape", "BoundaryShapes", "Triangulation",
            "Boundary Shapes").BoundaryShapes = Part.Shape()

        # Analysis properties.
        obj.addProperty(
            "App::PropertyEnumeration", "AnalysisType", "Analysis",
            "Set analysis type").AnalysisType = ["Default", "Elevation", "Slope", "Direction"]

        obj.addProperty(
            "App::PropertyInteger", "Ranges", "Analysis",
            "Ranges").Ranges = 5

        # Contour properties.
        obj.addProperty("Part::PropertyPartShape", "ContourShapes", "Contour",
            "Contour Shapes").ContourShapes = Part.Shape()

        obj.addProperty(
            "App::PropertyLength", "MajorInterval", "Contour",
            "Major contour interval").MajorInterval = 5000

        obj.addProperty(
            "App::PropertyLength", "MinorInterval", "Contour",
            "Minor contour interval").MinorInterval = 1000

        obj.Proxy = self

    def onChanged(self, obj, prop):
        '''
        Do something when a data property has changed.
        '''
        if prop == "Placement":
            placement = obj.getPropertyByName(prop)
            copy_mesh = obj.Mesh.copy()
            copy_mesh.Placement = placement
            obj.Mesh = copy_mesh

        if prop =="Clusters":
            pgs = obj.getPropertyByName(prop)
            points = []
            for pg in pgs:
                points.extend(pg.Vectors)

            obj.Vectors = points

        if prop =="Vectors":
            vectors = obj.getPropertyByName(prop)
            if vectors:
                base = get_georigin.get(vectors[0]).Origin

                if len(vectors) > 2:
                    pts = []
                    for i in vectors:
                        pts.append(i.sub(base))

                    obj.Delaunay = self.triangulate(vectors)
                else:
                    obj.Mesh = Mesh.Mesh()

        if prop == "Delaunay" or prop == "MaxLength" or prop == "MaxAngle":
            delaunay = obj.getPropertyByName("Delaunay")
            vectors = obj.getPropertyByName("Vectors")
            lmax = obj.getPropertyByName("MaxLength")
            amax = obj.getPropertyByName("MaxAngle")
            base = get_georigin.get().Origin

            pts = []
            for i in vectors:
                pts.append(i.sub(base))

            if delaunay:
                obj.Mesh = self.test_delaunay(
                    pts, delaunay, lmax, amax)

        if prop == "MinorInterval":
            min_int = obj.getPropertyByName(prop)
            obj.MajorInterval = min_int*5

    def execute(self, obj):
        '''
        Do something when doing a recomputation. 
        '''
        major = obj.MajorInterval
        minor = obj.MinorInterval

        obj.ContourShapes = self.get_contours(
            obj.Mesh, major.Value/1000, minor.Value/1000)

        obj.BoundaryShapes = self.get_boundary(obj.Mesh)
