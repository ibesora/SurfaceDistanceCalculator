import math
from shapely.geometry import LineString

class Line:
  def __init__(self, start, end):
      self.geom = LineString([start, end])
  def __str__(self):
      return str((str(self.geom)))
  def getGeom(self):
      return self.geom
  def getStart(self):
      return self.geom.coords[0]
  def getEnd(self):
      return self.geom.coords[1]
  def length(self):
      return self.geom.length
  def intersection(self, lineToIntersect):
      return self.geom.intersection(lineToIntersect.geom)

def line(a, b):
    return Line(a, b)

def getTextureData(x, y, data):
  return data[y][x]

def getMeters(x, y, data, metersPerHeightValue):
  return getTextureData(x, y, data)*metersPerHeightValue

def surfaceDistance(xDist, yDist):
  return math.sqrt(xDist*xDist + yDist*yDist)