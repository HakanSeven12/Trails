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

"""Provides the object code for Geo Origin objects."""

import FreeCAD, FreeCADGui

from pivy import coin
from libs import icons_path, zone_list


class GeoOrigin:
    """
    This class is about Point Group Object data features.
    """

    def __init__(self, obj):
        '''
        Set data properties.
        '''
        self.Type = 'Trails::GeoOrigin'

        obj.addProperty(
            "App::PropertyEnumeration", "UtmZone", "Base",
            "UTM zone").UtmZone = zone_list

        obj.addProperty(
            "App::PropertyVector", "Origin", "Base",
            "Origin point.").Origin = FreeCAD.Vector()

        obj.Proxy = self

        self.UtmZone = None
        self.Origin = None

    def onChanged(self, fp, prop):
        '''
        Do something when a data property has changed.
        '''
        # Set geo origin.
        node = self.get_geoorigin()

        if prop == "UtmZone":
            zone = fp.getPropertyByName("UtmZone")
            geo_system = ["UTM", zone, "FLAT"]
            node.geoSystem.setValues(geo_system)

        if prop == "Origin":
            origin = fp.getPropertyByName("Origin")
            node.geoCoords.setValue(origin.x, origin.y, 0.0)

    def execute(self, fp):
        '''
        Do something when doing a recomputation.
        '''
        return

    def __getstate__(self):
        """
        Save variables to file.
        """
        node = self.get_geoorigin()
        system = node.geoSystem.getValues()
        x,y,z = node.geoCoords.getValue().getValue()
        return system, [x, y, z]

    def __setstate__(self, state):
        """
        Get variables from file.
        """
        if state:
            system = state[0]
            origin = state[1]
            node = self.get_geoorigin()

            node.geoSystem.setValues(system)
            node.geoCoords.setValue(origin[0], origin[1], 0.0)

    def get_geoorigin(self):
        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        node = sg.getChild(0)

        if not isinstance(node, coin.SoGeoOrigin):
            node = coin.SoGeoOrigin()
            sg.insertChild(node,0)

        return node