from ast import Delete
from gc import disable, enable
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from turtle import clear, width
import pandas as pd
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.filedialog as fd
from pandastable import Table, TableModel, config
from Materials import Concrete, Steel, Fiber, Beam, Failure, Info
from sklearn.ensemble import RandomForestRegressor
from scipy import optimize
from scipy import stats
import numpy as np
matplotlib.use("TkAgg")

class databaseAndModel:
    def __init__(self, master,title):
        #region Master
        self.master = master
        self.master.grab_set() # to keep the window on top of the parent window
        self.master.title(title)
        self.master.geometry("850x400")
        ttk.Style().theme_use('clam')
        ttk.Style().configure('TNotebook',tabposition = 'en')
        self.notebook = ttk.Notebook(self.master) 
        self.notebook.pack(fill='both',expand=True)
        self.beamsNum = 0
        self.Y_pred = NONE
        #endregion

        #region Database Tab
        self.database_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.database_tab, text='Load Database')
        self.frame1_database = ttk.Frame(self.database_tab, height=400, width=800) 
        self.frame1_database.grid(row=0,column=0,sticky='new')       
        self.frame2_database = ttk.Frame(self.database_tab)        
        self.frame2_database.grid(row=1,column=0,sticky='new')
        self.import_database_file_button = ttk.Button(self.frame1_database, text='Import Database File', command=self.import_database)
        self.import_database_file_button.grid(row=0,column=0,columnspan = 3, sticky='nsew')  
        self.numBeams_label = ttk.Label(self.frame1_database, text="Total Number of Beams: ")
        self.numBeams_label.grid(row=0,column=5, columnspan=3, sticky="nsew", padx= 10)
        self.database_table_area = ttk.Frame(self.frame2_database)
        self.database_table_area.pack(fill='both',expand=True)
        #endregion

        #region Unstrengthened Tab
        self.unstrengthened_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.unstrengthened_tab, text='Unstrengthened Capacity')
        self.frame1_unstrengthened = ttk.Frame(self.unstrengthened_tab, height=500, width=500) 
        self.frame1_unstrengthened.grid(row=0,column=0,sticky='new')      
        self.frame2_unstrengthened = ttk.Frame(self.unstrengthened_tab)        
        self.frame2_unstrengthened.grid(row=1,column=0,sticky='new') 
        self.analyze_unstrengthened_button = ttk.Button(self.frame1_unstrengthened, text='Find Unstrengthened Capacity', command=self.unstrengthenedCapacity, state=DISABLED)
        self.analyze_unstrengthened_button.grid(row=0,column=0,sticky="N")    
        self.unstrengthened_table_area = ttk.Frame(self.frame2_unstrengthened)
        self.unstrengthened_table_area.pack(fill='both',expand=True)
        #endregion

        #region strainAndStressProfilesAtFailure Tab
        self.strainAndStressProfilesAtFailure_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.strainAndStressProfilesAtFailure_tab, text='Failure Analysis')
        self.frame1_strainAndStressProfilesAtFailure = ttk.Frame(self.strainAndStressProfilesAtFailure_tab, height=500, width=500) 
        self.frame1_strainAndStressProfilesAtFailure.grid(row=0,column=0,sticky='new')      
        self.frame2_strainAndStressProfilesAtFailure = ttk.Frame(self.strainAndStressProfilesAtFailure_tab)        
        self.frame2_strainAndStressProfilesAtFailure.grid(row=1,column=0,sticky='new') 
        self.strainAndStressProfilesAtFailure_button = ttk.Button(self.frame1_strainAndStressProfilesAtFailure, text='Obtain Failure Profiles', command=self.strainAndStressProfilesAtFailure, state=DISABLED)
        self.strainAndStressProfilesAtFailure_button.grid(row=0,column=0,sticky="N") 
        self.strainAndStressProfilesAtFailure_table_area = ttk.Frame(self.frame2_strainAndStressProfilesAtFailure)
        self.strainAndStressProfilesAtFailure_table_area.pack(fill='both',expand=True)
        #endregion

        #region Trilinear Tab
        self.trilinear_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trilinear_tab, text='Trilinear Analysis')
        self.frame1_trilinear = ttk.Frame(self.trilinear_tab, height=500, width=500) 
        self.frame1_trilinear.grid(row=0,column=0,sticky='new')      
        self.frame2_trilinear = ttk.Frame(self.trilinear_tab)        
        self.frame2_trilinear.grid(row=1,column=0,sticky='new') 
        self.trilinear_analysis_button = ttk.Button(self.frame1_trilinear, text='Perform Trilinear Analysis', command=self.trilinearParameters, state=DISABLED)
        self.trilinear_analysis_button.grid(row=0,column=0,sticky="N") 
        self.trilinear_table_area = ttk.Frame(self.frame2_trilinear)
        self.trilinear_table_area.pack(fill='both',expand=True)
        #endregion

        #region Machince Learning Tab
        self.ML_tab = tk.Frame(self.notebook)
        self.notebook.add(self.ML_tab, text='ML-Training')
        self.frame1_ML = tk.Frame(self.ML_tab, highlightbackground="black", highlightthickness = 1, width= 600, height= 400) 
        self.frame1_ML.grid(row=0,column=0, sticky='nwes', padx=7) 
        
        self.frame2_ML = tk.Frame(self.ML_tab, highlightbackground="black", highlightthickness = 1, width= 250, height= 400) 
        self.frame2_ML.grid(row=0,column=1,sticky='nwes')

        # Frame1 Content
        self.ML_config_label1 = ttk.Label(self.frame1_ML, text="Model Accuracy",  font =tk.font.Font(size = 12, weight = "bold"))
        self.ML_config_label1.grid(row=0,column=0, columnspan=3, sticky="N", padx=10, pady=4)

        self.figure = plt.Figure(figsize=(5,2.8))
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame1_ML)
        self.canvas.get_tk_widget().grid(row=2,column=0, columnspan=6, rowspan=3, sticky="NW", padx=10, pady=8)     
        self.plot_results_lable1 = ttk.Label(self.frame1_ML, text="Error Bar", background ="red", foreground = 'white', width = 20)
        self.plot_results_lable1.grid(row=1,column=0,sticky="NW", padx=2, pady=5)       
        self.plot_results_lable2 = ttk.Label(self.frame1_ML, text="Prediction Results", background ="blue", foreground = 'white', width = 20)
        self.plot_results_lable2.grid(row=1,column=1,sticky="NW", padx=2, pady=5)      
        self.plot_results_lable3 = ttk.Label(self.frame1_ML, text="Actual Results", background ="green", foreground = 'white', width = 20)
        self.plot_results_lable3.grid(row=1,column=2,sticky="NW", padx=2, pady=5)

        # Frame2 Content
        self.model_results_label1 = ttk.Label(self.frame2_ML, text="Prediction Model")
        self.model_results_label1.grid(row=0,column=0, columnspan=2, sticky="NW", padx=5, pady=3)

        self.Prediction_options = ["Random Forest"]
        self.Prediction_type = tk.StringVar()
        self.Prediction_type.set( "Random Forest" )
        self.drop = tk.OptionMenu(self.frame2_ML, self.Prediction_type , *self.Prediction_options)
        self.drop.config(width = 15)
        self.drop.grid(row=1,column=0, columnspan=2, sticky="NW", padx=5)

        self.num_of_trees = tk.IntVar()
        self.num_of_trees.set(500)

        self.random_state = tk.IntVar()
        self.random_state.set(42)

        self.error = tk.IntVar()
        self.error.set(5)

        self.explore_beam = tk.IntVar()
        self.explore_beam.set(0)

        self.model_results_label2 = ttk.Label(self.frame2_ML, text="Number of Trees")
        self.model_results_label2.grid(row=2,column=0, columnspan=2, sticky="NW", padx=5)
        self.trees_entry = tk.Entry(self.frame2_ML,textvariable = self.num_of_trees)
        self.trees_entry.grid(row=3,column=0, columnspan=2, sticky="NW", padx=5)

        self.model_results_label3 = ttk.Label(self.frame2_ML, text="Random State")
        self.model_results_label3.grid(row=4,column=0, columnspan=2, sticky="NW", padx=5)
        self.random_state_entry = tk.Entry(self.frame2_ML,textvariable = self.random_state)
        self.random_state_entry.grid(row=5,column=0, columnspan=2, sticky="NW", padx=5)

        self.train_model_button = ttk.Button(self.frame2_ML, text='Train Model', command=self.machineLearningTrainingModel, state=DISABLED)
        self.train_model_button.grid(row=6,column=0, columnspan=2, sticky="NW", padx=5, pady=5)

        self.separator = ttk.Separator(self.frame2_ML, orient='horizontal')
        self.separator.grid(row=7,column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.model_results_label4 = ttk.Label(self.frame2_ML, text="Error Percentage")
        self.model_results_label4.grid(row=8,column=0, columnspan=2, sticky="NW", padx=5, pady=5)
        self.error_entry = tk.Entry(self.frame2_ML,textvariable = self.error)
        self.error_entry.grid(row=9,column=0, columnspan=2, sticky="NW", padx=5)

        self.plot_error_button = ttk.Button(self.frame2_ML, text='Show Error', command=self.errorObservation, state=DISABLED)
        self.plot_error_button.grid(row=10,column=0, columnspan=2, sticky="NW", padx=5, pady=5)

        self.separator1 = ttk.Separator(self.frame2_ML, orient='horizontal')
        self.separator1.grid(row=11,column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.ML_results_button = ttk.Button(self.frame2_ML, text='Run Predictions', command=self.showParameters, state=DISABLED)
        self.ML_results_button.grid(row=13,column=0, columnspan=2, sticky="NW", padx=5, pady=10)


        #endregion

        #region Initiating tables
        self.database_table = None
        self.unstrengthened_table = None
        self.strainStressFailure_table = None
        self.trilinear_table = None
        self.prediction_parameters_table = None
        #endregion

    def import_database(self):
        self.analyze_unstrengthened_button.config(state = NORMAL)
        self.file_path = fd.askopenfilename(filetypes=[("Excel files", "*.xls")])
        if self.file_path:
            try:
                self.database = pd.read_excel(self.file_path, 0, header=0, index_col=None)
                self.beamsNum = len(self.database)
                self.numBeams_label = ttk.Label(self.frame1_database, text="Total Number of Beams: "+str(self.beamsNum))
                self.numBeams_label.grid(row=0,column=5, columnspan=3, sticky="nsew", padx= 10)
                self.headings = []
                for col in self.database:
                    self.headings.append(col)

                info = [Info() for i in range (self.beamsNum)]
                loading = [Failure() for i in range(self.beamsNum)]
                mat1 = [Concrete() for i in range(self.beamsNum)]
                mat2 = [Steel() for i in range(self.beamsNum)]
                mat3 = [Fiber() for i in range(self.beamsNum)]
                self.beams = [Beam() for i in range(self.beamsNum)]
                for i in range(self.beamsNum):
                    info[i].auther = self.database.Author[i]
                    info[i].autherReference = self.database.AuthorReference[i]
                    info[i].idInDatabase = int (self.database.Id_in_database[i])

                    loading[i].P = float(self.database.failure_load_N[i])
                    loading[i].a = float(self.database.a_mm[i])

                    mat1[i].H = float(self.database.H_mm[i])
                    mat1[i].B = float(self.database.B_mm[i])
                    mat1[i].L = float(self.database.L_mm[i])
                    mat1[i].fc = float(self.database.fc_MPa[i])
                    mat1[i].Ec = float(self.database.Ec_MPa[i])

                    mat2[i].fy = float(self.database.Fy_MPa[i])
                    mat2[i].Es = float(self.database.Es_MPa[i])
                    mat2[i].As = float(self.database.As_mm2[i])
                    mat2[i].Asc = float(self.database.Asc_mm2[i])
                    mat2[i].dt = float(self.database.d_mm[i])
                    mat2[i].ds = float(self.database.dc_mm[i])
                    mat2[i].Av = float(self.database.Av_mm2[i])
                    mat2[i].s = float(self.database.S_mm[i])
                    mat2[i].fyt = float(self.database.fyt_MPa[i])

                    mat3[i].n = float(self.database.n[i])
                    mat3[i].Ef = float(self.database.Ef_MPa[i])
                    mat3[i].ffu = float(self.database.ffu_MPa[i])
                    mat3[i].lp = float(self.database.Lp_mm[i])
                    mat3[i].bf = float(self.database.bf_mm[i])
                    mat3[i].df = float(self.database.df_mm[i])
                    mat3[i].tf = float(self.database.tf_mm[i])
                    mat3[i].ap = float(self.database.ap_mm[i])


                    self.beams[i].ID = i + 1
                    self.beams[i].Info = info[i]
                    self.beams[i].loading = loading[i]
                    self.beams[i].mat1 = mat1[i]
                    self.beams[i].mat2 = mat2[i]
                    self.beams[i].mat3 = mat3[i]
                
                self.database_table = Table(self.database_table_area, dataframe=self.database, showtoolbar=False, showstatusbar=True, width=630, height=300)
                options = config.load_options()
                options = {'font': 'Cambria','fontsize': 10,'cellwidth': 20}
                config.apply_options(options, self.database_table)
                self.database_table.autoResizeColumns() 
                self.database_table.show()
                      
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.database = None
           
    def unstrengthenedCapacity(self):
        self.strainAndStressProfilesAtFailure_button.config(state = NORMAL)
        self.unstrengthened = pd.DataFrame(columns = ['BeamID','fc_MPa','fy_MPa','concrete_strain','c_mm','tensile_steel_strain','tensile_steel_stress_MPa','compressive_steel_strain','compressive_steel_stress_MPa','Mun_Nmm'])
        self.numBeams_label1 = ttk.Label(self.frame1_unstrengthened, text="Total Number of Beams: " + str(self.beamsNum))
        self.numBeams_label1.grid(row=0,column=1, sticky="nsew", padx= 10)
        for i in range(self.beamsNum):

            fc = self.beams[i].mat1.fc
            ec = self.beams[i].mat1.Ec
            b = self.beams[i].mat1.B
            h = self.beams[i].mat1.H
            As = self.beams[i].mat2.As
            Asc = self.beams[i].mat2.Asc
            dt = self.beams[i].mat2.dt
            ds = self.beams[i].mat2.ds
            es = self.beams[i].mat2.Es
            fy = self.beams[i].mat2.fy
           
            if fc <= 30:
                beta1_norm = 0.85
            elif fc > 30 and fc < 55:
                beta1_norm = 1.09 - 0.008 * fc
            else:
                beta1_norm = 0.65

        #Finding unstrengthed moment including Asc
            def signal(x,y):
                if abs(x)<abs(y):
                    return x
                else:
                    if x<0:
                        return -y
                    else:
                        return y
            def forceEquilibrium(x):
                eps_un = 0.003*(x-ds)/x
                fps = signal(eps_un*es, fy)
                ees_un = 0.003*(dt-x)/x
                fs = signal(ees_un*es,fy)
                equilibrium = 0.85*beta1_norm*fc*b*x+Asc*fps-As*fs
                return equilibrium
            for layer in range(1,101):
                step=(layer/100)*h
                if forceEquilibrium(step) > - 7000 and forceEquilibrium(step) < 7000:
                    c_norm = step
                    break
            root = optimize.newton(forceEquilibrium,c_norm)
            self.beams[i].Cun = root
            eps_un = 0.003*(self.beams[i].Cun-ds)/self.beams[i].Cun
            fps = signal(eps_un*es, fy)
            ees_un = 0.003*(dt-self.beams[i].Cun)/self.beams[i].Cun
            fs = signal(ees_un*es,fy)
            self.beams[i].Mun = As*fs*(dt-0.5*beta1_norm*self.beams[i].Cun)+Asc*fps*(0.5*beta1_norm*self.beams[i].Cun-ds)

            self.unstrengthened.at[i,'BeamID'] = self.beams[i].ID
            self.unstrengthened.fc_MPa[i] = fc
            self.unstrengthened.fy_MPa[i] = fy
            self.unstrengthened.concrete_strain[i] = 0.003
            self.unstrengthened.c_mm[i] = self.beams[i].Cun
            self.unstrengthened.tensile_steel_strain[i] = ees_un
            self.unstrengthened.tensile_steel_stress_MPa[i] = fs
            self.unstrengthened.compressive_steel_strain[i] = eps_un
            self.unstrengthened.compressive_steel_stress_MPa[i] = fps
            self.unstrengthened.Mun_Nmm[i] = self.beams[i].Mun

        try:
            self.unstrengthened_table = Table(self.unstrengthened_table_area, dataframe=self.unstrengthened.astype({'fc_MPa':'float64','c_mm':'float64', 'tensile_steel_strain':'float64', 'compressive_steel_strain':'float64', 'tensile_steel_stress_MPa':'float64','compressive_steel_stress_MPa':'float64', 'Mun_Nmm':'float64'}), showtoolbar=False, showstatusbar=True, width=630, height=300)
            options = config.load_options()
            options = {'font': 'Cambria','fontsize': 10,'cellwidth': 60}
            config.apply_options(options, self.unstrengthened_table)
            #self.unstrengthened_table.autoResizeColumns()
            self.unstrengthened_table.show()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.unstrengthened = None

    def strainAndStressProfilesAtFailure(self):
        self.trilinear_analysis_button.config(state = NORMAL)
        self.strainStressProfilesAtFailure = pd.DataFrame(columns = ['BeamID','c_mm', 'ecf','eps','es','efcd','fps_MPa','fs_MPa','ff_MPa','Mexp_Nmm','M_verify','F_verify','Flag','Decision'])
        self.verified_counter=0
        self.numBeams_label2 = ttk.Label(self.frame1_strainAndStressProfilesAtFailure, text="Total Number of Beams: " + str(self.beamsNum))
        self.numBeams_label2.grid(row=0,column=1, sticky="nsew", padx= 10)

        for i in range(self.beamsNum):
            Pexp = self.beams[i].loading.P
            Mexp = self.beams[i].loading.get_M()
            fc = self.beams[i].mat1.fc
            ec = self.beams[i].mat1.Ec
            b = self.beams[i].mat1.B
            h = self.beams[i].mat1.H
            epc = 1.71 * fc / ec
            As = self.beams[i].mat2.As
            Asc = self.beams[i].mat2.Asc
            dt = self.beams[i].mat2.dt
            ds = self.beams[i].mat2.ds
            es = self.beams[i].mat2.Es
            fy = self.beams[i].mat2.fy
 
        #Finding failure strain profile

            Af = self.beams[i].mat3.get_Af()
            ef = self.beams[i].mat3.Ef
            df = self.beams[i].mat3.df
            tf = self.beams[i].mat3.tf
            ey = fy / es
            
            guess1 = 0.003
            guess2 = self.beams[i].Cun
    
            # case1 both no yielding
            def case1(x):
                return [((x[0] / epc) - (pow(x[0], 2) / (3 * pow(epc, 2)))) * fc * b * x[1] + Asc * (es * x[0] * (x[1] - ds) / x[1]) - As * (es * x[0] * (dt - x[1]) / x[1]) - Af * ef * (x[0] * (df - x[1]) / x[1]),As * es * (x[0] * (dt - x[1]) / x[1]) * (dt - (((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5) + Asc * (es * x[0] * (x[1] - ds) / x[1]) * ((((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5 - ds) + Af * ef * (x[0] * (df - x[1]) / x[1]) * (df - (((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5)-self.beams[i].loading.get_M()]

            answer1 = optimize.fsolve(case1, [guess1,guess2])
            if (answer1[0] * (answer1[1] - ds) / answer1[1]) < ey and (answer1[0] * (dt - answer1[1]) / answer1[1]) < ey:
                self.beams[i].ecf_exp = answer1[0]
                self.beams[i].Cexp = answer1[1]
                epsf = (answer1[0] * (answer1[1] - ds) / answer1[1])
                eesf = (answer1[0] * (dt - answer1[1]) / answer1[1])

            # case2 Asc no yield and As yield
            def case2(x):
                return [((x[0] / epc) - (pow(x[0], 2) / (3 * pow(epc, 2)))) * fc * b * x[1] + Asc * (es * x[0] * (x[1] - ds) / x[1]) - As * fy - Af * ef * (x[0] * (df - x[1]) / x[1]),As * fy * (dt - (((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5) + Asc * (es * x[0] * (x[1] - ds) / x[1]) * ((((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5 - ds) + Af * ef * (x[0] * (df - x[1]) / x[1]) * (df - (((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5)-self.beams[i].loading.get_M()]
            
            answer2 = optimize.fsolve(case2,[guess1,guess2])
            if (answer2[0] * (answer2[1] - ds) / answer2[1]) < ey and (answer2[0] * (dt - answer2[1]) / answer2[1]) >= ey:
                self.beams[i].ecf_exp = answer2[0]
                self.beams[i].Cexp = answer2[1]
                epsf = (answer2[0] * (answer2[1] - ds) / answer2[1])
                eesf = ey
 
            # case3 both yielding
            def case3(x):
                return [((x[0] / epc) - (pow(x[0], 2) / (3 * pow(epc, 2)))) * fc * b * x[1] + Asc * fy - As * fy - Af * ef * (x[0] * (df - x[1]) / x[1]),As * fy * (dt - (((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5) + Asc * fy * ((((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5 - ds) + Af * ef * (x[0] * (df - x[1]) / x[1]) * (df - (((4 * epc) - x[0]) / ((6 * epc) - (2 * x[0]))) * x[1] * 0.5)-self.beams[i].loading.get_M()]
            
            answer3 = optimize.fsolve(case3,[guess1,guess2])
            if (answer3[0] * (answer3[1] - ds) / answer3[1]) >= ey and (answer3[0] * (dt - answer3[1]) / answer3[1]) >= ey:
                self.beams[i].ecf_exp = answer3[0]
                self.beams[i].Cexp = answer3[1]
                epsf = ey
                eesf = ey
            
            self.beams[i].efcd_exp = self.beams[i].ecf_exp * (df - self.beams[i].Cexp) / self.beams[i].Cexp
            fpsf = epsf * es
            self.beams[i].fsf = eesf * es
            self.beams[i].fff = self.beams[i].efcd_exp * ef

            gama = ((1/3)-(self.beams[i].ecf_exp/(12*epc)))/(1-self.beams[i].ecf_exp/(3*epc))
            M_verify = As*self.beams[i].fsf*(dt-gama*self.beams[i].Cexp)+Af*self.beams[i].fff*(df-gama*self.beams[i].Cexp)+Asc*fpsf*(gama*self.beams[i].Cexp-ds)
            Alpha = (self.beams[i].ecf_exp / epc) - (pow(self.beams[i].ecf_exp, 2) / (3 * pow(epc, 2)))
            F_verify = Alpha*fc * b * self.beams[i].Cexp + Asc*fpsf - As*self.beams[i].fsf - Af*self.beams[i].fff
            if abs(M_verify-Mexp)>0.01:
                self.beams[i].M_verified = False
            if abs(F_verify)>0.01:
               self.beams[i].F_verified = False
            if self.beams[i].ecf_exp>=0.003:
                self.beams[i].ecf_verified = False
            
            #['BeamID','c_mm', 'ecf','eps','es','efcd','fps_MPa','fs_MPa','ff_MPa','Mexp_Nmm','M_verify','F_verify','Flag','Decision','TotalBeams','VerifiedBeams']
            self.strainStressProfilesAtFailure.at[i,'BeamID'] = self.beams[i].ID
            self.strainStressProfilesAtFailure.c_mm[i] = self.beams[i].Cexp
            self.strainStressProfilesAtFailure.ecf[i] = self.beams[i].ecf_exp
            self.strainStressProfilesAtFailure.eps[i] = epsf
            self.strainStressProfilesAtFailure.es[i] = eesf
            self.strainStressProfilesAtFailure.efcd[i] = self.beams[i].efcd_exp
            self.strainStressProfilesAtFailure.fps_MPa[i] = fpsf
            self.strainStressProfilesAtFailure.fs_MPa[i] = self.beams[i].fsf
            self.strainStressProfilesAtFailure.ff_MPa[i] = self.beams[i].fff
            self.strainStressProfilesAtFailure.Mexp_Nmm[i] = self.beams[i].loading.get_M()
            self.strainStressProfilesAtFailure.M_verify[i] = M_verify
            self.strainStressProfilesAtFailure.F_verify = F_verify

            if not self.beams[i].ecf_verified:
                self.strainStressProfilesAtFailure.Flag[i] = 'Concrete Crushing'
            if not self.beams[i].M_verified or not self.beams[i].F_verified:
                self.strainStressProfilesAtFailure.Decision[i] = 'No Convergence, Excluded'
           
            if self.beams[i].ecf_verified and self.beams[i].M_verified and self.beams[i].F_verified: 
                self.verified_counter+=1
                
        self.numBeams_label3 = ttk.Label(self.frame1_strainAndStressProfilesAtFailure, text="Verified Beams: " + str(self.verified_counter))
        self.numBeams_label3.grid(row=0,column=2, sticky="nsew", padx= 10)

        try:
            self.strainStressFailure_table = Table(self.strainAndStressProfilesAtFailure_table_area, dataframe=self.strainStressProfilesAtFailure.astype({'BeamID':'int','c_mm':'float', 'ecf':'float','eps':'float','es':'float','efcd':'float','fps_MPa':'float','fs_MPa':'float','ff_MPa':'float','Mexp_Nmm':'float','M_verify':'float','F_verify':'float','Flag':'str','Decision':'str'}), showtoolbar=False, showstatusbar=True, width=630, height=300)
            options = config.load_options()
            options = {'font': 'Cambria','fontsize': 10,'cellwidth': 60}
            config.apply_options(options, self.strainStressFailure_table)
            self.strainStressFailure_table.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.strainStressProfilesAtFailure = None

    def trilinearParameters(self):
        self.train_model_button.config(state = NORMAL)
        self.trilinearAnalysis = pd.DataFrame(columns = ['BeamID','Mexp','Mcr','ecf_cr','Ccr','Phi_cr','My','ecf_y','Cy','phi_y','Mn','ecf_n','Cn','phi_n','Mn_FailureMode','Comparison'])
        self.correlation = pd.DataFrame(columns = ['BeamID','x_axis', 'StrengtheningRatio'])
        self.numBeams_label4 = ttk.Label(self.frame1_trilinear, text="Total Number of Beams: " + str(self.beamsNum))
        self.numBeams_label4.grid(row=0,column=1, sticky="nsew", padx= 10)
        for i in range(self.beamsNum):
            counter = 0
            if self.beams[i].ecf_verified and self.beams[i].M_verified and self.beams[i].F_verified:
                fc = self.beams[i].mat1.fc
                ec = self.beams[i].mat1.Ec
                b = self.beams[i].mat1.B
                h = self.beams[i].mat1.H
                es = self.beams[i].mat2.Es
                fy = self.beams[i].mat2.fy
                ef = self.beams[i].mat3.Ef
                As = self.beams[i].mat2.As
                dt = self.beams[i].mat2.dt
                Asc = self.beams[i].mat2.Asc
                ds = self.beams[i].mat2.ds
                Af = self.beams[i].mat3.get_Af()
                df = self.beams[i].mat3.df
                ns = es/ec
                nf = ef/ec
                epc = 1.71 * fc / ec

                #Cracking
                yt = (0.5*b*h**2+As*(ns-1)*dt+Asc*(ns-1)*ds+Af*nf*df)/(b*h+(ns-1)*(As+Asc)+nf*Af)
                yb = h-yt
                Igt = (b*pow(h,3)/12)+(b*h*pow((0.5*h-yt),2))+((ns-1)*As*pow((dt-yt),2))+((ns-1)*Asc*pow((ds-yt),2))+(nf*Af*pow((df-yt),2))
                fr = 0.62*pow(fc,0.5)
                self.beams[i].Mcr = fr*Igt/yb
                self.beams[i].Ccr = yt
                self.beams[i].phi_cr = fr/(ec*yb)
                self.beams[i].ecf_cr = self.beams[i].Ccr*self.beams[i].phi_cr

                #Yielding
                ey = fy/es
            
                def force_yn(x):
                    return ((ey*x/(dt-x))/epc-(ey*x/(dt-x))**2/(3*epc**2))*fc*b*x+Asc*es*(ey*(x-ds)/(dt-x))-As*fy-Af*ef*(ey*(df-x)/(dt-x))
                
                for layer in range(1,101):
                    step=self.beams[i].Ccr*(1-layer/100)
                    if force_yn(step) > - 7000 and force_yn(step) < 7000:
                        guess = step
                        break

                self.beams[i].Cy = optimize.newton(force_yn,guess,tol=1e-04)
                fps = es*ey*(self.beams[i].Cy-ds)/(dt-self.beams[i].Cy)

                if fps>=fy:
                    def force_yy(x):
                        return (((ey*x/(dt-x))/epc-(ey*x/(dt-x))**2/(3*epc**2))*fc*b*x+Asc*fy-As*fy-Af*ef*(ey*(df-x)/(dt-x)))
                    
                    for layer in range(1,101):
                        step=self.beams[i].Ccr*(1-layer/100)
                        if force_yy(step) > - 7000 and force_yy(step) < 7000:
                            guess = step
                            break
                    self.beams[i].Cy = optimize.newton(force_yy,guess)
                    fps = fy
            
                self.beams[i].ecf_y = ey*self.beams[i].Cy/(dt-self.beams[i].Cy)
                self.beams[i].phi_y = self.beams[i].ecf_y/self.beams[i].Cy
                gama = ((1/3)-(self.beams[i].ecf_y/(12*epc)))/(1-self.beams[i].ecf_y/(3*epc))
                ff = ef*ey*(df-self.beams[i].Cy)/(dt-self.beams[i].Cy)
                self.beams[i].My = As*fy*(dt-gama*self.beams[i].Cy)+Af*ff*(df-gama*self.beams[i].Cy)+Asc*fps*(gama*self.beams[i].Cy-ds)

                #Ultimate
            
                #Start with concrete crushing
                if fc <= 30:
                    beta1_norm = 0.85
                elif fc > 30 and fc < 55:
                    beta1_norm = 1.09 - 0.008 * fc
                else:
                    beta1_norm = 0.65
                     
                def force_uccn(x):
                    return (0.85*beta1_norm*fc*b*x+Asc*es*(0.003*(x-ds)/x)-Af*ef*(0.003*(df-x)/x)-As*fy)
              
                
                for layer in range(1,101):
                    step=0.5*h*(1-layer/100)
                    if force_uccn(step) > - 7000 and force_uccn(step) < 7000:
                        guess = step
                        break
                
                self.beams[i].Cn = optimize.newton(force_uccn,guess)
        
                fps = es*0.003*(self.beams[i].Cn-ds)/(self.beams[i].Cn)
         
                if fps>fy:
                    def force_uccy(x):
                        return (0.85*beta1_norm*fc*b*x+Asc*fy-Af*ef*(0.003*(df-x)/x)-As*fy)
                    
                    for layer in range(1,101):
                        step=0.5*h*(1-layer/100)
                        if force_uccy(step) > - 7000 and force_uccy(step) < 7000:
                            guess = step
                            break
                    self.beams[i].Cn = optimize.newton(force_uccy,guess)
                    fps = fy
            
                efn = 0.003*(df-self.beams[i].Cn)/self.beams[i].Cn

                self.beams[i].ecf_n =  0.003
                self.beams[i].phi_n = self.beams[i].ecf_n/self.beams[i].Cn
                self.beams[i].Mn = As*fy*(dt-0.5*beta1_norm*self.beams[i].Cn)+Af*ef*efn*(df-0.5*beta1_norm*self.beams[i].Cn)+Asc*fps*(0.5*beta1_norm*self.beams[i].Cn-ds)
            
                #Checking the rupture case
                efu = self.beams[i].mat3.get_efu()
            
                if efn>efu:  
                    def force_urn(x):
                        return ((((efu*x/(df-x))/epc)-(efu*x/(df-x))**2/(3*epc**2))*fc*b*x+Asc*es*(efu*(x-ds)/(df-x))-As*fy-Af*ef*efu)
                    
                    for layer in range(1,101):
                        step=0.5*h*(1-layer/100)
                        if force_urn(step) > - 7000 and force_urn(step) < 7000:
                            guess = step
                            break
                    self.beams[i].Cn = optimize.newton(force_urn,guess)
                    self.beams[i].ecf_n = efu*self.beams[i].Cn/(df-self.beams[i].Cn)
                    efn = efu
                    fps = es*efu*(self.beams[i].Cn-ds)/(df-self.beams[i].Cn)
               
                    if fps>fy:
                        def force_ury(x):
                            return ((((efu*x/(df-x))/epc)-(efu*x/(df-x))**2/(3*epc**2))*fc*b*x+Asc*fy-As*fy-Af*ef*efu)
                        
                        for layer in range(1,101):
                            step=0.5*h*(1-layer/100)
                            if force_ury(step) > - 7000 and force_ury(step) < 7000:
                                guess = step
                                break
                        self.beams[i].Cn = optimize.newton(force_ury,guess)
                        fps = fy
                
                    self.beams[i].phi_n = efu/(df-self.beams[i].Cn)
                    self.beams[i].ecf_n = self.beams[i].phi_n * self.beams[i].Cn
                    gama = ((1/3)-(self.beams[i].ecf_n/(12*epc)))/(1-self.beams[i].ecf_n/(3*epc))
                    self.beams[i].Mn = As*fy*(dt-gama*self.beams[i].Cn)+Af*ef*efn*(df-gama*self.beams[i].Cn)+Asc*fps*(gama*self.beams[i].Cn-ds)

                self.beams[i].Mn_verified = False
                if self.beams[i].Mn > self.beams[i].loading.get_M():
                    self.beams[i].Mn_verified = True
                    rohf = Af / (b * dt)
                    rohs = As / (b * dt)
                    #xaxis1 = rohf *self.beams[i].fff* df / (rohs * fy * dt)
                    xaxis1 = rohf *efn*ef* df / (rohs * fy * dt)
                    #yaxis1 = (self.beams[i].loading.get_M() / self.beams[i].Mun)*(fy/self.beams[i].fsf)
                    yaxis1 = (self.beams[i].Mn / self.beams[i].Mun)#*(fy/self.beams[i].fsf)
                   
                    self.correlation.at[i,'BeamID'] = self.beams[i].ID
                    self.correlation.x_axis[i] = xaxis1 #(ρfxff/ρsxfy)x(df/d)
                    self.correlation.StrengtheningRatio[i] = yaxis1
                    counter+=1
                
                if self.beams[i].ecf_n == 0.003:
                    self.MnFailureMode = 'Concrete Crushing'
                else:
                    self.MnFailureMode = 'FRP Rupture'

                #Writing results ['BeamID','Mexp','Mcr','ecf_cr','Ccr','Phi_cr','My','ecf_y','Cy','phi_y','Mn','ecf_n','Cn','phi_n','Mn_FailureMode','Comparison']
                self.trilinearAnalysis.at[i,'BeamID'] = self.beams[i].ID
                self.trilinearAnalysis.Mexp[i] = self.beams[i].loading.get_M()

                self.trilinearAnalysis.Mcr[i] = self.beams[i].Mcr
                self.trilinearAnalysis.ecf_cr[i] = self.beams[i].ecf_cr
                self.trilinearAnalysis.Ccr[i] = self.beams[i].Ccr
                self.trilinearAnalysis.Phi_cr[i] = self.beams[i].phi_cr

                self.trilinearAnalysis.My[i] = self.beams[i].My
                self.trilinearAnalysis.ecf_y[i] = self.beams[i].ecf_y
                self.trilinearAnalysis.Cy[i] = self.beams[i].Cy
                self.trilinearAnalysis.phi_y[i] = self.beams[i].phi_y

                self.trilinearAnalysis.Mn[i] = self.beams[i].Mn
                self.trilinearAnalysis.ecf_n[i] = self.beams[i].ecf_n
                self.trilinearAnalysis.Cn[i] = self.beams[i].Cn
                self.trilinearAnalysis.phi_n[i] = self.beams[i].phi_n

                self.trilinearAnalysis.Mn_FailureMode[i] = self.MnFailureMode
 
                if self.beams[i].loading.get_M()>self.beams[i].Mn:
                    self.trilinearAnalysis.Comparison[i] = 'Mexp>Mn'

        self.numBeams_label4 = ttk.Label(self.frame1_trilinear, text="Verified Beams: " + str(self.verified_counter-counter))
        self.numBeams_label4.grid(row=0,column=2, sticky="nsew", padx= 10)
        try:

            self.trilinear_table = Table(self.trilinear_table_area, dataframe=self.trilinearAnalysis.astype({'BeamID':'int','Mexp':'float','Mcr':'float','ecf_cr':'float','Ccr':'float','Phi_cr':'float','My':'float','ecf_y':'float','Cy':'float','phi_y':'float','Mn':'float','ecf_n':'float','Cn':'float','phi_n':'float','Mn_FailureMode':'str'}), showtoolbar=False, showstatusbar=True, width=625, height=300)
            options = config.load_options()
            options = {'font': 'Cambria','fontsize': 10,'cellwidth': 60}
            config.apply_options(options, self.trilinear_table)
            self.trilinear_table.autoResizeColumns() 
            self.trilinear_table.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.trilinearAnalysis = None

    def machineLearningTrainingModel(self):
        self.ML_results_button.config(state = NORMAL)
        self.plot_error_button.config(state = NORMAL)
        self.ML_parameters = pd.DataFrame(columns = ['BeamID','a_mm','ap_mm','L_mm','Lp_mm','n','bf_mm','tf_mm','Ef_MPa','As_mm2','Es_MPa','Texp_Mid_N'])
        for i in range(self.beamsNum):
            if self.beams[i].ecf_verified and self.beams[i].M_verified and self.beams[i].F_verified and self.beams[i].Mn_verified:
                #region PROPERTIES
                fc = self.beams[i].mat1.fc
                L = self.beams[i].mat1.L
                As = self.beams[i].mat2.As
                es = self.beams[i].mat2.Es
                Af = self.beams[i].mat3.get_Af()
                ef = self.beams[i].mat3.Ef
                bf = self.beams[i].mat3.bf
                tf = self.beams[i].mat3.tf
                num = self.beams[i].mat3.n
                ap = self.beams[i].mat3.ap
                lp = self.beams[i].mat3.lp
                efcdf = self.beams[i].efcd_exp
                Texp_Mid = Af*ef*efcdf
                a = self.beams[i].loading.a

                #endregion

                #['BeamID','a_mm','ap_mm','L_mm','Lp_mm','n','bf_mm','tf_mm','Ef_MPa','As_mm2','Es_MPa','Texp_Mid_N']
                self.ML_parameters.at[i,'BeamID'] = self.beams[i].ID
                self.ML_parameters.a_mm[i] = a
                self.ML_parameters.ap_mm[i] = ap
                self.ML_parameters.L_mm[i] = L
                self.ML_parameters.Lp_mm[i] = lp
                self.ML_parameters.n[i] = num
                self.ML_parameters.bf_mm[i] = bf
                self.ML_parameters.tf_mm[i] = tf
                self.ML_parameters.Ef_MPa[i] = ef
                self.ML_parameters.As_mm2[i] = As
                self.ML_parameters.Es_MPa[i] = es
                self.ML_parameters.Texp_Mid_N[i] = Texp_Mid

        #Random Forest
        X = self.ML_parameters.drop(columns=['BeamID', 'Texp_Mid_N'])
        Y = self.ML_parameters.Texp_Mid_N

        # create regressor object
        self.regressor = RandomForestRegressor(n_estimators=self.num_of_trees.get(),random_state=self.random_state.get())

        # fit the regressor with x and y data
        self.regressor.fit(X, Y)
        # test the output by changing values
        self.Y_pred = self.regressor.predict(X)
        
        self.res = pd.DataFrame({'Predicted_N' : self.Y_pred, 'Texp_Mid_N' : Y,})
        self.figure.clear()
        ax = self.figure.add_subplot()
        ax.plot(self.ML_parameters.BeamID,self.ML_parameters.Texp_Mid_N/self.ML_parameters.Texp_Mid_N,"g-", linewidth=3 )
        ax.plot(self.ML_parameters.BeamID, self.Y_pred/self.ML_parameters.Texp_Mid_N, "b-", linewidth=1 )
        ax.set(xlim=(0, self.beamsNum), xticks=np.arange(self.beamsNum, self.beamsNum))
        ax.set_ylabel('Predicted/Actual', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='normal', size=10))
        ax.set_xlabel('Data Points', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='normal', size=10))
        plt.margins(False)
        self.canvas.draw()

    def errorObservation(self):
        self.canvas.get_tk_widget().destroy()
        self.ML_error = pd.DataFrame(columns = ['BeamID','Texp_Mid_N','ErrorValue'])
        for i in range(self.beamsNum):
            if self.beams[i].ecf_verified and self.beams[i].M_verified and self.beams[i].F_verified and self.beams[i].Mn_verified:
                #region PROPERTIES
                Af = self.beams[i].mat3.get_Af()
                ef = self.beams[i].mat3.Ef
                bf = self.beams[i].mat3.bf
                tf = self.beams[i].mat3.tf
                num = self.beams[i].mat3.n
                efcdf = self.beams[i].efcd_exp
                Texp_Mid = Af*ef*efcdf

                #endregion

                #['BeamID','a_mm','ap_mm','L_mm','Lp_mm','n','bf_mm','tf_mm','Ef_MPa','As_mm2','Es_MPa','Texp_Mid_N','ErrorValue']
                self.ML_error.at[i,'BeamID'] = self.beams[i].ID
                self.ML_error.Texp_Mid_N[i] = Texp_Mid
                self.ML_error.ErrorValue[i] = self.error.get() * Texp_Mid / 100
        self.figure.clear()
        self.figure = plt.Figure(figsize=(5,2.8))
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame1_ML)
        self.canvas.get_tk_widget().grid(row=3,column=0, columnspan=6, rowspan=3, sticky="NW", padx=10, pady=8)
        ax = self.figure.add_subplot()
        ax.plot(self.ML_error.BeamID,self.ML_error.Texp_Mid_N/self.ML_error.Texp_Mid_N,"g-", linewidth=3 )
        ax.plot(self.ML_error.BeamID, self.Y_pred/self.ML_error.Texp_Mid_N, "b-", linewidth=1 )
        ax.errorbar(self.ML_error.BeamID, self.Y_pred/self.ML_error.Texp_Mid_N, yerr=self.ML_error.ErrorValue/self.ML_error.Texp_Mid_N, linewidth=1, capsize=4, ecolor='red')
        ax.set(xlim=(0, self.beamsNum), xticks=np.arange(self.beamsNum, self.beamsNum))
        ax.set_ylabel('Predicted/Actual', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='normal', size=10))
        ax.set_xlabel('Data Points', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='normal', size=10))
        plt.margins(False)
        self.canvas.draw()
    
    def showParameters(self):
        self.parameters_window = Toplevel(width = 500, height = 500)
        self.parameters_window.grab_set()
        self.parameters_window.title("MLCCD-Parameters")
        self.parameters_notebook = ttk.Notebook(self.parameters_window) 
        self.parameters_notebook.grid(row=0, column=0, sticky='nsew')
        self.parameters_show_tab = tk.Frame(self.parameters_notebook)
        self.parameters_notebook.add(self.parameters_show_tab, text='Training Parameters') 
        self.prediction_parameters_table_area = ttk.Frame(self.parameters_show_tab)
        self.prediction_parameters_table_area.pack(fill='both',expand=True)
        self.prediction_parameters_table = Table(self.prediction_parameters_table_area, dataframe=self.ML_parameters.astype({'BeamID':'int','a_mm':'float','ap_mm':'float','L_mm':'float','Lp_mm':'float','n':'int','bf_mm':'float','tf_mm':'float','Ef_MPa':'float','As_mm2':'float','Es_MPa':'float','Texp_Mid_N':'float'}), showtoolbar=False, showstatusbar=True, width=750, height=300)
        options = config.load_options()
        options = {'font': 'Cambria','fontsize': 10,'cellwidth': 60}
        config.apply_options(options, self.prediction_parameters_table)
        self.prediction_parameters_table.show()

        self.correlation_tab = tk.Frame(self.parameters_notebook)
        self.parameters_notebook.add(self.correlation_tab, text='Calibration') 
        self.frame1_correlation = tk.Frame(self.correlation_tab, highlightbackground="black", highlightthickness = 1, width= 600, height= 450) 
        self.frame1_correlation.grid(row=0,column=0, sticky='nwes', padx=7)

        self.slope = tk.DoubleVar()
        self.slope_label = ttk.Label(self.frame1_correlation, text="Slope")
        self.slope_label.grid(row=0,column=0, sticky="W", padx=2)
        self.slope_entry = tk.Entry(self.frame1_correlation ,textvariable = self.slope, width = 20)
        self.slope_entry.grid(row=0,column=1, sticky="W", padx=2)

        self.intercept = tk.DoubleVar()
        self.intercept_label = ttk.Label(self.frame1_correlation, text="Intercept")
        self.intercept_label.grid(row=0,column=2, sticky="W")
        self.intercept_entry = tk.Entry(self.frame1_correlation ,textvariable = self.intercept, width = 20)
        self.intercept_entry.grid(row=0,column=3, sticky="W")

        self.update_correlation_button = ttk.Button(self.frame1_correlation, text='Update Correlation', command=self.updateCorrelation)
        self.update_correlation_button.grid(row=1,column=0, columnspan=3, sticky="W")
         
        self.figure1 = plt.Figure(figsize=(5,4))
        self.canvas1 = FigureCanvasTkAgg(self.figure1, self.frame1_correlation)
        self.canvas1.get_tk_widget().grid(row=2,column=0,columnspan=4,rowspan=2, sticky="W")     
        
        df = pd.DataFrame(zip(self.correlation.x_axis, self.correlation.StrengtheningRatio))
        df = df[(np.abs(stats.zscore(df)) < 3.5).all(axis=1)]
        b, m = np.polyfit(df[0], df[1], 1) #(bx+m)
        self.slope.set(b)
        self.intercept.set(m)
        ax = self.figure1.add_subplot()
        ax.plot(df[0], df[1], 'o', label='Original data', markersize=6)
        ax.plot(df[0], b*df[0] + m, 'r')
        ax.text(1, 3, 'y = ' + ' {:.2f}'.format(b) + 'x + '+ '{:.2f}'.format(m), size=8)

        ax.set_ylabel('Strengthening Ratio', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='normal', size=10))
        ax.set_xlabel('(ρf.ff.df/ρs.fy.d)', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='italic', size=10))
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        self.canvas1.draw()

        self.frame2_correlation = tk.Frame(self.correlation_tab, highlightbackground="black", highlightthickness = 1, width= 350, height= 450) 
        self.frame2_correlation.grid(row=0,column=1,sticky='nwes', padx=7)

        self.prediction_label = ttk.Label(self.frame2_correlation, text="Beam Prediction Parameters", font =tk.font.Font(family="Helvetica", size = 10, weight = "bold", underline=1))
        self.prediction_label.grid(row=0,column=0, columnspan = 4, sticky="N", padx=2, pady=8)

        self.a = tk.DoubleVar()
        self.a_label = ttk.Label(self.frame2_correlation, text="a_mm")
        self.a_label.grid(row=1,column=0, sticky="W", padx=2)
        self.a_entry = tk.Entry(self.frame2_correlation ,textvariable = self.a, width = 10)
        self.a_entry.grid(row=1,column=1, sticky="W", padx=2)

        self.h = tk.DoubleVar()
        self.h_label = ttk.Label(self.frame2_correlation, text="H_mm")
        self.h_label.grid(row=1,column=2, sticky="W", padx=2)
        self.h_entry = tk.Entry(self.frame2_correlation ,textvariable = self.h, width = 10)
        self.h_entry.grid(row=1,column=3, sticky="W", padx=2)

        self.b = tk.DoubleVar()
        self.b_label = ttk.Label(self.frame2_correlation, text="B_mm")
        self.b_label.grid(row=2,column=0, sticky="W", padx=2)
        self.b_entry = tk.Entry(self.frame2_correlation ,textvariable = self.b, width = 10)
        self.b_entry.grid(row=2,column=1, sticky="W", padx=2)

        self.L = tk.DoubleVar()
        self.L_label = ttk.Label(self.frame2_correlation, text="L_mm")
        self.L_label.grid(row=2,column=2, sticky="W", padx=2)
        self.L_entry = tk.Entry(self.frame2_correlation ,textvariable = self.L, width = 10)
        self.L_entry.grid(row=2,column=3, sticky="W", padx=2)

        self.fc = tk.DoubleVar()
        self.fc_label = ttk.Label(self.frame2_correlation, text="fc_MPa")
        self.fc_label.grid(row=3,column=0, sticky="W", padx=2)
        self.fc_entry = tk.Entry(self.frame2_correlation ,textvariable = self.fc, width = 10)
        self.fc_entry.grid(row=3,column=1, sticky="W", padx=2)

        self.Ec = tk.DoubleVar()
        self.Ec_label = ttk.Label(self.frame2_correlation, text="Ec_MPa")
        self.Ec_label.grid(row=3,column=2, sticky="W", padx=2)
        self.Ec_entry = tk.Entry(self.frame2_correlation ,textvariable = self.Ec, width = 10)
        self.Ec_entry.grid(row=3,column=3, sticky="W", padx=2)

        self.fy = tk.DoubleVar()
        self.fy_label = ttk.Label(self.frame2_correlation, text="fy_MPa")
        self.fy_label.grid(row=4,column=0, sticky="W", padx=2)
        self.fy_entry = tk.Entry(self.frame2_correlation ,textvariable = self.fy, width = 10)
        self.fy_entry.grid(row=4,column=1, sticky="W", padx=2)

        self.Es = tk.DoubleVar()
        self.Es_label = ttk.Label(self.frame2_correlation, text="Es_MPa")
        self.Es_label.grid(row=4,column=2, sticky="W", padx=2)
        self.Es_entry = tk.Entry(self.frame2_correlation ,textvariable = self.Es, width = 10)
        self.Es_entry.grid(row=4,column=3, sticky="W", padx=2)

        self.As = tk.DoubleVar()
        self.As_label = ttk.Label(self.frame2_correlation, text="As_mm2")
        self.As_label.grid(row=5,column=0, sticky="W", padx=2)
        self.As_entry = tk.Entry(self.frame2_correlation ,textvariable = self.As, width = 10)
        self.As_entry.grid(row=5,column=1, sticky="W", padx=2)

        self.Asc = tk.DoubleVar()
        self.Asc_label = ttk.Label(self.frame2_correlation, text="Asc_mm2")
        self.Asc_label.grid(row=5,column=2, sticky="W", padx=2)
        self.Asc_entry = tk.Entry(self.frame2_correlation ,textvariable = self.Asc, width = 10)
        self.Asc_entry.grid(row=5,column=3, sticky="W", padx=2)

        self.d = tk.DoubleVar()
        self.d_label = ttk.Label(self.frame2_correlation, text="d_mm")
        self.d_label.grid(row=6,column=0, sticky="W", padx=2)
        self.d_entry = tk.Entry(self.frame2_correlation ,textvariable = self.d, width = 10)
        self.d_entry.grid(row=6,column=1, sticky="W", padx=2)

        self.dc = tk.DoubleVar()
        self.dc_label = ttk.Label(self.frame2_correlation, text="dc_mm")
        self.dc_label.grid(row=6,column=2, sticky="W", padx=2)
        self.dc_entry = tk.Entry(self.frame2_correlation ,textvariable = self.dc, width = 10)
        self.dc_entry.grid(row=6,column=3, sticky="W", padx=2)

        self.Av = tk.DoubleVar()
        self.Av_label = ttk.Label(self.frame2_correlation, text="Av_mm2")
        self.Av_label.grid(row=7,column=0, sticky="W", padx=2)
        self.Av_entry = tk.Entry(self.frame2_correlation ,textvariable = self.Av, width = 10)
        self.Av_entry.grid(row=7,column=1, sticky="W", padx=2)

        self.s = tk.DoubleVar()
        self.s_label = ttk.Label(self.frame2_correlation, text="s_mm")
        self.s_label.grid(row=7,column=2, sticky="W", padx=2)
        self.s_entry = tk.Entry(self.frame2_correlation ,textvariable = self.s, width = 10)
        self.s_entry.grid(row=7,column=3, sticky="W", padx=2)

        self.fyt = tk.DoubleVar()
        self.fyt_label = ttk.Label(self.frame2_correlation, text="fyt_MPa")
        self.fyt_label.grid(row=8,column=0, sticky="W", padx=2)
        self.fyt_entry = tk.Entry(self.frame2_correlation ,textvariable = self.fyt, width = 10)
        self.fyt_entry.grid(row=8,column=1, sticky="W", padx=2)

        self.n = tk.IntVar()
        self.n_label = ttk.Label(self.frame2_correlation, text="Num of sheets")
        self.n_label.grid(row=8,column=2, sticky="W", padx=2)
        self.n_entry = tk.Entry(self.frame2_correlation ,textvariable = self.n, width = 10)
        self.n_entry.grid(row=8,column=3, sticky="W", padx=2)

        self.Ef = tk.DoubleVar()
        self.Ef_label = ttk.Label(self.frame2_correlation, text="Ef_MPa")
        self.Ef_label.grid(row=9,column=0, sticky="W", padx=2)
        self.Ef_entry = tk.Entry(self.frame2_correlation ,textvariable = self.Ef, width = 10)
        self.Ef_entry.grid(row=9,column=1, sticky="W", padx=2)

        self.ffu = tk.DoubleVar()
        self.ffu_label = ttk.Label(self.frame2_correlation, text="ffu_MPa")
        self.ffu_label.grid(row=9,column=2, sticky="W", padx=2)
        self.ffu_entry = tk.Entry(self.frame2_correlation ,textvariable = self.ffu, width = 10)
        self.ffu_entry.grid(row=9,column=3, sticky="W", padx=2)

        self.Lp = tk.DoubleVar()
        self.Lp_label = ttk.Label(self.frame2_correlation, text="Lp_mm")
        self.Lp_label.grid(row=10,column=0, sticky="W", padx=2)
        self.Lp_entry = tk.Entry(self.frame2_correlation ,textvariable = self.Lp, width = 10)
        self.Lp_entry.grid(row=10,column=1, sticky="W", padx=2)

        self.bf = tk.DoubleVar()
        self.bf_label = ttk.Label(self.frame2_correlation, text="bf_mm")
        self.bf_label.grid(row=10,column=2, sticky="W", padx=2)
        self.bf_entry = tk.Entry(self.frame2_correlation ,textvariable = self.bf, width = 10)
        self.bf_entry.grid(row=10,column=3, sticky="W", padx=2)

        self.df = tk.DoubleVar()
        self.df_label = ttk.Label(self.frame2_correlation, text="df_mm")
        self.df_label.grid(row=11,column=0, sticky="W", padx=2)
        self.df_entry = tk.Entry(self.frame2_correlation ,textvariable = self.df, width = 10)
        self.df_entry.grid(row=11,column=1, sticky="W", padx=2)

        self.tf = tk.DoubleVar()
        self.tf_label = ttk.Label(self.frame2_correlation, text="tf_mm")
        self.tf_label.grid(row=11,column=2, sticky="W", padx=2)
        self.tf_entry = tk.Entry(self.frame2_correlation ,textvariable = self.tf, width = 10)
        self.tf_entry.grid(row=11,column=3, sticky="W", padx=2)

        self.ap = tk.DoubleVar()
        self.ap_label = ttk.Label(self.frame2_correlation, text="ap_mm")
        self.ap_label.grid(row=12,column=0, sticky="W", padx=2)
        self.ap_entry = tk.Entry(self.frame2_correlation ,textvariable = self.ap, width = 10)
        self.ap_entry.grid(row=12,column=1, sticky="W", padx=2)

        self.separator2 = ttk.Separator(self.frame2_correlation, orient='horizontal')
        self.separator2.grid(row=14,column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        self.autoFill_button = ttk.Button(self.frame2_correlation, text='Fill from sheet 2', command=self.read_excel_and_fill_entries)
        self.autoFill_button.grid(row=15,column=0, columnspan=2, sticky="W", pady=10)

        self.runResults_button = ttk.Button(self.frame2_correlation, text='Update Input', command=self.update_entries)
        self.runResults_button.grid(row=16,column=0, columnspan=2, sticky="W", pady=10)

        self.runResults_button = ttk.Button(self.frame2_correlation, text='Run Results', command=self.results)
        self.runResults_button.grid(row=17,column=0, columnspan=2, sticky="W", pady=10)

        self.testedBeam = Beam()
        self.fillBeam = pd.DataFrame(columns = ['a_mm','H_mm','B_mm','L_mm','fc_MPa','Ec_MPa','Fy_MPa','Es_MPa','As_mm2','Asc_mm2','d_mm','dc_mm','Av_mm2','S_mm','fyt_MPa','n','Ef_MPa','ffu_MPa','Lp_mm','bf_mm','df_mm','tf_mm','ap_mm'])
        
        self.testedBeam.loading.a = self.fillBeam.a_mm[0] = self.a.get()
        self.testedBeam.mat1.H = self.fillBeam.H_mm[0] = self.h.get()
        self.testedBeam.mat1.B = self.fillBeam.B_mm[0] = self.b.get()
        self.testedBeam.mat1.L = self.fillBeam.L_mm[0] = self.L.get()
        self.testedBeam.mat1.fc = self.fillBeam.fc_MPa[0] = self.fc.get()
        self.testedBeam.mat1.Ec = self.fillBeam.Ec_MPa[0] = self.Ec.get()

        self.testedBeam.mat2.fy = self.fillBeam.Fy_MPa[0] = self.fy.get()
        self.testedBeam.mat2.Es = self.fillBeam.Es_MPa[0] = self.Es.get()
        self.testedBeam.mat2.As = self.fillBeam.As_mm2[0] = self.As.get()
        self.testedBeam.mat2.Asc = self.fillBeam.Asc_mm2[0] = self.Asc.get()
        self.testedBeam. mat2.dt = self.fillBeam.d_mm[0] = self.d.get()
        self.testedBeam.mat2.ds = self.fillBeam.dc_mm[0] = self.dc.get()
        self.testedBeam.mat2.Av = self.fillBeam.Av_mm2[0] = self.Av.get()
        self.testedBeam.mat2.s = self.fillBeam.S_mm[0] = self.s.get()
        self.testedBeam.mat2.fyt = self.fillBeam.fyt_MPa[0] = self.fyt.get()

        self.testedBeam.mat3.n = self.fillBeam.n[0] = self.n.get()
        self.testedBeam.mat3.Ef = self.fillBeam.Ef_MPa[0] = self.Ef.get()
        self.testedBeam.mat3.ffu = self.fillBeam.ffu_MPa[0] = self.ffu.get()
        self.testedBeam.mat3.lp = self.fillBeam.Lp_mm[0] = self.Lp.get()
        self.testedBeam.mat3.bf = self.fillBeam.bf_mm[0] = self.bf.get()
        self.testedBeam.mat3.df = self.fillBeam.df_mm[0] = self.df.get()
        self.testedBeam.mat3.tf = self.fillBeam.tf_mm[0] = self.tf.get()
        self.testedBeam.mat3.ap = self.fillBeam.ap_mm[0] = self.ap.get()

    def read_excel_and_fill_entries(self):
        try:
            self.fillBeam = pd.read_excel(self.file_path, 1, header=0, index_col=None)
            self.a.set(self.fillBeam.a_mm[0])
            self.h.set(self.fillBeam.H_mm[0])
            self.b.set(self.fillBeam.B_mm[0])
            self.L.set(self.fillBeam.L_mm[0])
            self.fc.set(self.fillBeam.fc_MPa[0])
            self.Ec.set(self.fillBeam.Ec_MPa[0])
            self.fy.set(self.fillBeam.Fy_MPa[0])
            self.Es.set(self.fillBeam.Es_MPa[0])
            self.As.set(self.fillBeam.As_mm2[0])
            self.Asc.set(self.fillBeam.Asc_mm2[0])
            self.d.set(self.fillBeam.d_mm[0])
            self.dc.set(self.fillBeam.dc_mm[0])
            self.Av.set(self.fillBeam.Av_mm2[0])
            self.s.set(self.fillBeam.S_mm[0])
            self.fyt.set(self.fillBeam.fyt_MPa[0])
            self.n.set(self.fillBeam.n[0])
            self.Ef.set(self.fillBeam.Ef_MPa[0])
            self.ffu.set(self.fillBeam.ffu_MPa[0])
            self.Lp.set(self.fillBeam.Lp_mm[0])
            self.bf.set(self.fillBeam.bf_mm[0])
            self.df.set(self.fillBeam.df_mm[0])
            self.tf.set(self.fillBeam.tf_mm[0])
            self.ap.set(self.fillBeam.ap_mm[0])

            self.testedBeam.loading.a = self.fillBeam.a_mm[0] = self.a.get()
            self.testedBeam.mat1.H = self.fillBeam.H_mm[0] = self.h.get()
            self.testedBeam.mat1.B = self.fillBeam.B_mm[0] = self.b.get()
            self.testedBeam.mat1.L = self.fillBeam.L_mm[0] = self.L.get()
            self.testedBeam.mat1.fc = self.fillBeam.fc_MPa[0] = self.fc.get()
            self.testedBeam.mat1.Ec = self.fillBeam.Ec_MPa[0] = self.Ec.get()

            self.testedBeam.mat2.fy = self.fillBeam.Fy_MPa[0] = self.fy.get()
            self.testedBeam.mat2.Es = self.fillBeam.Es_MPa[0] = self.Es.get()
            self.testedBeam.mat2.As = self.fillBeam.As_mm2[0] = self.As.get()
            self.testedBeam.mat2.Asc = self.fillBeam.Asc_mm2[0] = self.Asc.get()
            self.testedBeam. mat2.dt = self.fillBeam.d_mm[0] = self.d.get()
            self.testedBeam.mat2.ds = self.fillBeam.dc_mm[0] = self.dc.get()
            self.testedBeam.mat2.Av = self.fillBeam.Av_mm2[0] = self.Av.get()
            self.testedBeam.mat2.s = self.fillBeam.S_mm[0] = self.s.get()
            self.testedBeam.mat2.fyt = self.fillBeam.fyt_MPa[0] = self.fyt.get()

            self.testedBeam.mat3.n = self.fillBeam.n[0] = self.n.get()
            self.testedBeam.mat3.Ef = self.fillBeam.Ef_MPa[0] = self.Ef.get()
            self.testedBeam.mat3.ffu = self.fillBeam.ffu_MPa[0] = self.ffu.get()
            self.testedBeam.mat3.lp = self.fillBeam.Lp_mm[0] = self.Lp.get()
            self.testedBeam.mat3.bf = self.fillBeam.bf_mm[0] = self.bf.get()
            self.testedBeam.mat3.df = self.fillBeam.df_mm[0] = self.df.get()
            self.testedBeam.mat3.tf = self.fillBeam.tf_mm[0] = self.tf.get()
            self.testedBeam.mat3.ap = self.fillBeam.ap_mm[0] = self.ap.get()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.database = None

    def update_entries(self):
        try:
            self.testedBeam.loading.a = self.fillBeam.a_mm[0] = self.a.get()
            self.testedBeam.mat1.H = self.fillBeam.H_mm[0] = self.h.get()
            self.testedBeam.mat1.B = self.fillBeam.B_mm[0] = self.b.get()
            self.testedBeam.mat1.L = self.fillBeam.L_mm[0] = self.L.get()
            self.testedBeam.mat1.fc = self.fillBeam.fc_MPa[0] = self.fc.get()
            self.testedBeam.mat1.Ec = self.fillBeam.Ec_MPa[0] = self.Ec.get()

            self.testedBeam.mat2.fy = self.fillBeam.Fy_MPa[0] = self.fy.get()
            self.testedBeam.mat2.Es = self.fillBeam.Es_MPa[0] = self.Es.get()
            self.testedBeam.mat2.As = self.fillBeam.As_mm2[0] = self.As.get()
            self.testedBeam.mat2.Asc = self.fillBeam.Asc_mm2[0] = self.Asc.get()
            self.testedBeam. mat2.dt = self.fillBeam.d_mm[0] = self.d.get()
            self.testedBeam.mat2.ds = self.fillBeam.dc_mm[0] = self.dc.get()
            self.testedBeam.mat2.Av = self.fillBeam.Av_mm2[0] = self.Av.get()
            self.testedBeam.mat2.s = self.fillBeam.S_mm[0] = self.s.get()
            self.testedBeam.mat2.fyt = self.fillBeam.fyt_MPa[0] = self.fyt.get()

            self.testedBeam.mat3.n = self.fillBeam.n[0] = self.n.get()
            self.testedBeam.mat3.Ef = self.fillBeam.Ef_MPa[0] = self.Ef.get()
            self.testedBeam.mat3.ffu = self.fillBeam.ffu_MPa[0] = self.ffu.get()
            self.testedBeam.mat3.lp = self.fillBeam.Lp_mm[0] = self.Lp.get()
            self.testedBeam.mat3.bf = self.fillBeam.bf_mm[0] = self.bf.get()
            self.testedBeam.mat3.df = self.fillBeam.df_mm[0] = self.df.get()
            self.testedBeam.mat3.tf = self.fillBeam.tf_mm[0] = self.tf.get()
            self.testedBeam.mat3.ap = self.fillBeam.ap_mm[0] = self.ap.get()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.database = None

    def updateCorrelation(self):
        self.figure1 = plt.Figure(figsize=(5,4))
        self.canvas1 = FigureCanvasTkAgg(self.figure1, self.frame1_correlation)
        self.canvas1.get_tk_widget().grid(row=2,column=0,columnspan=4,rowspan=2, sticky="NW", pady=5)     
        df = pd.DataFrame(zip(self.correlation.x_axis, self.correlation.StrengtheningRatio))
        df = df[(np.abs(stats.zscore(df)) < 3.5).all(axis=1)]
        b, m = np.polyfit(df[0], df[1], 1) #(bx+m)

        ax = self.figure1.add_subplot()
        ax.plot(df[0], df[1], 'o', label='Original data', markersize=6)
        ax.plot(df[0], float(self.slope_entry.get())*df[0] + float(self.intercept_entry.get()), 'r', label='Fitted line')
        ax.text(1, 3, 'y = ' + ' {:.2f}'.format(float(self.slope_entry.get())) + 'x + '+ '{:.2f}'.format(float(self.intercept_entry.get())), size=8)

        ax.set_ylabel('Strengthening Ratio', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='normal', size=10))
        ax.set_xlabel('(ρf.ff.df/ρs.fy.d)', fontproperties=font_manager.FontProperties(family='Times New Roman', weight='bold', style='italic', size=10))
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        self.canvas1.draw()

    def results(self):
        #region Predict
        X = pd.DataFrame(self.fillBeam, columns= ['a_mm','ap_mm','L_mm','Lp_mm','n','bf_mm','tf_mm','Ef_MPa','As_mm2','Es_MPa'])
        Y_pred = self.regressor.predict(X)
        #endregion

        #region Initiate parameters
        fc = self.testedBeam.mat1.fc# = self.fillBeam.fc_Mpa[0]
        ec = self.testedBeam.mat1.Ec# = self.fillBeam.Ec_Mpa[0]
        b = self.testedBeam.mat1.B# = self.fillBeam.B_mm[0]
        h = self.testedBeam.mat1.H# = self.fillBeam.H_mm[0]
        As = self.testedBeam.mat2.As# = self.fillBeam.As_mm2[0]
        Asc = self.testedBeam.mat2.Asc# = self.fillBeam.Asc_mm2[0]
        dt = self.testedBeam.mat2.dt# = self.fillBeam.d_mm[0]
        ds = self.testedBeam.mat2.ds# = self.fillBeam.dc_mm[0]
        es = self.testedBeam.mat2.Es# = self.fillBeam.Es_Mpa[0]
        fy = self.testedBeam.mat2.fy #= self.fillBeam.Fy_Mpa[0]
        ef = self.testedBeam.mat3.Ef
        df = self.testedBeam.mat3.df
        tf = self.testedBeam.mat3.tf
        Af = self.testedBeam.mat3.get_Af()
        n = self.testedBeam.mat3.n
        epc = 1.71 * fc / ec
        ns = es/ec
        nf = ef/ec
        #endregion

        #region Finding unstrengthened moment
        if fc <= 30:
            beta1_norm = 0.85
        elif fc > 30 and fc < 55:
            beta1_norm = 1.09 - 0.008 * fc
        else:
            beta1_norm = 0.65

        def signal(x,y):
            if abs(x)<abs(y):
                return x
            else:
                if x<0:
                    return -y
                else:
                    return y
        def forceEquilibrium(x):
            eps_un = 0.003*(x-ds)/x
            fps = signal(eps_un*es, fy)
            ees_un = 0.003*(dt-x)/x
            fs = signal(ees_un*es,fy)
            equilibrium = 0.85*beta1_norm*fc*b*x+Asc*fps-As*fs
            return equilibrium
        for layer in range(1,101):
            step=(layer/100)*h
            if forceEquilibrium(step) > - 7000 and forceEquilibrium(step) < 7000:
                c_norm = step
                break
        root = optimize.newton(forceEquilibrium,c_norm)
        self.testedBeam.Cun = root
        eps_un = 0.003*(self.testedBeam.Cun-ds)/self.testedBeam.Cun
        fps = signal(eps_un*es, fy)
        ees_un = 0.003*(dt-self.testedBeam.Cun)/self.testedBeam.Cun
        fs = signal(ees_un*es,fy)
        self.testedBeam.Mun = As*fs*(dt-0.5*beta1_norm*self.testedBeam.Cun)+Asc*fps*(0.5*beta1_norm*self.testedBeam.Cun-ds)
        #endregion

        #region Finding Cracking
        yt = (0.5*b*h**2+As*(ns-1)*dt+Asc*(ns-1)*ds+Af*nf*df)/(b*h+(ns-1)*(As+Asc)+nf*Af)
        yb = h-yt
        Igt = (b*pow(h,3)/12)+(b*h*pow((0.5*h-yt),2))+((ns-1)*As*pow((dt-yt),2))+((ns-1)*Asc*pow((ds-yt),2))+(nf*Af*pow((df-yt),2))
        fr = 0.62*pow(fc,0.5)
        self.testedBeam.Mcr = fr*Igt/yb
        self.testedBeam.Ccr = yt
        self.testedBeam.phi_cr = fr/(ec*yb)
        self.testedBeam.ecf_cr = self.testedBeam.Ccr*self.testedBeam.phi_cr
        #endregion

        #region Finding Yielding
        ey = fy/es
            
        def force_yn(x):
            return ((ey*x/(dt-x))/epc-(ey*x/(dt-x))**2/(3*epc**2))*fc*b*x+Asc*es*(ey*(x-ds)/(dt-x))-As*fy-Af*ef*(ey*(df-x)/(dt-x))
                
        for layer in range(1,101):
            step=self.testedBeam.Ccr*(1-layer/100)
            if force_yn(step) > - 7000 and force_yn(step) < 7000:
                guess = step
                break

        self.testedBeam.Cy = optimize.newton(force_yn,guess,tol=1e-04)
        fps = es*ey*(self.testedBeam.Cy-ds)/(dt-self.testedBeam.Cy)

        if fps>=fy:
            def force_yy(x):
                return (((ey*x/(dt-x))/epc-(ey*x/(dt-x))**2/(3*epc**2))*fc*b*x+Asc*fy-As*fy-Af*ef*(ey*(df-x)/(dt-x)))
                    
            for layer in range(1,101):
                step=self.testedBeam.Ccr*(1-layer/100)
                if force_yy(step) > - 7000 and force_yy(step) < 7000:
                    guess = step
                    break
            self.testedBeam.Cy = optimize.newton(force_yy,guess)
            fps = fy
            
        self.testedBeam.ecf_y = ey*self.testedBeam.Cy/(dt-self.testedBeam.Cy)
        self.testedBeam.phi_y = self.testedBeam.ecf_y/self.testedBeam.Cy
        gama = ((1/3)-(self.testedBeam.ecf_y/(12*epc)))/(1-self.testedBeam.ecf_y/(3*epc))
        ff = ef*ey*(df-self.testedBeam.Cy)/(dt-self.testedBeam.Cy)
        self.testedBeam.My = As*fy*(dt-gama*self.testedBeam.Cy)+Af*ff*(df-gama*self.testedBeam.Cy)+Asc*fps*(gama*self.testedBeam.Cy-ds)
        #endregion 

        #region Finding ultimate capacity
        #Start with concrete crushing
        if fc <= 30:
            beta1_norm = 0.85
        elif fc > 30 and fc < 55:
            beta1_norm = 1.09 - 0.008 * fc
        else:
            beta1_norm = 0.65
                     
        def force_uccn(x):
            return (0.85*beta1_norm*fc*b*x+Asc*es*(0.003*(x-ds)/x)-Af*ef*(0.003*(df-x)/x)-As*fy)
              
                
        for layer in range(1,101):
            step=0.5*h*(1-layer/100)
            if force_uccn(step) > - 7000 and force_uccn(step) < 7000:
                guess = step
                break
                
        self.testedBeam.Cn = optimize.newton(force_uccn,guess)
        
        fps = es*0.003*(self.testedBeam.Cn-ds)/(self.testedBeam.Cn)
         
        if fps>fy:
            def force_uccy(x):
                return (0.85*beta1_norm*fc*b*x+Asc*fy-Af*ef*(0.003*(df-x)/x)-As*fy)
                    
            for layer in range(1,101):
                step=0.5*h*(1-layer/100)
                if force_uccy(step) > - 7000 and force_uccy(step) < 7000:
                    guess = step
                    break
            self.testedBeam.Cn = optimize.newton(force_uccy,guess)
            fps = fy
            
        efn = 0.003*(df-self.testedBeam.Cn)/self.testedBeam.Cn

        self.testedBeam.ecf_n =  0.003
        self.testedBeam.phi_n = self.testedBeam.ecf_n/self.testedBeam.Cn
        self.testedBeam.Mn = As*fy*(dt-0.5*beta1_norm*self.testedBeam.Cn)+Af*ef*efn*(df-0.5*beta1_norm*self.testedBeam.Cn)+Asc*fps*(0.5*beta1_norm*self.testedBeam.Cn-ds)
            
        #Checking the rupture case
        efu = self.testedBeam.mat3.get_efu()
            
        if efn>efu:  
            def force_urn(x):
                return ((((efu*x/(df-x))/epc)-(efu*x/(df-x))**2/(3*epc**2))*fc*b*x+Asc*es*(efu*(x-ds)/(df-x))-As*fy-Af*ef*efu)
                    
            for layer in range(1,101):
                step=0.5*h*(1-layer/100)
                if force_urn(step) > - 7000 and force_urn(step) < 7000:
                    guess = step
                    break
            self.testedBeam.Cn = optimize.newton(force_urn,guess)
            self.testedBeam.ecf_n = efu*self.testedBeam.Cn/(df-self.testedBeam.Cn)
            efn = efu
            fps = es*efu*(self.testedBeam.Cn-ds)/(df-self.testedBeam.Cn)
               
            if fps>fy:
                def force_ury(x):
                    return ((((efu*x/(df-x))/epc)-(efu*x/(df-x))**2/(3*epc**2))*fc*b*x+Asc*fy-As*fy-Af*ef*efu)
                        
                for layer in range(1,101):
                    step=0.5*h*(1-layer/100)
                    if force_ury(step) > - 7000 and force_ury(step) < 7000:
                        guess = step
                        break
                self.testedBeam.Cn = optimize.newton(force_ury,guess)
                fps = fy
                
            self.testedBeam.phi_n = efu/(df-self.testedBeam.Cn)
            self.testedBeam.ecf_n = self.testedBeam.phi_n * self.testedBeam.Cn
            gama = ((1/3)-(self.testedBeam.ecf_n/(12*epc)))/(1-self.testedBeam.ecf_n/(3*epc))
            self.testedBeam.Mn = As*fy*(dt-gama*self.testedBeam.Cn)+Af*ef*efn*(df-gama*self.testedBeam.Cn)+Asc*fps*(gama*self.testedBeam.Cn-ds)
        #endregion
        
        #region Show results
        X = (self.testedBeam.phi_n-self.testedBeam.phi_y)/(self.testedBeam.Mn-self.testedBeam.My)
        Z = (self.testedBeam.ecf_n-self.testedBeam.ecf_y)/(self.testedBeam.Mn-self.testedBeam.My)
        X_bar = (self.testedBeam.phi_y-self.testedBeam.phi_cr)/(self.testedBeam.My-self.testedBeam.Mcr)
        Z_bar = (self.testedBeam.ecf_y-self.testedBeam.ecf_cr)/(self.testedBeam.My-self.testedBeam.Mcr)
        Debonding_Strain = 0.41*math.sqrt(fc/(n*ef*tf))
        rohf = Af / (b * dt)
        rohs = As / (b * dt)
        self.prediction_results = pd.DataFrame(columns = ['Mun','Mn','FRP_strain_nominal','FRP_strain_debonding','FRP_strain_CCD', 'Critical_strain','X_axis','Strengthening_ratio','Critical_Mn'])
        self.prediction_results.at[0,'Mun'] = self.testedBeam.Mun
        self.prediction_results.Mn[0] = self.testedBeam.Mn
        self.prediction_results.FRP_strain_nominal[0] = efn
        self.prediction_results.FRP_strain_debonding[0] = Debonding_Strain
        
        def get_strain(M_init):
            if M_init < self.testedBeam.Mcr:
                phi = M_init*self.testedBeam.phi_cr/self.testedBeam.Mcr
                ecf = M_init*self.testedBeam.ecf_cr/self.testedBeam.Mcr
                efcd = phi*df-ecf

            if M_init > self.testedBeam.Mcr and M_init < self.testedBeam.My:
                phi = M_init*X_bar-self.testedBeam.Mcr*X_bar+self.testedBeam.phi_cr
                ecf = M_init*Z_bar-self.testedBeam.Mcr*Z_bar+self.testedBeam.ecf_cr
                efcd = phi*df-ecf  

            if M_init > self.testedBeam.My:
                phi = M_init*X-self.testedBeam.My*X+self.testedBeam.phi_y
                ecf = M_init*Z-self.testedBeam.My*Z+self.testedBeam.ecf_y
                efcd = phi*df-ecf  
            return efcd
        
        strain1 = Y_pred[0]/(ef*Af)
        xaxis = rohf * strain1 * ef * df / (rohs * fy * dt)
        yaxis = self.slope.get()*xaxis+self.intercept.get()
        M_init = yaxis * self.testedBeam.Mun
        strain2 = get_strain(M_init)
        self.prediction_results.FRP_strain_CCD[0] = strain2
        strains = [efn,Debonding_Strain,strain2]
        strains.sort()
        self.prediction_results.Critical_strain[0] = strains[0]
        xaxis = rohf *ef*strains[0]* df / (rohs * fy * dt)
        yaxis = self.slope.get()*xaxis+self.intercept.get()
        self.prediction_results.X_axis[0] = xaxis
        self.prediction_results.Strengthening_ratio[0] = self.slope.get()*xaxis+self.intercept.get()
        self.prediction_results.Critical_Mn[0] = min(yaxis * self.testedBeam.Mun,self.testedBeam.Mn)
        

        self.results_window = Toplevel(width = 500, height = 500)
        self.results_window.grab_set()
        self.results_window.title("Prediction Results")
        self.results_frame = ttk.Frame(self.results_window) 
        self.results_frame.pack(fill='both',expand=True)

        #self.prediction_parameters_table = Table(self.prediction_parameters_table_area, dataframe=self.ML_parameters.astype({'BeamID':'int','a_mm':'float','ap_mm':'float','L_mm':'float','Lp_mm':'float','n':'int','bf_mm':'float','tf_mm':'float','Ef_MPa':'float','As_mm2':'float','Es_MPa':'float','Texp_Mid_N':'float'}), showtoolbar=False, showstatusbar=True, width=750, height=300)
        self.prediction_results_output = Table(self.results_frame, dataframe=self.prediction_results.astype({'Mun':'float','Mn':'float','FRP_strain_nominal':'float','FRP_strain_debonding':'float','FRP_strain_CCD':'float','Critical_strain':'float','X_axis':'float','Strengthening_ratio':'float','Critical_Mn':'float'}), showtoolbar=False, showstatusbar=True, width=755, height = 40)
        options = config.load_options()
        options = {'font': 'Cambria','fontsize': 10,'floatprecision': 5}
        config.apply_options(options, self.prediction_results_output)
        self.database_table.autoResizeColumns()
        self.prediction_results_output.show()

        #endregion

        #def writeResults():
        #    with pd.ExcelWriter('PredictionResults.xlsx') as writer: