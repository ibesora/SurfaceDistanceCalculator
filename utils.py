import math
from enum import Enum
from shapely.geometry import LineString

Quadrants = Enum('Quadrants', 'First Second Third Fourth')
CellEdges = Enum('CellEdges', 'Top Bottom Left Right Diagonal')

class Line:
  def __init__(self, start, end, name):
    self.vertices = [start, end]
    self.geom = LineString([start, end])
    self.name = name
  def __str__(self):
    return str((self.name, str(self.geom)))
  def getVertices(self):
    return self.vertices
  def getGeom(self):
    return self.geom
  def getName(self):
    return self.name
  def getStart(self):
    return self.geom.coords[0]
  def getEnd(self):
    return self.geom.coords[1]
  def length(self):
    return self.geom.length
  def intersection(self, lineToIntersect):
    return self.geom.intersection(lineToIntersect.geom)

class Hit:
  def __init__(self, point, line):
    self.geom = point
    self.line = line
  def __str__(self):
    return str((str(self.geom), str(self.line)))
  def getGeom(self):
    return self.geom
  def getLine(self):
    return self.line
  def getNormalizedDistanceOnLine(self):
    return Line(self.line.getStart(), self.geom, "Hit edge").length() / self.line.length()

def line(a, b, name = "Custom"):
  return Line(a, b, name)

def translatePoint(p, v):
  return (p[0] + v[0], p[1] + v[1])

def diagonalLine(start, name):
  return line(start, translatePoint(start, (-1, 1)), name)

def verticalLine(start, name):
  return line(start, translatePoint(start, (0, 1)), name)

def horizontalLine(start, name):
  return line(start, translatePoint(start, (1, 0)), name)

def top(cellIndex):
  return horizontalLine(cellIndex, CellEdges.Top)

def bottom(cellIndex):
  return horizontalLine(translatePoint(cellIndex, (0, 1)), CellEdges.Bottom)

def left(cellIndex):
  return verticalLine(cellIndex, CellEdges.Left)

def right(cellIndex):
  return verticalLine(translatePoint(cellIndex, (1, 0)), CellEdges.Right)

def diagonal(cellIndex):
  return diagonalLine(translatePoint(cellIndex, (1, 0)), CellEdges.Diagonal)

def getTextureData(x, y, data):
  return data[y][x]

def getMeters(x, y, data, metersPerHeightValue):
  return getTextureData(x, y, data)*metersPerHeightValue

def surfaceDistance(xDist, yDist):
  return math.sqrt(xDist*xDist + yDist*yDist)

def getQuadrant(line):
  start = line.getStart()
  startCol = start[0]
  startRow = start[1]
  end = line.getEnd()
  endCol = end[0]
  endRow = end[1]
  if (startCol < endCol and startRow >= endRow): return Quadrants.First
  if (startCol >= endCol and startRow > endRow): return Quadrants.Second
  if (startCol > endCol and startRow <= endRow): return Quadrants.Third
  if (startCol <= endCol and startRow < endRow): return Quadrants.Fourth    

def interpolateHeight(startHeight, endHeight, k):
  height = startHeight + (endHeight - startHeight)*k
  return height