import tkinter
import utilities
from tkinter import ttk

class Fereastra_nomenclator(tkinter.Toplevel):
    def __init__(self,master): # Constructorul clasei Fereastra_nomenclator (clasa care mosteneste TopLevel din Tkinter)
        super().__init__(master) # Initializarea clasei parinte (clasa Meniu Principal)
        self.title('Nomenclator') # Titlul ferestrei
        self.resizable(False, False) # Imposibilitate de redimensionare fereastra
        self.update_idletasks() # Asteapta initializarea completa a ferestrei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,625,450)) # Setam geometria si centrarea pe ecran
        
        # MODIFICARE STIL TAB-URI
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[5, 3], font=('TkDefaultFont', 8))

        # NOTEBOOK PENTRU A PUTEA PUNE TABURI IN FEREASTRA
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both',padx=5,pady=5)

        # ADAUGAREA FRAMEURILOR DEFINITE IN CLASE IN TABUL AFERENT FIECAREI OPERATIUNI
        self.frame_medici_curanti = MediciCuranti(self.notebook)
        self.frame_medici_trimitatori = MediciTrimitatori(self.notebook)

        # POZITIONARE EFECTIVA IN APLICATIE PENTRU TAB-URI
        self.notebook.add(self.frame_medici_curanti, text='Medici Curanti')
        self.notebook.add(self.frame_medici_trimitatori, text='Medici Trimitatori')





class MediciCuranti(ttk.Frame):
    def __init__(self, parinte):
        super().__init__(parinte)
        self.frame_date_medic = tkinter.Frame(self)
        self.frame_date_medic.grid(column=0, row=0,padx=(0,10),pady=(10,10))

        tkinter.Label(self.frame_date_medic,text='Nume: ').grid(column=0,row=0,pady=5)
        tkinter.Label(self.frame_date_medic,text='Prenume: ').grid(column=0,row=1,pady=5)
        tkinter.Label(self.frame_date_medic,text='Parafa: ').grid(column=0,row=2,pady=5)


        self.entry_nume = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_nume.grid(column=1,row=0,padx=5,pady=5)

        self.entry_prenume = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_prenume.grid(column=1,row=1,padx=5,pady=5)


        self.entry_parafa = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_parafa.grid(column=1,row=2,padx=5,pady=5)


        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=1,row=0,padx=(10,10),pady=(10,10))

        tkinter.Button(self.frame_butoane,text='Adaugare',width=25).grid(column=0,row=0,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare',width=25).grid(column=0,row=1,pady=5)
        tkinter.Button(self.frame_butoane,text='Incarcare nomenclator medici',width=25).grid(column=0,row=2,pady=5)


        coloane = ('IdMedic','Nume','Prenume','Parafa')
        self.tabel_medici_curanti = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_medici_curanti.heading(coloana,text=coloana,anchor='center')
            self.tabel_medici_curanti.column(coloana,width=125,anchor='center')

        self.tabel_medici_curanti.grid(column=0,row=1,columnspan=2,rowspan=2,padx=(50,10),pady=(10,10))




class MediciTrimitatori(ttk.Frame):
    def __init__(self, parinte):
        super().__init__(parinte)
        self.frame_date_medic = tkinter.Frame(self)
        self.frame_date_medic.grid(column=0, row=0,padx=(0,10),pady=(10,10))

        tkinter.Label(self.frame_date_medic,text='Nume: ').grid(column=0,row=0,pady=5)
        tkinter.Label(self.frame_date_medic,text='Prenume: ').grid(column=0,row=1,pady=5)
        tkinter.Label(self.frame_date_medic,text='Parafa: ').grid(column=0,row=2,pady=5)


        self.entry_nume = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_nume.grid(column=1,row=0,padx=5,pady=5)

        self.entry_prenume = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_prenume.grid(column=1,row=1,padx=5,pady=5)


        self.entry_parafa = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_parafa.grid(column=1,row=2,padx=5,pady=5)


        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=1,row=0,padx=(10,10),pady=(10,10))

        tkinter.Button(self.frame_butoane,text='Adaugare',width=25).grid(column=0,row=0,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare',width=25).grid(column=0,row=1,pady=5)
        tkinter.Button(self.frame_butoane,text='Incarcare nomenclator medici',width=25).grid(column=0,row=2,pady=5)


        coloane = ('IdMedic','Nume','Prenume','Parafa')
        self.tabel_medici_curanti = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_medici_curanti.heading(coloana,text=coloana,anchor='center')
            self.tabel_medici_curanti.column(coloana,width=125,anchor='center')

        self.tabel_medici_curanti.grid(column=0,row=1,columnspan=2,rowspan=2,padx=(50,10),pady=(10,10))
