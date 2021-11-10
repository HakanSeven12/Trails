# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 Joel Graff <monograff76@gmail.com>                 *
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

"""Key maps for LandXML elements and the internal dictionary keys"""

from ..utils.const import Const


class KeyMaps(Const):
    """
    LandXML tag to local dictionary key mappings
    """

    #lists of tags for different units of measurements / geometry types
    XML_TAGS = {
        'length':
            ['radius', 'radiusStart', 'radiusEnd', 'chord', 'external',
             'midOrd', 'tangent', 'length', 'tanShort', 'tanLong', 'totalX',
             'totalY'
            ],

        'angle':
            ['delta', 'dir', 'dirStart', 'dirEnd', 'theta'],

        'coordinate':
            ['Start', 'End', 'Center', 'PI']
    }

    #lists of tags for different Python data types.
    #These are the datatypes that they represent in XML
    #(e.g. 'rot' = 'ccw' / 'cw' in XML, but -1.0 / 1.0 in dictionary)
    XML_TYPES = {
        'float':
            ['chord', 'constant', 'delta', 'dir', 'dirEnd', 'dirStart',
             'external', 'length', 'midOrd', 'radius', 'radiusEnd',
             'radiusStart', 'staBack', 'staIncrement', 'staInternal',
             'staStart', 'tangent', 'staAhead', 'staBack'],

        'string':
            ['crvType', 'desc', 'name', 'note', 'manufacturer',
             'manufacturerURL', 'oID', 'rot', 'spiType', 'state', 'timeStamp',
             'version']
    }

    #map of LandXML tags to internal Python dictionary to provide more
    #meaningful internal names.
    XML_MAP = {
        'chord': 'Chord', 'constant': 'Constant', 'crvType': 'CurveType',
        'delta': 'Delta', 'desc': 'Description', 'dir': 'BearingIn',
        'dirEnd': 'BearingOut', 'dirStart': 'BearingIn',
        'external': 'External',
        'length': 'Length',
        'midOrd': 'MiddleOrdinate',
        'name': 'ID', 'note': 'Note',
        'oID': 'ObjectID',
        'radius': 'Radius', 'radiusStart': 'StartRadius',
        'radiusEnd': 'EndRadius', 'rot': 'Direction',
        'spiType': 'SpiralType', 'staAhead': 'Ahead', 'staBack': 'Back',
        'staIncrement': 'Direction', 'staInternal': 'Position',
        'staStart': 'StartStation', 'staEnd': 'EndStation', 'state': 'Status',
        'tangent': 'Tangent', 'tanLong': 'TanLong', 'tanShort': 'TanShort',
        'theta': 'Theta', 'totalX': 'TotalX', 'totalY': 'TotalY',
        'version': 'Version'
    }

    #attributes for each LandXML Tag.
    #Attribute names are divided into two lists.
    #The first list is required attributes, the second is optional
    #Used for validating imported data sets
    XML_ATTRIBS = {
        'Project': [
            ['name'],
            ['desc', 'state']
        ],
        'Application': [
            ['name'],
            ['desc', 'manufacturer', 'version', 'manufacturerURL', 'timeStamp']
        ],
        'Surfaces': [
            [],
            ['desc', 'name', 'state']
        ],
        'Surface': [
            ['name'],
            ['desc', 'oID', 'state']
        ],
        'Definition': [
            ['surfType'],
            ['area2DSurf', 'area3DSurf', 'elevMax', 'elevMin']
        ],
        'Pnts': [
            [],
            []
        ],
        'P': [
            ['id'],
            []
        ],
        'Faces': [
            [],
            ['desc', 'name', 'state']
        ],
        'F': [
            [],
            ['i', 'n', 'b']
        ],
        'Alignments': [
            [],
            ['desc', 'name', 'state']
        ],
        'Alignment': [
            ['name', 'length', 'staStart'],
            ['desc', 'oID', 'state']
        ],
        'CoordGeom': [
            [],
            ['desc', 'name', 'state', 'oID']
        ],
        'StaEquation': [
            ['staAhead', 'staInternal'],
            ['desc', 'staBack', 'staIncrement']
        ],
        'Curve': [
            ['rot'],
            ['chord', 'crvType', 'delta', 'desc', 'dirEnd', 'dirStart',
             'external', 'length', 'midOrd', 'name', 'radius', 'staStart',
             'state', 'tangent', 'oID', 'note']
        ],
        'Line': [
            [],
            ['desc', 'dir', 'length', 'name', 'staStart', 'state', 'oID',
             'note']
        ],
        'Spiral': [
            ['length', 'radiusEnd', 'radiusStart', 'rot', 'spiType'],
            ['chord', 'constant', 'desc', 'dirEnd', 'dirStart', 'external',
             'length', 'midOrd', 'name', 'note', 'oID', 'staStart', 'state',
             'tanLong', 'tanShort', 'theta', 'totalX', 'totalY']
        ]
    }
