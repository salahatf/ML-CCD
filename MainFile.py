from Node import Node
from Members import Member
from GUI import TrussAnalysisGUI
from Truss import Truss
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import *
import numpy as np #Numpy for working with arrays
from numpy import genfromtxt #For importing structure data from csv
from xlwt import Workbook
import math

class MyApplication:
    def __init__(self, master):
        self.master = master
        master.title("Non-linear Geometric Analysis of Trusses")
        master.geometry("500x400")
        truss_2d_button = ttk.Button(master, text='2D Truss', command=lambda: self.show_popup("2D Truss"))
        truss_2d_button.pack(pady=10)

        truss_3d_button = ttk.Button(master, text='3D Truss', command=lambda: self.show_popup("3D Truss"))
        truss_3d_button.pack(pady=10)

        self.canvas = Canvas(master, width=300, height=300)      
        self.canvas.pack()      
        self.img = ImageTk.PhotoImage(Image.read("2d.GIF"))       
        self.canvas.create_image(20, 20, anchor=NW, image=self.img)

    def show_popup(self, title):
        popup = Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x200")

root = tk.Tk()
app = MyApplication(root)
root.mainloop()


#if __name__ == '__main__':
#    root = tk.Tk()
#    app = TrussAnalysisGUI(root)
#    root.mainloop()

#root = Tk()
#root.withdraw()
#InputFolder = filedialog.askdirectory(parent = root, initialdir="D:\\0. My Ph.D\1. Courses\2022-2023\Spring 2023\Advanced Structural Analysis II, CE833\Project", title='Select the location of the input files')
#resultsFile = filedialog.asksaveasfile(filetypes = [('Excel Files', '*.xls')], defaultextension = '.xls', initialfile="Results.xls",)

#wbw = Workbook()
#nodes = genfromtxt(InputFolder+'/Nodes.csv', delimiter=',')
#members = genfromtxt(InputFolder+'/Members.csv', delimiter=',',dtype=float)
#restrainedNodes = genfromtxt(InputFolder+'/BC.csv', delimiter=',',dtype=int)
#loadedNodes = genfromtxt(InputFolder+'/Load.csv', delimiter=',',dtype=float)

#Nodes = []
#Members = []
#RestrainedDOF = []
#ExternalLoad = []

#for i, node in enumerate (nodes):
#    Nodes.append(Node(node[0],node[1],node[2],i))

#for j, member in enumerate (members):
#    Members.append(Member(j,int(member[0]),int(member[1]),member[2],member[3]))

#for restrainedNode in restrainedNodes:
#    RestrainedDOF.append(3*restrainedNode)
#    RestrainedDOF.append(3*restrainedNode+1)
#    RestrainedDOF.append(3*restrainedNode+2)

#if loadedNodes.ndim == 1:
#        ExternalLoad.append([int(loadedNodes[0])*3,loadedNodes[1]])
#        ExternalLoad.append([int(loadedNodes[0])*3+1,loadedNodes[2]])
#        ExternalLoad.append([int(loadedNodes[0])*3+2,loadedNodes[3]])
#else:
#    for k in loadedNodes:
#        ExternalLoad.append([int(loadedNodes[k])*3,loadedNodes[1]])
#        ExternalLoad.append([int(loadedNodes[k])*3+1,loadedNodes[2]])
#        ExternalLoad.append([int(loadedNodes[k])*3+2,loadedNodes[3]])

#Truss1 = Truss(Nodes,Members,ExternalLoad,RestrainedDOF,resultsFile.name,wbw)
#Truss1.solve1E()
#Truss1.results()
#steps = 100
#iterations = 400
#Truss1.solve2E(Nodes,steps,iterations,1e-3)

