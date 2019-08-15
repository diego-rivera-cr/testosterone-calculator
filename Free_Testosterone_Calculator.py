#Calculadora de testosterona libre

import math

class FreeTestosteroneCalculator:
    testosterone_conversion_dictionary = {
        "ng/dL" : 1,
        "ng/mL" : 100,
        "nmol/dL" : 288.4,
        "nmol/mL" : 28840,
        "nmol/L" : 28.84
    }
    
    albumin_conversion_dictionary = {
        "g/L" : 0.1,
        "g/dL" : 1
    }
    
    #constant, fron mol to nmol and viceversa
    kt = pow(10,9)
    
    
    def __init__(self, testosterone, testosterone_units, albumin, albumin_units, shbg):
        self.spawn(testosterone, testosterone_units, albumin, albumin_units, shbg)
    
    #method to init or respawn class with new data and calculations
    def spawn(self, testosterone, testosterone_units, albumin, albumin_units, shbg):
            self.correct_testosterone_units(testosterone, testosterone_units)
            self.correct_albumin_units(albumin, albumin_units)
            self.testosterone_molar()
            self.shbg = shbg
            self.shbg_molar(shbg)
            self.constant_factors()
            self.calculate_free_and_biovailable_testosterone()
    
    #use testosterone units as ng/mL
    def correct_testosterone_units(self, testosterone, units):
        self.testosterone = testosterone * self.testosterone_conversion_dictionary[units]
        self.testosterone_units = units
        
    #use testosterone units as g/dL
    def correct_albumin_units(self, albumin, units):
        self.albumin = albumin * self.albumin_conversion_dictionary[units]
        self.albumin_units = units
    
    #change testosterone to molar units
    def testosterone_molar(self):
        self.testosterone_molar_units = (self.testosterone/2.884) * pow(10,-10)
        
    #change SHBG to molar units
    def shbg_molar(self, shbg):
        self.shbg_molar_units = (shbg / 10) * pow(10,-8)
    
    
    def constant_factors(self):
        #testosterone bound to albumin
        self.f_a=((36000 * self.albumin *(1.45 * 0.0001))+1) * self.kt
        self.f_a1bumin = ((36000 * self.albumin *(1.45 * 0.0001))+1)
        #testosterone bound to SHBG
        self.f_b= self.kt *( self.shbg_molar_units - self.testosterone_molar_units) + self.f_a1bumin
        self.f_c = -(self.testosterone_molar_units)
        factor = (self.f_b * self.f_b)-(4 * self.f_a) * self.f_c
        self.wortel = math.sqrt(factor)
        self.f_testosterone = (-(self.f_b) + self.wortel)/( 2 * self.f_a)
        self.f_testosterone_p = (self.f_testosterone * 100)/self.testosterone_molar_units
        
        
    def calculate_free_and_biovailable_testosterone(self):
        #free calculated testosterone
        self.free_calculated_testosterone =(self.f_testosterone_p/100) * self.testosterone
        #bioavailable calculated testosterone
        self.bioavailable_testosterone = self.free_calculated_testosterone * self.f_a1bumin
        #correct free and bioavailable testosterone according to testosterone units
        if (self.testosterone_units=="ng/mL"):
            self.free_calculated_testosterone = self.free_calculated_testosterone/100
            self.bioavailable_testosterone=self.bioavailable_testosterone/100
        if (self.testosterone_units=="nmol/dL"):
            self.free_calculated_testosterone = self.free_calculated_testosterone * 0.00347
            self.bioavailable_testosterone = self.bioavailable_testosterone * 0.00347
        if (self.testosterone_units=="nmol/L"):
            self.free_calculated_testosterone = self.free_calculated_testosterone * 0.0347
            self.bioavailable_testosterone = self.bioavailable_testosterone * 0.0347
        if (self.testosterone_units=="nmol/mL"):
            self.free_calculated_testosterone = self.free_calculated_testosterone * 0.0000347
            self.bioavailable_testosterone = self.bioavailable_testosterone * 0.0000347
    
    
    def get_free_testosterone_ng_per_dL(self):
        return self.free_calculated_testosterone
        
    
    def get_free_testosterone_ng_per_dL_percentage(self):
        return self.free_calculated_testosterone/self.testosterone*100
        
        
    def get_free_testosterone_pg_per_mL(self):
        return self.free_calculated_testosterone*10
        
    
    def get_bioavailable_testosterone_ng_per_dL(self):
        return self.bioavailable_testosterone
        
        
    def get_bioavailable_testosterone_ng_per_dL_percentage(self):
        return self.bioavailable_testosterone/self.testosterone*100
        
        
    def get_free_androgen_index(self):
        FAI = 100*self.testosterone_molar_units/self.shbg_molar_units
        return FAI

def main():
    a = 42
    au = "g/L"
    t = 300
    tu = "ng/dL"
    s = 53
    calculator = FreeTestosteroneCalculator(t,tu,a,au,s)
    ft = calculator.get_free_testosterone_ng_per_dL()
    ftpgml = calculator.get_free_testosterone_pg_per_mL()
    ftp = calculator.get_free_testosterone_ng_per_dL_percentage()
    bt = calculator.get_bioavailable_testosterone_ng_per_dL()
    btp = calculator.get_bioavailable_testosterone_ng_per_dL_percentage()
    fai = calculator.get_free_androgen_index()
    print("Free Testosterone:", round(ft,1), " ng/dL ", round(ftpgml,1), " pg/mL ", round(ftp,2), "%")
    print("Bioavailable Testosterone:", round(bt,1), " ng/dL ", round(btp,2), "%")
    print("FAI: ", round(fai,2))
    return 0

if __name__ == '__main__':
    main()

