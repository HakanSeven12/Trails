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

"""Provides the viewprovider code for Alignment objects."""

import FreeCAD
from pivy import coin
from copy import deepcopy
from math import pi

from libs import icons_path
from ..get import get_georigin
from ..functions import alignment_functions


class ViewProviderAlignment(alignment_functions.ViewFunctions):
    """
    This class is about Alignment Object view features.
    """

    def __init__(self, vobj):
        '''
        Set view properties.
        '''
        vobj.addProperty(
            "App::PropertyBool", "Labels", "Base",
            "Show/hide labels").Labels = False

        vobj.Proxy = self

    def attach(self, vobj):
        '''
        Create Object visuals in 3D view.
        '''
        self.Object = vobj.Object

        # Line style.
        line_style = coin.SoDrawStyle()
        line_style.style = coin.SoDrawStyle.LINES
        line_style.lineWidth = 2

        # Line geometry keepers.
        line_color = coin.SoBaseColor()
        line_color.rgb = (1.0, 0.0, 0.0)
        self.lines = coin.SoSeparator()
        self.lines.addChild(line_style)
        self.lines.addChild(line_color)

        # Curve geometry keepers.
        curve_color = coin.SoBaseColor()
        curve_color.rgb = (0.0, 0.5, 0.0)
        self.curves = coin.SoSeparator()
        self.curves.addChild(line_style)
        self.curves.addChild(curve_color)

        # Spiral geometry keepers.
        spiral_color = coin.SoBaseColor()
        spiral_color.rgb = (0.0, 0.33, 1.0)
        self.spirals = coin.SoSeparator()
        self.spirals.addChild(line_style)
        self.spirals.addChild(spiral_color)

        # Labels root.
        ticks = coin.SoSeparator()
        self.tick_coords = coin.SoGeoCoordinate()
        self.tick_lines = coin.SoLineSet()
        ticks.addChild(self.tick_coords)
        ticks.addChild(self.tick_lines)
        self.labels = coin.SoSeparator()

        # Alignment root.
        lines_root = coin.SoSeparator()
        lines_root.addChild(self.lines)
        lines_root.addChild(self.curves)
        lines_root.addChild(self.spirals)
        lines_root.addChild(ticks)
        lines_root.addChild(self.labels)
        vobj.addDisplayMode(lines_root,"Wireframe")

    def onChanged(self, vobj, prop):
        '''
        Update Object visuals when a view property changed.
        '''
        if prop == "Labels":

            self.labels.removeAllChildren()
            labels = vobj.getPropertyByName(prop)

            # Set System.
            origin = get_georigin.get()
            geo_system = ["UTM", origin.UtmZone, "FLAT"]
            self.tick_coords.geoSystem.setValues(geo_system)

            if labels:
                points = []
                line_vert = []
                stations = self.get_stations(vobj.Object)

                for label, tick in stations.items():
                    font = coin.SoFont()
                    font.size = 3000
                    sta_label = coin.SoSeparator()
                    location = coin.SoTransform()
                    text = coin.SoAsciiText()

                    text.string.setValues([str(label)])
                    start = deepcopy(tick[0]).sub(origin.Origin)
                    end = deepcopy(tick[-1]).sub(origin.Origin)

                    if start.y>end.y:
                        angle = start.sub(end).getAngle(FreeCAD.Vector(1,0,0))-pi
                    else:
                        angle = end.sub(start).getAngle(FreeCAD.Vector(1,0,0))

                    location.translation = end
                    location.rotation.setValue(coin.SbVec3f(0, 0, 1), angle)

                    sta_label.addChild(font)
                    sta_label.addChild(location)
                    sta_label.addChild(text)
                    self.labels.addChild(sta_label)

                    points.extend(tick)
                    line_vert.append(len(tick))

                self.tick_coords.point.values = points
                self.tick_lines.numVertices.values = line_vert

    def updateData(self, obj, prop):
        '''
        Update Object visuals when a data property changed.
        '''
        if prop == "Shape":
            shape = obj.getPropertyByName(prop)
            if not shape.SubShapes: return

            # Set System.
            origin = get_georigin.get()
            geo_system = ["UTM", origin.UtmZone, "FLAT"]

            copy_shape = shape.copy()
            copy_shape.Placement.move(origin.Origin)

            lines = copy_shape.SubShapes[0]
            for wire in lines.Wires:
                points = []
                for vertex in wire.OrderedVertexes:
                    points.append(vertex.Point)

                line = coin.SoType.fromName('SoFCSelection').createInstance()
                line.style = 'EMISSIVE_DIFFUSE'

                line_coords = coin.SoGeoCoordinate()
                line_coords.geoSystem.setValues(geo_system)
                line_coords.point.values = points
                line_set = coin.SoLineSet()

                line.addChild(line_coords)
                line.addChild(line_set)
                self.lines.addChild(line)

                del points

            curves = copy_shape.SubShapes[1]
            for wire in curves.Wires:
                points = []
                for vertex in wire.OrderedVertexes:
                    points.append(vertex.Point)

                curve = coin.SoType.fromName('SoFCSelection').createInstance()
                curve.style = 'EMISSIVE_DIFFUSE'

                curve_coords = coin.SoGeoCoordinate()
                curve_coords.geoSystem.setValues(geo_system)
                curve_coords.point.values = points
                curve_set = coin.SoLineSet()

                curve.addChild(curve_coords)
                curve.addChild(curve_set)
                self.curves.addChild(curve)

                del points

            spirals = copy_shape.SubShapes[2]
            for wire in spirals.Wires:
                points = []
                for vertex in wire.OrderedVertexes:
                    points.append(vertex.Point)

                spiral = coin.SoType.fromName('SoFCSelection').createInstance()
                spiral.style = 'EMISSIVE_DIFFUSE'

                spiral_coords = coin.SoGeoCoordinate()
                spiral_coords.geoSystem.setValues(geo_system)
                spiral_coords.point.values = points
                spiral_set = coin.SoLineSet()

                spiral.addChild(spiral_coords)
                spiral.addChild(spiral_set)
                self.spirals.addChild(spiral)

                del points
            del copy_shape

    def getDisplayMode(self, obj):
        '''
        Return a list of display modes.
        '''
        modes = ["Wireframe"]
        return modes

    def getDefaultDisplayMode(self):
        '''
        Return the name of the default display mode.
        '''
        return "Wireframe"

    def setDisplayMode(self, mode):
        '''
        Map the display mode defined in attach with 
        those defined in getDisplayModes.
        '''
        return "Wireframe"

    def getIcon(self):
        '''
        Return object treeview icon.
        '''
        return icons_path + '/Alignment.svg'

    def claimChildren(self):
        """
        Provides object grouping
        """
        return self.Object.Group

    def setEdit(self, vobj, mode=0):
        """
        Enable edit
        """
        return True

    def unsetEdit(self, vobj, mode=0):
        """
        Disable edit
        """
        return False

    def doubleClicked(self, vobj):
        """
        Detect double click
        """
        pass

    def setupContextMenu(self, obj, menu):
        """
        Context menu construction
        """
        pass

    def edit(self):
        """
        Edit callback
        """
        pass
    def __getstate__(self):
        """
        Save variables to file.
        """
        return None

    def __setstate__(self, state):
        """
        Get variables from file.
        """
        return None
