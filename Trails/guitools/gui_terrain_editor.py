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

"""Provides GUI tools to edit Terrain objects."""

import FreeCAD, FreeCADGui
from pivy import coin

from trails_variables import icons_path


class AddPoint:
    """
    Command to add a point to Terrain.
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return {
            'Pixmap': icons_path + '/AddTriangle.svg',
            'MenuText': "Add Point",
            'ToolTip': "Add a point to selected Terrain."
            }

    def IsActive(self):
        """
        Define tool button activation situation
        """
        # Check for document
        if FreeCAD.ActiveDocument:
            # Check for selected object
            selection = FreeCADGui.Selection.getSelection()
            if selection:
                if selection[-1].Proxy.Type == 'Trails::Terrain':
                    return True
        return False

    def Activated(self):
        """
        Command activation method
        """
        # Create an event callback for add_point() function
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.event_callback = self.view.addEventCallbackPivy(
            coin.SoButtonEvent.getClassTypeId(), self.add_point)

    def add_point(self, cb):
        """
        Take two triangle by mouse clicks and swap edge between them
        """
        # Get event
        event = cb.getEvent()

        # If mouse right button pressed finish swap edge operation
        if event.getTypeId().isDerivedFrom(coin.SoKeyboardEvent.getClassTypeId()):
            if event.getKey() == coin.SoKeyboardEvent.ESCAPE \
                and event.getState() == coin.SoKeyboardEvent.DOWN:
                self.view.removeEventCallbackPivy(
                    coin.SoButtonEvent.getClassTypeId(), self.event_callback)

        # If mouse left button pressed get picked point
        elif event.getTypeId().isDerivedFrom(coin.SoMouseButtonEvent.getClassTypeId()):
            if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 \
                and event.getState() == coin.SoMouseButtonEvent.DOWN:
                picked_point = cb.getPickedPoint()

                # Get triangle index at picket point
                if picked_point:
                    detail = picked_point.getDetail()

                    if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                        face_detail = coin.cast(
                            detail, str(detail.getTypeId().getName()))
                        index = face_detail.getFaceIndex()

                        obj = self.view.getObjectInfo(self.view.getCursorPos())
                        curpos = FreeCAD.Vector(float(obj["x"]),float(obj["y"]),float(obj["z"]))           

                        terrain = FreeCADGui.Selection.getSelection()[-1]
                        copy_mesh = terrain.Mesh.copy()
                        copy_mesh.insertVertex(index, curpos)
                        terrain.Mesh = copy_mesh

FreeCADGui.addCommand('Add Point', AddPoint())


class AddTriangle:
    """
    Command to add a tirangle to Terrain.
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return {
            'Pixmap': icons_path + '/AddTriangle.svg',
            'MenuText': "Add Triangle",
            'ToolTip': "Add a triangle to selected Terrain."
            }

    def IsActive(self):
        """
        Define tool button activation situation
        """
        # Check for document
        if FreeCAD.ActiveDocument:
            # Check for selected object
            selection = FreeCADGui.Selection.getSelection()
            if selection:
                if selection[-1].Proxy.Type == 'Trails::Terrain':
                    return True
        return False

    def Activated(self):
        """
        Command activation method
        """
        # Call for Mesh.Addfacet function
        FreeCADGui.runCommand("Mesh_AddFacet")

FreeCADGui.addCommand('Add Triangle', AddTriangle())


class DeleteTriangle:
    """
    Command to delete a tirangle from Terrain.
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return {
            'Pixmap': icons_path + '/DeleteTriangle.svg',
            'MenuText': "Delete Triangle",
            'ToolTip': "Delete triangles from selected Terrain."
              }

    def IsActive(self):
        """
        Define tool button activation situation
        """
        # Check for document
        if FreeCAD.ActiveDocument:
            # Check for selected object
            selection = FreeCADGui.Selection.getSelection()
            if selection:
                if selection[-1].Proxy.Type == 'Trails::Terrain':
                    return True
        return False

    def Activated(self):
        """
        Command activation method
        """
        # Create an event callback for delete() function
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.event_callback = self.view.addEventCallbackPivy(
            coin.SoButtonEvent.getClassTypeId(), self.delete)
        self.indexes = []

    def delete(self, cb):
        """
        Take two triangle by mouse clicks and swap edge between them
        """
        # Get event
        event = cb.getEvent()

        # If mouse right button pressed finish swap edge operation
        if event.getTypeId().isDerivedFrom(coin.SoKeyboardEvent.getClassTypeId()):
            if event.getKey() == coin.SoKeyboardEvent.ESCAPE \
                and event.getState() == coin.SoKeyboardEvent.DOWN:
                self.view.removeEventCallbackPivy(
                    coin.SoButtonEvent.getClassTypeId(), self.event_callback)

        # If mouse left button pressed get picked point
        elif event.getTypeId().isDerivedFrom(coin.SoMouseButtonEvent.getClassTypeId()):
            if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 \
                and event.getState() == coin.SoMouseButtonEvent.DOWN:
                picked_point = cb.getPickedPoint()

                # Get triangle index at picket point
                if picked_point:
                    detail = picked_point.getDetail()

                    if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                        face_detail = coin.cast(
                            detail, str(detail.getTypeId().getName()))
                        index = face_detail.getFaceIndex()
                        self.indexes.append(index)

        # If mouse left button pressed get picked point
        if event.getTypeId().isDerivedFrom(coin.SoKeyboardEvent.getClassTypeId()):
            if event.getKey() == coin.SoKeyboardEvent.R \
                and event.getState() == coin.SoKeyboardEvent.DOWN:

                terrain = FreeCADGui.Selection.getSelection()[-1]
                copy_mesh = terrain.Mesh.copy()
                copy_mesh.removeFacets(self.indexes)
                self.indexes.clear()
                terrain.Mesh = copy_mesh

FreeCADGui.addCommand('Delete Triangle', DeleteTriangle())


class SwapEdge:
    """
    Command to swap an edge between two triangles
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return {
            'Pixmap': icons_path + '/SwapEdge.svg',
            'MenuText': "Swap Edge",
            'ToolTip': "Swap Edge of selected Terrain."
            }

    def IsActive(self):
        """
        Define tool button activation situation
        """
        # Check for document
        if FreeCAD.ActiveDocument:
            # Check for selected object
            selection = FreeCADGui.Selection.getSelection()
            if selection:
                if selection[-1].Proxy.Type == 'Trails::Terrain':
                    return True
        return False

    def Activated(self):
        """
        Command activation method
        """
        # Create an event callback for SwapEdge() function
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.face_indexes = []
        self.MC = FreeCADGui.ActiveDocument.ActiveView.addEventCallbackPivy(
            coin.SoButtonEvent.getClassTypeId(), self.SwapEdge)

    def SwapEdge(self, cb):
        """
        Take two triangle by mouse clicks and swap edge between them
        """
        # Get event
        event = cb.getEvent()

        # If mouse right button pressed finish swap edge operation
        if event.getTypeId().isDerivedFrom(coin.SoKeyboardEvent.getClassTypeId()):
            if event.getKey() == coin.SoKeyboardEvent.ESCAPE \
                and event.getState() == coin.SoKeyboardEvent.DOWN:
                self.view.removeEventCallbackPivy(
                    coin.SoButtonEvent.getClassTypeId(), self.MC)

        # If mouse left button pressed get picked point
        elif event.getTypeId().isDerivedFrom(coin.SoMouseButtonEvent.getClassTypeId()):
            if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 \
                and event.getState() == coin.SoMouseButtonEvent.DOWN:
                picked_point = cb.getPickedPoint()

                # Get triangle index at picket point
                if picked_point is not None:
                    detail = picked_point.getDetail()

                    if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                        face_detail = coin.cast(
                            detail, str(detail.getTypeId().getName()))
                        index = face_detail.getFaceIndex()
                        self.face_indexes.append(index)

                        # try to swap edge between picked triangle
                        if len(self.face_indexes) == 2:
                            terrain = FreeCADGui.Selection.getSelection()[-1]
                            copy_mesh = terrain.Mesh.copy()

                            try:
                                copy_mesh.swapEdge(
                                    self.face_indexes[0], self.face_indexes[1])

                            except Exception:
                                print("The edge between these triangles cannot be swappable")

                            terrain.Mesh = copy_mesh
                            self.face_indexes.clear()
                            FreeCAD.ActiveDocument.recompute()

FreeCADGui.addCommand('Swap Edge', SwapEdge())


class SmoothTerrain:
    """
    Command to smooth Terrain.
    """

    def __init__(self):
        """
        Constructor
        """

        # Set icon,  menu text and tooltip
        self.resources = {
            'Pixmap': icons_path + '/SmoothSurface.svg',
            'MenuText': "Smooth Terrain",
            'ToolTip': "Smooth selected Terrain."
            }

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return self.resources

    def IsActive(self):
        """
        Define tool button activation situation
        """
        # Check for document
        if FreeCAD.ActiveDocument:
            # Check for selected object
            selection = FreeCADGui.Selection.getSelection()
            if selection:
                if selection[-1].Proxy.Type == 'Trails::Terrain':
                    return True
        return False

    @staticmethod
    def Activated():
        """
        Command activation method
        """
        # Get selected terrain and smooth it
        terrain = FreeCADGui.Selection.getSelection()[0]
        terrain.Mesh.smooth()

FreeCADGui.addCommand('Smooth Terrain', SmoothTerrain())
