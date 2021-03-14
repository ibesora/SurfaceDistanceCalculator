from utils import line

def computeSurfaceDistance(start, end, data, metersPerPixel, metersPerHeightValue):
  path = line(start, end)
  if (path.length == 0): return [{"accumSurfaceDistance": 0}]
  return []