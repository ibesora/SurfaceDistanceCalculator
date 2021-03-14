from utils import line, getMeters, surfaceDistance

def computeSurfaceDistance(start, end, data, metersPerPixel, metersPerHeightValue):
  path = line(start, end)
  if (path.length == 0): return [{"accumSurfaceDistance": 0}]
  if (path.getStart()[1] == path.getEnd()[1]): return rowDistance(path, data, metersPerPixel, metersPerHeightValue)
  if (path.getStart()[0] == path.getEnd()[0]): return columnDistance(path, data, metersPerPixel, metersPerHeightValue)
  return []

def rowDistance(line, data, metersPerPixel, metersPerHeightValue):
  return axisAlignedDistance(line, data, 0, metersPerPixel, metersPerHeightValue)

def columnDistance(line, data, metersPerPixel, metersPerHeightValue):
  return axisAlignedDistance(line, data, 1, metersPerPixel, metersPerHeightValue)

def axisAlignedDistance(line, data, index, metersPerPixel, metersPerHeightValue):
  start = line.getStart()
  end = line.getEnd()
  steps = int(end[index]) - int(start[index]) + 1
  stepsInfo = []
  
  stepsInfo.append(buildStepData(0, getMeters(int(start[0]), int(start[1]), data, metersPerHeightValue), 0, 0, 0))
  for i in range(1, steps):
    prevStep = stepsInfo[len(stepsInfo) - 1]
    prevAccum = prevStep["accumDistance"]
    prevHeight = prevStep["height"]
    prevAccumSD = prevStep["accumSurfaceDistance"]
    stepDist = metersPerPixel
    if (index == 0):
        # Traversing columns
        stepHeight = getMeters(int(start[0]) + i, int(start[1]), data, metersPerHeightValue)
    else:
        # Traversing rows
        stepHeight = getMeters(int(start[0]), int(start[1]) + i, data, metersPerHeightValue)
    stepAccumDist = prevAccum + metersPerPixel
    stepSurfaceDist = surfaceDistance(stepDist, stepHeight - prevHeight)
    stepsInfo.append(buildStepData(stepDist, stepHeight, stepAccumDist, stepSurfaceDist, prevAccumSD + stepSurfaceDist))
  return stepsInfo

def buildStepData(dist, height, accumDistance, surfaceDist, accumSurfaceDistance):
  return {
    "dist": dist,
    "height": height,
    "accumDistance": accumDistance,
    "surfaceDistance": surfaceDist,
    "accumSurfaceDistance": accumSurfaceDistance
  }