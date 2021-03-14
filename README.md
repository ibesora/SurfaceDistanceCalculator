# SurfaceDistanceCalculator
Given two 512x512 heightmaps, computes the surface distance between two points and prints the difference

## Requirements
Python 3.8

## Installation
1. Create a virtual environment via `python -m venv surf_dist`
2. Activate the virtual environment with `source surf_dist/bin/activate`
3. Install the needed packages via `pip install numpy argparse shapely`

## Running
You can run the code via `python surf_dist.py -startX 0 -startY 0 -endX 511 -endY 511`

You can find the supported arguments in the following table

Parameter name | Required | Description
--- | --- | ---
startX | Yes | Image X coordinate of the starting point
startY | Yes | Image Y coordinate of the starting point
endX | Yes | Image X coordinate of the ending point
endY | Yes | Image Y coordinate of the ending point
filePre | No | File to use as the pre data. Defaults to `data/pre.data`
filePost | No | File to use as the post data. Defaults to `data/post.data`
metersPPx | No | Meters per pixel. Defaults to 30
metersPHV | No | Meters per height value. Defaults to 11

## Jupyter
There's a jupyter notebook file which contains different visualizations of the data and the computation.

To run it please perform the following steps:
1. Install the needed packages via `pip install ipykernel jupyterlab matplotlib`. You might need to also install the `wheel` package to be able to run the previous step.
2. Add the kernel to jupyter via `python -m ipykernel install --user --name=surf_dist`
3. Run `jupyter lab` and choose the `surf_dist` kernel
