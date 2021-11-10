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

"""Provides the object code for Alignment objects."""

import Part
from FreeCAD import Vector
from math import inf, pi

from ..utils import units
from ..get import get_georigin
from ..functions import alignment_functions


class Alignment(alignment_functions.DataFunctions):
    """
    This class is about Alignment Object data features.
    """

    def __init__(self, obj, label=""):
        """
        Set data properties.
        """
        self.Type = 'Trails::Alignment'

        # Metadata properties.
        obj.addProperty(
            'App::PropertyString', "ID", "Base",
            "ID of alignment").ID = label

        obj.addProperty(
            'App::PropertyString', "oID", "Base",
            "Object ID").oID = ""

        obj.addProperty(
            'App::PropertyString', "Description", "Base",
            "Alignment description").Description = ""

        obj.addProperty(
            'App::PropertyLength', "Length", "Base",
            "Alignment length", 1).Length = 0.0

        obj.addProperty(
            'App::PropertyLength', "StartStation", "Base",
            "Starting station of the alignment").StartStation = 0.0

        obj.addProperty(
            'App::PropertyEnumeration', "Status", "Base",
            'Alignment status').Status = ['existing', 'proposed', 'abandoned', 'destroyed']

        obj.addProperty(
            'App::PropertyVector', "Datum", "Base",
            "Datum value as Northing / Easting").Datum = Vector()

        obj.addProperty(
            'App::PropertyFloatList', "Hashes", "Base",
            "Coordinate hashes").Hashes = []

        # Geometry properties.
        subdivision_desc = """Method of Curve Subdivision\n\n
            Tolerance - ensure error between segments and curve is (n)\n
            Interval - Subdivide curve into segments of fixed length\n
            Segment - Subdivide curve into equal-length segments"""

        obj.addProperty(
            'App::PropertyEnumeration', "Method", "Segment", subdivision_desc
        ).Method = ['Tolerance', 'Interval', 'Segment']

        obj.addProperty(
            'App::PropertyFloat', "SegmentFactor", "Segment",
            "Set the curve segments to control accuracy").SegmentFactor = int(1000.0 / units.scale_factor()) / 100.0

        obj.addProperty(
            'App::PropertyString', 'ModelKeeper', 'Base', "ModelKeeper"
        ).ModelKeeper = ''

        obj.addProperty(
            "Part::PropertyPartShape", "Shape", "Base",
            "Alignment Shape").Shape = Part.Shape()

        obj.addProperty(
            "App::PropertyVectorList", "PIs", "Base",
            "Discretization of Points of Intersection (PIs) as a list of vectors").PIs = []

        obj.addProperty(
            "App::PropertyLink", "ParentAlignment", "Base",
            "Links to parent alignment object").ParentAlignment = None

        obj.Proxy = self
        self.init_class_members(obj)

    def init_class_members(self, obj):
        """
        Separate function for initialization on creation / reload.
        """
        self.Object = obj

        self.meta = {}
        self.errors = []
        self.model = None
        self.hashes = None
        self.curve_edges = None

    def onDocumentRestored(self, obj):
        """
        Restore Object references on reload.
        """
        self.init_class_members(obj)
        self.set_geometry(eval(obj.ModelKeeper))

    def __getstate__(self):
        """
        Save variables to file.
        """
        return self.Type

    def __setstate__(self, state):
        """
        Get variables from file.
        """
        if state:
            self.Type = state

    def onChanged(self, obj, prop):
        '''
        Update Object when a property changed.
        '''
        if prop == "Method":

            _prop = obj.getPropertyByName(prop)

            if _prop == 'Interval':
                self.obj.SegmentFactor = int(3000.0 / units.scale_factor())

            elif _prop == 'Segment':
                self.obj.SegmentFactor = 200.0

            elif _prop == 'Tolerance':
                self.obj.SegmentFactor = \
                    int(1000.0 / units.scale_factor()) / 100.0

    def execute(self, obj):
        '''
        Update Object when doing a recomputation. 
        '''
        if hasattr(self.model, 'discretize_geometry'):
            curves, spirals, lines, points = self.model.discretize_geometry(
                [0.0], obj.Method, obj.SegmentFactor, types=True)

            origin = get_georigin.get(points[0])

            obj.Shape = self.get_shape(lines, curves, spirals, origin.Origin)