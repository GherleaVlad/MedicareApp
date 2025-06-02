import tkinter
import utilities
from tkinter import ttk

'''
Modulul fereastra_sectii este destinat adaugarii/editarii sectiilor existente in program.
Atentie! Modificarea sau stergerea unei sectii este posibila doar daca nu a fost folosita, adica daca nu este atribuita unui utilizator din baza de date.
'''

class FereastraSectii(tkinter.Toplevel):
    def __init__(self, master): # Initializare constructor pentru clasa Fereastra Sectii (reprezinta tkinter.TopLevel - clasa copil pentru tkinter.Tk)
        super().__init__(master) # Initializare constructor pentru clasa parinte (adica pentru clasa MeniuPrincipal - care reprezinta tkinter.Tk (clasa principala - radacina))
        self.title('Sectii') # Numele ferestrei
        self.resizable(False, False) # Dimensiunea nu este modificabila
        self.update_idletasks() # Asteapta initializarea completa a aplicatiei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,800,350)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei


        frame_tabel = tkinter.Frame(self)
        frame_tabel.grid(column=1,row=0,padx=(20,20),pady=(20,20))
        
        frame_date = tkinter.Frame(self)
        frame_date.grid(column=0,row=0,padx=(20,20),pady=(20,5))

        coloane = ('IdSectie', 'Denumire','Medic Sef Sectie')
        tabel_pacient = ttk.Treeview(frame_tabel, columns=coloane, show='headings')

        for coloana in coloane:
            tabel_pacient.heading(coloana,text=coloana)
            tabel_pacient.column(coloana,width=120)

        tabel_pacient.pack()
        
        # Butoane si Entry-uri pentru introducere operator

        tkinter.Button(frame_date,text='INCARCA SECTII',width=25, relief='groove').grid(column=0,row=0,padx=5,pady=5,columnspan=2)

        # Entry si label pentru sectie
        tkinter.Label(frame_date,text='SECTIE: ').grid(column=0,row=1,padx=5,pady=5)
        entry_sectie = tkinter.Entry(frame_date, width=26)
        entry_sectie.grid(column=1,row=1,padx=5,pady=5)

        # Entry si label pentru medic sef de sectie
        tkinter.Label(frame_date,text='SEF SECTIE: ').grid(column=0,row=2,padx=5,pady=5)
        entry_sef_sectie = ttk.Combobox(frame_date, values=['Sectie1','Sectie2'], state='readonly', width=23)
        entry_sef_sectie.grid(column=1,row=2,padx=5,pady=5)
        
        tkinter.Button(frame_date,text='SALVARE',width=21).grid(column=0,row=3,padx=5,pady=3)
        tkinter.Button(frame_date,text='ACTUALIZARE',width=21).grid(column=1,row=3,padx=3,pady=5)

    def adaugare_sectie(self):
        pass
