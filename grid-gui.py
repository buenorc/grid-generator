# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:38:12 2019

@author: Rafael de Carvalho Bueno
"""

import webbrowser

from tkinter import *
from tkinter import ttk
import tkinter.ttk as tka
from tkinter.filedialog import *
from tkinter import filedialog


def OpenUrl(url):
    webbrowser.open_new(url)

    
def AboutCallBack():
   msg = messagebox.showinfo( "About", " Grid Generator \n \n Rectangular grid generator for Delft3d numerical model \n \n  \n Report problems and improvements to email adresss below \n rafael.bueno.itt@gmail.com\n \n other open-source programs, see \n https://sites.google.com/view/rafaelbueno/initial \n\n\n Rafael de Carvalho Bueno ")    


def shape_input():
    global path_shape
    path_shape = askopenfilename(defaultextension='.shp', filetypes=[('SHP files','*.shp')])
    

def output_folder():

    global folder_path
    folder_path = filedialog.askdirectory()


def generator():
    
    import grid as grid
    
    xm = mnum.get()
    xn = nnum.get()
    
    grid.main(path_shape,xm,xn,folder_path)
        
# ---------------------- menu -------------------------------------------------        
window = Tk()

window.title("Grid generator") 
window.geometry('450x250')

# ----------------------- initial menu ----------------------------------------

menubar = Menu(window)
infomenu = Menu(menubar, tearoff = 0)


infomenu.add_cascade(label = "Code", command = menubar)


url = 'https://github.com/buenorc/grid-generator.git'
menubar.add_command(label = "Info",  command = lambda aurl=url:OpenUrl(aurl))
menubar.add_command(label = "About", command = AboutCallBack)
menubar.add_command(label = "Exit",  command = window.destroy)

# ----------------------- Sub-menu --------------------------------------------

Label(window,anchor="w", text="Shapefile (.shp):            ").grid(row=1,column=0,pady=4,sticky='w')
Button(window,text='Open File',command=shape_input).grid(row=1,column=1,pady=4,sticky='w')

mnum = IntVar()
nnum = IntVar()

Label(window, text="Number of grids N").grid(row=2,column=0,pady=4,sticky='w')
nnum = Entry(window, bd =3)
nnum.insert(END,50)
nnum.grid(row=2,column=1,pady=4)

Label(window, text="Number of grids M").grid(row=3,column=0,pady=4,sticky='w')
mnum = Entry(window, bd =3)
mnum.insert(END,50)
mnum.grid(row=3,column=1,pady=4)


Label(window,anchor="w", text="Output folder:").grid(row=4,column=0,pady=4,sticky='w')
Button(window,text='Open File',command=output_folder).grid(row=4,column=1,pady=4,sticky='w')

Button(window,font="Verdana 9 bold",text='Generate',command=generator, height = 1, width = 10).grid(row=6,column=0,pady=8,sticky='w')


window.config(menu = menubar)
window.mainloop()