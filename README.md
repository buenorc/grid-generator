# Grid generator (with GUI)

## Rectangular grid generator for Delft3d numerical model based on closed landboundary file (shapefile)

The algorithm requires as input data the following information:

1) a shapefile (.shp) 
2) pair of integers related to the number of grid poits (-1) in m- and n- direction (integers) 

The output file generated by the algorithm, ***grid.grd***, can be used in the Delft3D model. 

PS: The program does not provide the grid enclosure file (.enc) that can be generated altomatically when the .grd is loaded and saved in RGFGRID (Delft3D model)

To run the code, the user must have installed the following packages in a Python interpreter:

1) Numpy
2) Shapely 
3) Pyshp (shapefile)
4) Tkinter (for the GUI)


