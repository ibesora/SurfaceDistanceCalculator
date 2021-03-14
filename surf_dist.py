from argparse import ArgumentParser
import numpy as np

DefaultPreFilePath = 'data/pre.data'
DefaultPostFilePath = 'data/post.data'
MetersPerPixel = 30
MetersPerHeightValue = 11

def main() -> int:
    parser = ArgumentParser('Surface distance calculator')
    parser.add_argument('-startX', required=True, dest="start_x", help="Image X coordinate of the starting point")
    parser.add_argument('-startY', required=True, dest="start_y", help="Image Y coordinate of the starting point")
    parser.add_argument('-endX', required=True, dest="end_x", help="Image X coordinate of the end point")
    parser.add_argument('-endY', required=True, dest="end_y", help="Image Y coordinate of the end point")
    parser.add_argument('-filePre', dest="file_pre", help="File to use as the pre data. Defaults to data/pre.data")
    parser.add_argument('-filePost', dest="file_post", help="Filte to use as the post data. Defaults to data/post.data")
    parser.add_argument('-metersPPx', dest="meters_per_px", help="Meters per pixel. Defaults to 30")
    parser.add_argument('-metersPHV', dest="meters_per_height_value", help="Meters per height value. Defaults to 11")
    args = parser.parse_args()
    
    filePre = DefaultPreFilePath
    filePost = DefaultPostFilePath
    metersPerPixel = MetersPerPixel
    metersPerHeightValue = MetersPerHeightValue
    if (args.file_pre is None):
        print("Argument filePre not found. Using default file ", DefaultPreFilePath)
    else:
        filePre = args.file_pre
        print("Using pre file in ", args.file_pre)
        
    if (args.file_post is None):
        print("Argument filePost not found. Using default file ", DefaultPostFilePath)
    else:
        filePre = args.file_post
        print("Using post file in ", args.file_post)
        
    if (args.meters_per_px is None):
        print("Argument metersPPx not found. Using default value ", MetersPerPixel)
    else:
        metersPerPixel = args.meters_per_px
        print("Using meters per pixel as ", int(metersPerPixel))
        
    if (args.meters_per_height_value is None):
        print("Argument metersPHV not found. Using default value ", MetersPerHeightValue)
    else:
        metersPerHeightValue = args.metersPHV
        print("Using meters per height value as ", int(metersPerHeightValue))
        
    rawDataPre = np.reshape(np.fromfile(filePre, dtype=np.ubyte), (512, 512))
    rawDataPost = np.reshape(np.fromfile(filePost, dtype=np.ubyte), (512, 512))
    startPoint = (int(args.start_x), int(args.start_y))
    endPoint = (int(args.end_x), int(args.end_y))
    
    resultsPre = computeSurfaceDistance(startPoint, endPoint, rawDataPre, metersPerPixel, metersPerHeightValue)
    resultsPost = computeSurfaceDistance(startPoint, endPoint, rawDataPost, metersPerPixel, metersPerHeightValue)
    surfaceDistPre = resultsPre[len(resultsPre) - 1]["accumSurfaceDistance"]
    surfaceDistPost = resultsPost[len(resultsPost) - 1]["accumSurfaceDistance"]
    print("Distance (m) pre eruption:", surfaceDistPre)
    print("Distance (m) post eruption:", surfaceDistPost)
    print("Difference (m):", surfaceDistPre - surfaceDistPost)   

if __name__ == '__main__':
    exit(main())
