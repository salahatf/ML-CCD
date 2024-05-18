from databaseAndModel import databaseAndModel
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import PIL.Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MLCCD:

    def __init__(self, master):
        self.master = master
        self.master.config(highlightbackground="black", highlightthickness = 2)
        master.title("ML-CCD")
        master.geometry("550x325")
        ttk.Style().theme_use('clam')

        self.title_tab = tk.Frame(self.master, highlightbackground="black", highlightthickness = 1)
        self.title_tab.grid(row=0,column=0,columnspan =2, sticky="N")
        title_label = ttk.Label(self.title_tab, text='Machine Learning Prediction of Concrete Cover Delamination (ML-CCD)\n', font =tk.font.Font(size = 12, weight = "bold", underline=1))
        title_label.pack(fill='both',expand=True)

        self.names_tab = tk.Frame(self.master, highlightbackground="black", highlightthickness = 1, width=200, height=210)
        self.names_tab.grid(row=1,column=0, sticky="N")
        names_label1 = ttk.Label(self.names_tab, text='\n\nDeveloped By:\n', font =tk.font.Font(size = 12, weight = "bold", underline=1))
        names_label1.pack(fill='both',expand=True)
        names_label2 = ttk.Label(self.names_tab, text='Fahed H. Salahat \n(fsalahat@ppu.edu)\n', font =tk.font.Font(size = 12, weight = "bold"))
        names_label2.pack(fill='both',expand=True)
        names_label3 = ttk.Label(self.names_tab, text='Hayder A. Rasheed \n(hayder@ksu.edu)\n', font =tk.font.Font(size = 12, weight = "bold"))
        names_label3.pack(fill='both',expand=True)
        names_label4 = ttk.Label(self.names_tab, text='Huthaifa I. Ashqar \n(huthaifa.ashqar@aaup.edu)   \n', font =tk.font.Font(size = 12, weight = "bold"))
        names_label4.pack(fill='both',expand=True)

        self.logo_tab = tk.Frame(self.master, highlightbackground="black", highlightthickness = 1, width=320, height=220)
        self.logo_tab.grid(row=1,column=1,sticky="N")
        start_button = tk.Button(self.logo_tab, text='Start', fg = 'green', font = tk.font.Font(size = 12, weight = "bold"), command=lambda: self.show_popup(databaseAndModel,'Database Analysis and Model Training'), border=3)
        start_button.pack(pady=7)
        self.canvas_for_picture = Canvas(self.logo_tab, width=300, height=210)      
        self.canvas_for_picture.pack(fill='both',expand=True)
        self.img3d = ImageTk.PhotoImage(PIL.Image.open("pic.png"))
        self.canvas_for_picture.create_image(160, 120, anchor=CENTER, image = self.img3d)
        self.canvas_for_picture.config(highlightbackground="gray", highlightthickness = 1.5)

    def show_popup(self,item,title):
        item(Toplevel(self.master),title)
        
root = Tk()
app = MLCCD(root)
root.mainloop()