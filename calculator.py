from utils import line, getMeters, surfaceDistance, getQuadrant, Quadrants, diagonal, top, bottom, left, right, Hit, CellEdges, interpolateHeight

def computeSurfaceDistance(start, end, data, metersPerPixel, metersPerHeightValue):
  path = line(start, end)
  if (path.length == 0): return [{"accumSurfaceDistance": 0}]
  if (path.getStart()[1] == path.getEnd()[1]): return rowDistance(path, data, metersPerPixel, metersPerHeightValue)
  if (path.getStart()[0] == path.getEnd()[0]): return columnDistance(path, data, metersPerPixel, metersPerHeightValue)
  return nonAxisAlignedDistance(path, data, metersPerPixel, metersPerHeightValue)

def rowDistance(line, data, metersPerPixel, metersPerHeightValue):
  return axisAlignedDistance(line, data, 0, metersPerPixel, metersPerHeightValue)

def columnDistance(line, data, metersPerPixel, metersPerHeightValue):
  return axisAlignedDistance(line, data, 1, metersPerPixel, metersPerHeightValue)

def axisAlignedDistance(line, data, index, metersPerPixel, metersPerHeightValue):
  start = line.getStart()
  end = line.getEnd()
  steps = abs(int(end[index]) - int(start[index])) + 1
  direction = 1 if end[index] > start[index] else -1
  print("Steps", steps)
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
      stepHeight = getMeters(int(start[0]) + i * direction, int(start[1]), data, metersPerHeightValue)
    else:
      # Traversing rows
      stepHeight = getMeters(int(start[0]), int(start[1]) + i * direction, data, metersPerHeightValue)
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

def nonAxisAlignedDistance(path, data, metersPerPixel, metersPerHeightValue):
  quadrant = getQuadrant(path)
  start = path.getStart()
  end = path.getEnd()
  currentCell = [start[0], start[1]]
  stepsInfo = []
  lastIntersectingPoint = start
      
  stepsInfo.append(buildStepData(0, getMeters(int(start[0]), int(start[1]), data, metersPerHeightValue), 0, 0, 0))
  while currentCell[0] != end[0] or currentCell[1] != end[1]:
    (intersectionHits, cellIndexUpdater) = computeIntersections(path, getLinesToTest(quadrant, currentCell))
    
    for hit in intersectionHits:
      prevStep = stepsInfo[len(stepsInfo) - 1]
      prevAccum = prevStep["accumDistance"]
      prevHeight = prevStep["height"]
      prevAccumSD = prevStep["accumSurfaceDistance"]
      stepDist = line(lastIntersectingPoint, (hit.getGeom().x, hit.getGeom().y)).length() * metersPerPixel
      startVertex = hit.getLine().getVertices()[0]
      endVertex = hit.getLine().getVertices()[1]
      startVertexHeight = getMeters(int(startVertex[0]), int(startVertex[1]), data, metersPerHeightValue)
      endVertexHeight = getMeters(int(endVertex[0]), int(endVertex[1]), data, metersPerHeightValue)
      stepHeight = interpolateHeight(startVertexHeight, endVertexHeight, hit.getNormalizedDistanceOnLine())
      stepAccumDist = prevAccum + stepDist
      stepSurfaceDist = surfaceDistance(stepDist, stepHeight - prevHeight)
      stepsInfo.append(buildStepData(stepDist, stepHeight, stepAccumDist, stepSurfaceDist, prevAccumSD + stepSurfaceDist))
      lastIntersectingPoint = (hit.getGeom().x, hit.getGeom().y)
    
    currentCell[0] += cellIndexUpdater[0]
    currentCell[1] += cellIndexUpdater[1]
  return stepsInfo

def computeIntersections(path, lines):
  def distanceSorter(hit):
    return line(path.getStart(), hit.getGeom()).length()
  
  intersections = {}
  cellUpdater = [0, 0]
  
  for i in range(0, len(lines)):
    intersection = path.intersection(lines[i])
    if (intersection.geom_type == 'Point'):
      intersections[intersection.wkt] = Hit(intersection, lines[i])
      cellUpdater = updateCellIndexUpdater(lines[i].getName(), cellUpdater)
  uniqueIntersections = list(intersections.values())
  uniqueIntersections.sort(key=distanceSorter)
  return (uniqueIntersections, cellUpdater)

def getLinesToTest(quadrant, currentCell):
  lines = []
  if (quadrant == Quadrants.First):
    lines = [diagonal(currentCell), top(currentCell), right(currentCell)]
  elif (quadrant == Quadrants.Second): 
    lines = [diagonal(currentCell), top(currentCell), left(currentCell)]
  elif (quadrant == Quadrants.Third): 
    lines = [diagonal(currentCell), bottom(currentCell), left(currentCell)]
  elif (quadrant == Quadrants.Fourth): 
    lines = [diagonal(currentCell), bottom(currentCell), right(currentCell)]
  return lines

def updateCellIndexUpdater(name, cellUpdater):
  newCellIndexUpdater = cellUpdater
  if (name == CellEdges.Top): return [cellUpdater[0], cellUpdater[1] - 1]
  elif (name == CellEdges.Bottom): return [cellUpdater[0], cellUpdater[1] + 1]
  elif (name == CellEdges.Left): return [cellUpdater[0] - 1, cellUpdater[1]]
  elif (name == CellEdges.Right): return [cellUpdater[0] + 1, cellUpdater[1]]
  return cellUpdater