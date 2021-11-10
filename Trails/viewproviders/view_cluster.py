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

"""Provides the viewprovider code for Cluster objects."""

import FreeCAD
from pivy import coin
import random, copy

from libs import icons_path, marker_dict
from ..get import get_georigin


class ViewProviderCluster:
    """
    This class is about Cluster Object view features.
    """

    def __init__(self, vobj):
        '''
        Set view properties.
        '''
        (r, g, b) = (random.random(), random.random(), random.random())

        vobj.addProperty(
            "App::PropertyBool", "Labels", "Base",
            "Show/hide labels").Labels = False

        vobj.addProperty(
            "App::PropertyBool", "Name", "Labels",
            "Show point name labels").Name = False

        vobj.addProperty(
            "App::PropertyBool", "NortingEasting", "Labels",
            "Show norting easting labels").NortingEasting = False

        vobj.addProperty(
            "App::PropertyBool", "Elevation", "Labels",
            "Show elevation labels").Elevation = False

        vobj.addProperty(
            "App::PropertyBool", "Description", "Labels",
            "Show description labels").Description = False

        vobj.addProperty(
            "App::PropertyColor", "PointColor", "Point Style",
            "Color of the point group").PointColor = (r, g, b)

        vobj.addProperty(
            "App::PropertyFloatConstraint", "PointSize", "Point Style",
            "Size of the point group").PointSize = (3.0, 1.0, 20.0, 1.0)

        vobj.Proxy = self

    def attach(self, vobj):
        '''
        Create Object visuals in 3D view.
        '''
        # GeoCoord Node.
        self.geo_coords = coin.SoGeoCoordinate()

        # Point group features.
        points = coin.SoPointSet()
        self.markers = coin.SoMarkerSet()
        self.color_mat = coin.SoMaterial()
        self.point_normal = coin.SoNormal()
        self.point_style = coin.SoDrawStyle()
        self.point_style.style = coin.SoDrawStyle.POINTS

        # Highlight for selection.
        highlight = coin.SoType.fromName('SoFCSelection').createInstance()
        highlight.style = 'EMISSIVE_DIFFUSE'
        highlight.addChild(self.geo_coords)
        highlight.addChild(points)
        highlight.addChild(self.markers)

        # Point labels features.
        color =coin.SoBaseColor()
        self.point_labels = coin.SoSeparator()
        self.point_labels.addChild(color)

        # Point group root.
        point_root = coin.SoSeparator()
        point_root.addChild(self.point_labels)
        point_root.addChild(self.point_style)
        point_root.addChild(self.point_normal)
        point_root.addChild(self.color_mat)
        point_root.addChild(highlight)
        vobj.addDisplayMode(point_root,"Point")

        # Take features from properties.
        if vobj.Object.Points: self.onChanged(vobj,"Elevation")
        self.onChanged(vobj,"PointSize")
        self.onChanged(vobj,"PointColor")

    def onChanged(self, vobj, prop):
        '''
        Update Object visuals when a view property changed.
        '''
        labels = vobj.getPropertyByName("Labels")
        self.point_labels.removeAllChildren()
        if labels:
            if prop == "Labels" or prop == "Name" or prop == "NortingEasting"\
                or prop == "Elevation" or prop == "Description":
                origin = get_georigin.get()

                show_name = vobj.getPropertyByName("Name")
                show_ne = vobj.getPropertyByName("NortingEasting")
                show_z = vobj.getPropertyByName("Elevation")
                show_des = vobj.getPropertyByName("Description")

                for vector in vobj.Object.Points:
                    font = coin.SoFont()
                    font.size = 1000
                    point_label = coin.SoSeparator()
                    location = coin.SoTranslation()
                    text = coin.SoAsciiText()
                    index = vobj.Object.Points.index(vector)
                    labels =[]

                    if show_name: labels.append(vobj.Object.PointNames[index])
                    if show_ne: labels.extend([str(round(vector.x/1000, 3)), str(round(vector.y/1000,3))])
                    if show_z: labels.append(str(round(vector.z/1000,3)))
                    if show_des and vobj.Object.Descriptions: labels.append(vobj.Object.Descriptions[index])

                    location.translation = vector.sub(FreeCAD.Vector(origin.Origin))
                    text.string.setValues(labels)
                    point_label.addChild(font)
                    point_label.addChild(location)
                    point_label.addChild(text)
                    self.point_labels.addChild(point_label)

        if prop == "PointSize":
            size = vobj.getPropertyByName(prop)
            self.point_style.pointSize = size

        if prop == "PointColor":
            color = vobj.getPropertyByName(prop)
            self.color_mat.diffuseColor = (color[0],color[1],color[2])

    def updateData(self, obj, prop):
        '''
        Update Object visuals when a data property changed.
        '''
        if prop == "Points":
            points = obj.getPropertyByName(prop)
            if points.Points:
                origin = get_georigin.get()

                pts = []
                for i in points.Points:
                    point = copy.deepcopy(i)
                    pts.append(point.add(origin.Origin))

                geo_system = ["UTM", origin.UtmZone, "FLAT"]
                self.geo_coords.geoSystem.setValues(geo_system)
                self.geo_coords.point.values = pts

        if prop == "Marker":
            marker = obj.getPropertyByName(prop)
            self.markers.markerIndex = marker_dict[marker]

    def getDisplayModes(self, vobj):
        '''
        Return a list of display modes.
        '''
        modes=[]
        modes.append("Point")

        return modes

    def getDefaultDisplayMode(self):
        '''
        Return the name of the default display mode.
        '''
        return "Point"

    def setDisplayMode(self,mode):
        '''
        Map the display mode defined in attach with 
        those defined in getDisplayModes.
        '''
        return mode

    def getIcon(self):
        '''
        Return object treeview icon.
        '''
        return icons_path + '/PointGroup.svg'

    def __getstate__(self):
        """
        Save variables to file.
        """
        return None
 
    def __setstate__(self,state):
        """
        Get variables from file.
        """
        return None
