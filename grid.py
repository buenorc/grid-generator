# -*- coding: utf-8 -*-
"""
@author: rafael de carvalho bueno

"""

import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from shapely.geometry import Polygon, Point

n = 280  # number of grid points in n-direction
m = 200  # number of grid points in m-direction 


sf = shp.Reader('.\shapefiles\landboundary_passauna')

x_center = np.zeros((n-1,m-1),float)
y_center = np.zeros((n-1,m-1),float)

layer_x  = np.zeros((n  ,m  ),float)
layer_y  = np.zeros((n  ,m  ),float)


mask     = np.zeros((n-1,m-1),bool)

points = [pt.shape.__geo_interface__ for pt in sf.shapeRecords()]
points = points[0]['coordinates']

poly = Polygon(points)

for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    
# grid boundaries
xg = np.linspace(min(x),max(x),m)
yg = np.linspace(min(y),max(y),n)

x_grid, y_grid = np.meshgrid(xg, yg)



for mi in range(m-1):
    for ni in range(n-1):
        x_center[ni,mi] = (x_grid[ni+1,mi+1]+x_grid[ni,mi])/2
        y_center[ni,mi] = (y_grid[ni+1,mi+1]+y_grid[ni,mi])/2

        mask[ni,mi] = poly.contains(Point(x_center[ni,mi], y_center[ni,mi]))
        
        if mask[ni,mi] == True:
            layer_x[ni,mi]     = x_grid[ni,mi]
            layer_x[ni,mi+1]   = x_grid[ni,mi+1]
            layer_x[ni+1,mi]   = x_grid[ni+1,mi]
            layer_x[ni+1,mi+1] = x_grid[ni+1,mi+1]
            layer_y[ni,mi]     = y_grid[ni,mi]
            layer_y[ni,mi+1]   = y_grid[ni,mi+1]
            layer_y[ni+1,mi]   = y_grid[ni+1,mi]
            layer_y[ni+1,mi+1] = y_grid[ni+1,mi+1]
                     
segs1 = np.stack((x_grid,y_grid), axis=2)
segs2 = segs1.transpose(1,0,2)

segs3 = np.stack((np.where(layer_x==0,None,layer_x),np.where(layer_y==0,None,layer_y)), axis=2)
segs4 = segs3.transpose(1,0,2)

fig, ax = plt.subplots(1,3,figsize=(10,5))
ax[0].plot(x, y, color = 'black')
ax[1].plot(x, y, color = 'black')


plt.axes(ax[1])
plt.gca().add_collection(LineCollection(segs1,lw=0.8,color='gray'))
plt.gca().add_collection(LineCollection(segs2,lw=0.8,color='gray'))
ax[1].scatter(x_grid,y_grid,s=3,marker='+', c = 'black')
ax[1].scatter(x_center,y_center,s=5,marker='x', c = 'red')


ax[2].plot(x, y, color = 'black', alpha=0.5)
ax[2].scatter(x_center[mask],y_center[mask],s=5,marker='x', c = 'red')
plt.axes(ax[2])
plt.gca().add_collection(LineCollection(segs3,lw=0.8,color='gray'))
plt.gca().add_collection(LineCollection(segs4,lw=0.8,color='gray'))


fig.tight_layout()
plt.savefig('figures\Fig1.jpg',dpi=1000)
plt.show()

layer_x = np.where(layer_x==None,0,layer_x)
layer_y[layer_y==None] = 0

file_grd = open('grid.grd','w')
file_grd.write('Coordinate System = Cartesian\n')
file_grd.write('\t{}\t{}\n'.format(m,n))
file_grd.write('{}\t{}\t{}\n'.format(0,0,0))

for ni in range(n):
    file_grd.write('Eta= {}'.format(ni+1))
    for mi in range(m):
        file_grd.write(' {}'.format(layer_x[ni,mi]))
    file_grd.write('\n')
    
for ni in range(n):
    file_grd.write('Eta= {}'.format(ni+1))
    for mi in range(m):
        file_grd.write(' {}'.format(layer_y[ni,mi]))
    file_grd.write('\n')    

file_grd.close()


