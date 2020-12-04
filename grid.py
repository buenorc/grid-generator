# -*- coding: utf-8 -*-
"""
@author: rafael de carvalho bueno

"""
import sys
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from shapely.geometry import Polygon, Point
from tkinter import *


class StdoutRedirector(object):

    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, str):
        self.text_area.insert(END, str)
        self.text_area.see(END)


def main (path_shape,m,n,folder_path):

    old_stdout = sys.stdout
    
    root = Tk()
    root.configure(background='white')
    root.title("Generator running") 
    root.geometry('450x500')

    outputPanel = Text(root, wrap='word', height=30, width=100)
    outputPanel.grid(column=0, row=0, columnspan = 2, sticky='NSWE', padx=5, pady=5)

    n = int(n)
    m = int(m)


    sys.stdout = StdoutRedirector(outputPanel)
    print ("> ")
    root.update()
    print ("> Grid generator is being loaded...")
    root.update()
    print ("> -----------------------------------")
    root.update()
    print ("> Grid Generator,     December 2020")
    root.update()  
    print ("> ")
    root.update() 
    if (n*m>1000):    
        print ("> This may take few minutes")
        root.update()  
    sf = shp.Reader(path_shape)

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

    dx = xg[1] - xg[0] 
    dy = yg[1] - yg[0]

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
    plt.savefig(folder_path+'/grid.jpg',dpi=1000)
    plt.show()

    layer_x = np.where(layer_x==None,0,layer_x)
    layer_y[layer_y==None] = 0

    file_grd = open(folder_path+'/grid.grd','w')
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


    print ("> ")
    root.update()
    print ("> ")
    root.update()
    print ('> Grid size x\t'+str(round(dx,2))+' m')
    print ('> Grid size y\t'+str(round(dy,2))+' m')
    root.update() 
    print ("> ")
    root.update()
    print ("> -----------------------------------")
    root.update() 
    print ("> ")
    root.update()
    print ("> FINISHED           Grid Generator ")
    root.update() 
    print ("> ")
    root.update()
    print ("> ")
    root.update()
    print ("> Check path for results:")
    root.update()
    print ("> "+folder_path)
    root.update() 
    print ("> ")
    root.update()
    print ("> ")
    root.update()
    print ("> For additional information:")
    root.update()
    print ("> shorturl.at/mqyAE")
    root.update()
    print ("> ")
    root.update()
    print ("> ")
    root.update()
    root.update()
    
    
    root.mainloop()
    sys.stdout = old_stdout