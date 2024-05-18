class Info():
    def __init__(self):
        #Beam auther, reference per auther and ID in database
        self.auther = ''
        self.autherReference = ''
        self.idInDatabase = 0

class Failure:
    def __init__(self):
        # Failure load and shear span
        self.P = 0
        self.a = 0
 
    def get_M(self):
        #Returns the failure moment for four-point bending
        return self.P * self.a / 2

class Concrete:
    def __init__(self):
        #Parameters for concrete material
        self.H = 0
        self.B = 0
        self.L = 0
        self.fc = 0
        self.Ec = 0

   
    def get_Ac(self):
        #Returns area of concrete
        return self.H * self.B

class Steel:
    def __init__(self):
        #Parameters for steel material
        self.fy = 0
        self.Es = 0
        self.As = 0
        self.Asc = 0
        self.dt = 0
        self.ds = 0
        self.Av = 0
        self.s = 0
        self.fyt = 0

class Fiber:
    def __init__(self):
        #Parameters for the FRP material
        self.n = 0
        self.Ef = 0
        self.ffu = 0
        self.lp = 0
        self.bf = 0
        self.df = 0
        self.tf = 0
        self.ap = 0
    
    def get_Af(self):
        #Returns total area of FRP
        return self.bf * self.tf * self.n
    def get_efu(self):
        #Returns ultimate FRP strain
        return self.ffu / self.Ef
    
class Beam():
    
    def __init__(self):
        #Beam ID in this code
        self.ID = 0
       
        #Unstrengthened nominal strength
        self.Mun = 0
        self.Cun = 0

        #Concrete strain and nuetral axis from equilibrium equations at failure
        self.ecf_exp = 0
        self.Cexp = 0
        self.efcd_exp = 0
        self.F_verified = True
        self.M_verified = True
        self.ecf_verified = True
        self.Mn_verified = True
 
        # The trilinear parameters to obtain M-ecft, M-phi
        # Cracking
        self.Mcr = 0
        self.Ccr = 0
        self.phi_cr = 0
        self.ecf_cr = 0

        # Yielding
        self.My = 0
        self.Cy = 0
        self.phi_y = 0
        self.ecf_y = 0

        # Ultimate
        self.Mn = 0
        self.Cn = 0
        self.phi_n = 0
        self.ecf_n = 0

        #Beam properties with respect to Concrete,Steel,Fiber,Epoxy,Failure
        self.Info = Info()
        self.loading = Failure()
        self.mat1 = Concrete()
        self.mat2 = Steel()
        self.mat3 = Fiber()

