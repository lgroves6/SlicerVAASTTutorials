import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np 
#
# VIVECalibration
#

class VIVECalibration(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "VIVECalibration" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# VIVECalibrationWidget
#

class VIVECalibrationWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  def __init__(self, parent=None):
    ScriptedLoadableModuleWidget.__init__(self, parent)
    slicer.mymod = self
    self.connectorNode = None
    self.transformNode = None
    self.markupsNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode')
    self.collectionNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode')
    self.error = 0.0 
  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    l = slicer.modules.createmodels.logic()
    self.needleModel = l.CreateNeedle(150, 1, 2.5, False)
    
    # self.array1 = np.array([29, 24.37, 160.992])
    # self.array2 = np.array([28, 1.630, 69.785])
    # self.array3 = np.array([29,-7.321, 33.884])
    # self.array4 = np.array([-26, 24.129, 160.022])
    # self.array5 = np.array([-28, 11.065, 107.626])
    # self.array6 = np.array([-30.387, -7.394, 33.589])
    
    self.jigArray = np.array([[29, 24.37, 160.992],[28, 1.630, 69.785],[29,-7.321, 33.884],[-26, 24.129, 160.022],[-28, 11.065, 107.626],[-30.387, -7.394, 33.589]])
    self.collectedArray = np.array([[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]])
    self.points = vtk.vtkPoints()
    self.points.SetNumberOfPoints(6)
    self.points.SetPoint(0,self.jigArray[0])
    self.points.SetPoint(1,self.jigArray[1])
    self.points.SetPoint(2,self.jigArray[2])
    self.points.SetPoint(3,self.jigArray[3])
    self.points.SetPoint(4,self.jigArray[4])
    self.points.SetPoint(5,self.jigArray[5])

    self.collectedPoints = vtk.vtkPoints()
    self.collectedPoints.SetNumberOfPoints(6)
    self.DN = self.markupsNode.GetDisplayNode()
    self.DN.SetSelectedColor(0, 0, 1)
    self.DN.SetTextScale(0)
    self.markupsNode.AddFiducialFromArray(self.jigArray[0])
    self.markupsNode.AddFiducialFromArray(self.jigArray[1])
    self.markupsNode.AddFiducialFromArray(self.jigArray[2])
    self.markupsNode.AddFiducialFromArray(self.jigArray[3])
    self.markupsNode.AddFiducialFromArray(self.jigArray[4])
    self.markupsNode.AddFiducialFromArray(self.jigArray[5])

    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
    self.parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    self.parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(self.parametersCollapsibleButton)
    
    self.parametersFormLayout = qt.QFormLayout(self.parametersCollapsibleButton)
     
    self.connectButton = qt.QPushButton()
    self.connectButton.setDefault(False)
    self.connectButton.text = "Connect" 
    self.parametersFormLayout.addWidget(self.connectButton)
    
    self.TransformSelector = slicer.qMRMLNodeComboBox()
    self.TransformSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.TransformSelector.selectNodeUponCreation = True
    self.TransformSelector.addEnabled = False
    self.TransformSelector.removeEnabled = False
    self.TransformSelector.noneEnabled = True
    self.TransformSelector.showHidden = False
    self.TransformSelector.showChildNodeTypes = False
    self.TransformSelector.setMRMLScene( slicer.mrmlScene )
    self.TransformSelector.setToolTip( "Pick the transform representing the straw line." )
    self.parametersFormLayout.addRow("Tip to Probe: ", self.TransformSelector)
    
    self.collectButton = qt.QPushButton()
    self.collectButton.setDefault(False)
    self.collectButton.text = "Collect Fiducial" 
    self.parametersFormLayout.addWidget(self.collectButton)
    self.shortcut = qt.QShortcut(qt.QKeySequence('c'), slicer.util.mainWindow())
    self.deleteButton = qt.QPushButton()
    self.deleteButton.setDefault(False)
    self.deleteButton.text = "Delete Last Fiducial" 
    self.parametersFormLayout.addWidget(self.deleteButton)

    self.calculateButton = qt.QPushButton()
    self.calculateButton.setDefault(False)
    self.calculateButton.text = "Calculate Transformation Matrix" 
    self.parametersFormLayout.addWidget(self.calculateButton)

    self.transformTable = qt.QTableWidget() 
    self.transTableItem = qt.QTableWidgetItem()
    self.fidError = qt.QLabel()
    self.transformTable.setRowCount(4)
    self.transformTable.setColumnCount(4)
    self.transformTable.horizontalHeader().hide()
    self.transformTable.verticalHeader().hide()
    self.transformTable.setItem(0,0, qt.QTableWidgetItem("1"))
    self.transformTable.setItem(0,1, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(0,2, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(0,3, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(1,0, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(1,1, qt.QTableWidgetItem("1"))
    self.transformTable.setItem(1,2, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(1,3, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(2,0, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(2,1, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(2,2, qt.QTableWidgetItem("1"))
    self.transformTable.setItem(2,3, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(3,0, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(3,1, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(3,2, qt.QTableWidgetItem("0"))
    self.transformTable.setItem(3,3, qt.QTableWidgetItem("1"))
    self.transformTable.resizeColumnToContents(0)
    self.transformTable.resizeColumnToContents(1)
    self.transformTable.resizeColumnToContents(2)
    self.transformTable.resizeColumnToContents(3)
    self.transformTable.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.MinimumExpanding)
    # self.copyIcon =qt.QIcon(":Icons/Medium/SlicerEditCopy.png")
    # self.copyButton = qt.QPushButton()
    # self.copyButton.setIcon(self.copyIcon)
    # self.copyButton.toolTip = "Copy" 
    # self.copyButton.setMaximumWidth(64)
    # self.copyHbox = qt.QHBoxLayout()
    # self.copyHbox.addWidget(self.copyButton)
    self.parametersFormLayout.addRow(qt.QLabel("Transformation Matrix:"))
    self.parametersFormLayout.addRow(self.transformTable)
    self.copyButton = qt.QPushButton()
    self.copyButton.setDefault(False)
    self.copyButton.text = "Copy Transform" 
    self.parametersFormLayout.addWidget(self.copyButton)
    
    self.errorString = qt.QLabel()
    self.errorString.text = "RMSE: "+str(self.error)
    self.parametersFormLayout.addRow(self.errorString)

    self.connectButton.connect('clicked(bool)', self.onConnectButtonClicked)
    self.TransformSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onTransformChanged)
    self.collectButton.connect('clicked(bool)', self.onCollectButtonClicked)
    self.shortcut.connect('activated()', self.onCollectButtonClicked)
    self.deleteButton.connect('clicked(bool)', self.onDeleteButtonClicked)
    self.calculateButton.connect('clicked(bool)', self.onCalculateButtonClicked)
    self.copyButton.connect('clicked(bool)', self.onCopyButtonClicked)
    self.layout.addStretch(1)
    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
  def onConnectButtonClicked(self):
    if self.connectorNode is not None: 
      self.connectorNode = None
    else:
      self.connectorNode = slicer.vtkMRMLIGTLConnectorNode()
      slicer.mrmlScene.AddNode(self.connectorNode) 
      self.connectorNode.SetTypeClient('localhost', 18944)
      self.connectorNode.Start() 
      self.connectCheck = 0   

  def onTransformChanged(self):
    if self.transformNode is not None: 
      self.transformNode.SetAndObserveTransformNodeID(None) 
      self.transformNode = None 
    self.transformNode = self.TransformSelector.currentNode() 
    if self.transformNode is None:
      print('Please select a tip to probe transform')
    else:
      self.needleModel.SetAndObserveTransformNodeID(self.transformNode.GetID()) 
 
  def onCollectButtonClicked(self): 
    self.mat = vtk.vtkMatrix4x4()
    self.transformNode.GetMatrixTransformToWorld(self.mat)
    self.n = self.collectionNode.GetNumberOfFiducials()
    self.collectedArray[self.n] = [self.mat.GetElement(0,3),self.mat.GetElement(1,3),self.mat.GetElement(2,3)]
    self.collectionNode.AddFiducialFromArray(self.collectedArray[self.n])
    self.collectedPoints.SetPoint(self.n, self.collectedArray[self.n])
  def onDeleteButtonClicked(self):
    self.n = self.collectionNode.GetNumberOfMarkups()
    self.collectionNode.RemoveMarkup(self.n-1)

  def onCalculateButtonClicked(self):
    self.landmarkTransform = vtk.vtkLandmarkTransform()
    self.landmarkTransform.SetSourceLandmarks(self.collectedPoints)
    self.landmarkTransform.SetTargetLandmarks(self.points)
    self.landmarkTransform.SetModeToRigidBody()
    self.landmarkTransform.Update()
    self.outputMatrix = vtk.vtkMatrix4x4()
    self.landmarkTransform.GetMatrix(self.outputMatrix)
    self.transformTable.setItem(0,0, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(0,0))))
    self.transformTable.setItem(0,1, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(0,1))))
    self.transformTable.setItem(0,2, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(0,2))))
    self.transformTable.setItem(0,3, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(0,3))))
    self.transformTable.setItem(1,0, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(1,0))))
    self.transformTable.setItem(1,1, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(1,1))))
    self.transformTable.setItem(1,2, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(1,2))))
    self.transformTable.setItem(1,3, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(1,3))))
    self.transformTable.setItem(2,0, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(2,0))))
    self.transformTable.setItem(2,1, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(2,1))))
    self.transformTable.setItem(2,2, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(2,2))))
    self.transformTable.setItem(2,3, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(2,3))))
    self.transformTable.setItem(3,0, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(3,0))))
    self.transformTable.setItem(3,1, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(3,1))))
    self.transformTable.setItem(3,2, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(3,2))))
    self.transformTable.setItem(3,3, qt.QTableWidgetItem(str(self.outputMatrix.GetElement(3,3))))
    self.transformTable.resizeColumnToContents(0)
    self.transformTable.resizeColumnToContents(1)
    self.transformTable.resizeColumnToContents(2)
    self.transformTable.resizeColumnToContents(3)
    self.calNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'JigSensorToJig')
    self.calNode.SetMatrixTransformToParent(self.outputMatrix)
    self.collectionNode.SetAndObserveTransformNodeID(self.calNode.GetID())
    self.array = np.ones(4)
    self.transformedArray = np.array([[0, 0, 0],[0, 0, 0],[0, 0, 0],[ 0, 0,0],[0, 0,0],[0,0, 0]], np.float64())
    for i in range (0,6): 
      self.collectionNode.GetMarkupPointWorld(i,0,self.array)
      self.transformedArray[i] = self.array[0:3]
    self.error = np.linalg.norm(self.jigArray-self.transformedArray)
    self.errorString.text = "RMSE: "+str(self.error)
  def onCopyButtonClicked(self,numFidLabel):
    if self.numFidLabel >=1:
      self.outputTransform = '[' + str(self.outputMatrix.GetElement(0,0))+','+ str(self.outputMatrix.GetElement(0,1))+','+str(self.outputMatrix.GetElement(0,2))+','+str(self.outputMatrix.GetElement(0,3))+','+str(self.outputMatrix.GetElement(1,3))+';'+str(self.outputMatrix.GetElement(1,0))+','+str(self.outputMatrix.GetElement(1,1))+','+str(self.outputMatrix.GetElement(1,2))+','+str(self.outputMatrix.GetElement(1,3))+';'+str(self.outputMatrix.GetElement(2,0))+','+str(self.outputMatrix.GetElement(2,1))+','+str(self.outputMatrix.GetElement(2,2))+','+str(self.outputMatrix.GetElement(2,3))+']'
    else:
      self.outputTransform = 'Calibration Required' 
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    root.clipboard_clear() 
    root.clipboard_append(self.outputTransform)
    root.update()
    root.destroy()