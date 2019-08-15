try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
from Free_Testosterone_Calculator import FreeTestosteroneCalculator
from pprint import pprint
from _tkinter import TclError


class TestosteroneCalculatorApp:
    def __init__(self, master):
        #1: Crea un constructor
        self.builder = builder = pygubu.Builder()
        #2: Carga un archivo con el diseño de la interfaz
        builder.add_from_file('testo_app_ui.ui')
        #3: Crea el widget usando 'master' como padre
        self.mainwindow = builder.get_object('Testosterona', master)
        # Configure callbacks
        builder.connect_callbacks(self)
    
    def calculate(self):
        try:
            data = self.get_data()
            pprint(data)
            self.set_calculator(data)
            calculations = self.testosterone_calculate(data)
            pprint(calculations)
            self.set_variable_data('fai',calculations['fai'])
            self.set_variable_data('ft',calculations['ftpgml'])
            self.set_variable_data('ftu',calculations['ftpgmlu'])
            self.set_variable_data('ftp',(str(calculations['ftp'])+'%'))
            self.set_variable_data('bt',calculations['bt'])
            self.set_variable_data('btu',calculations['btu'])
            self.set_variable_data('btp',(str(calculations['btp'])+'%'))
        except TclError as te:
            print(te)
        except KeyError as ke:
            print(ke)
            
    
    def set_calculator(self, data):
        t = data['testosterone']
        tu = data['testosterone_units']
        a = data['albumin']
        au = data['albumin_units']
        s = data['shbg']
        self.calculator = FreeTestosteroneCalculator(t,tu,a,au,s)
        
    def testosterone_calculate(self, data):
        t = data['testosterone']
        tu = data['testosterone_units']
        a = data['albumin']
        au = data['albumin_units']
        s = data['shbg']
        self.calculator.spawn(t,tu,a,au,s)
        calculations = dict(
            ft = round(self.calculator.get_free_testosterone_ng_per_dL(),2),
            ftpgml = round(self.calculator.get_free_testosterone_pg_per_mL(),1),
            ftu = 'ng/dL',
            ftpgmlu = 'pg/mL',
            ftp = round(self.calculator.get_free_testosterone_ng_per_dL_percentage(),2),
            bt = round(self.calculator.get_bioavailable_testosterone_ng_per_dL(),1),
            btp = round(self.calculator.get_bioavailable_testosterone_ng_per_dL_percentage(),1),
            btu = 'ng/dL',
            fai = round(self.calculator.get_free_androgen_index(),1),
            )
        return calculations
     
    
    def get_data(self):
        data = dict(
                testosterone = self.get_variable_data('testosterone'),
                testosterone_units = self.get_variable_data('testosterone_units'),
                shbg = self.get_variable_data('shbg'),
                shbg_units = self.get_variable_data('shbg_units'),
                albumin = self.get_variable_data('albumin'),
                albumin_units = self.get_variable_data('albumin_units')
                )
        return data
    
    def get_variable_data(self, variable_name):
        return self.builder.tkvariables.__getitem__(variable_name).get()
        
    
    def set_variable_data(self, variable_name, data):
        self.builder.tkvariables.__getitem__(variable_name).set(data)

def main():
    root = tk.Tk()
    app = TestosteroneCalculatorApp(root)
    root.title("Testosterona libre")
    root.iconbitmap("calculator.ico")
    root.fg = "black"
    root.mainloop()
    return 0

if __name__ == '__main__':
    main()

