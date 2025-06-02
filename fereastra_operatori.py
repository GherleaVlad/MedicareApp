import tkinter
import utilities
from tkinter import ttk

'''
Modulul fereastra_operatori este folosit pentru creare, editarea sau stergerea operatorilor existenti in aplicatie.
'''

class FereastraOperatori(tkinter.Toplevel):
    def __init__(self, master): # Initializare constructor pentru clasa Fereastra Operatori (reprezinta tkinter.TopLevel - clasa copil pentru tkinter.Tk)
        super().__init__(master) # Initializare constructor pentru clasa parinte (adica pentru clasa MeniuPrincipal - care reprezinta tkinter.Tk (clasa principala - radacina))
        self.title('Operatori') # Numele ferestrei
        self.resizable(False, False) # Dimensiunea nu este modificabila
        self.update_idletasks() # Asteapta initializarea completa a aplicatiei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,975,300)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei

        frame_tabel = tkinter.Frame(self)
        frame_tabel.grid(column=1,row=0,padx=(20,20),pady=(20,20))
        
        frame_date = tkinter.Frame(self)
        frame_date.grid(column=0,row=0,padx=(20,20),pady=(20,5))

        coloane = ('IdOperator', 'Utilizator', 'Parola','Nume', 'Prenume', 'Sectie')
        tabel_pacient = ttk.Treeview(frame_tabel, columns=coloane, show='headings',height=11)

        for coloana in coloane:
            tabel_pacient.heading(coloana,text=coloana)
            tabel_pacient.column(coloana,width=90)

        tabel_pacient.pack()
        
        # Butoane si Entry-uri pentru introducere operator

        tkinter.Button(frame_date,text='INCARCA UTILIZATORI',width=25, relief='groove').grid(column=0,row=0,padx=5,pady=5,columnspan=2)

        # Entry si label pentru utilizator
        tkinter.Label(frame_date,text='UTILIZATOR: ').grid(column=0,row=1,padx=5,pady=5)
        entry_utilizator = tkinter.Entry(frame_date, width=26)
        entry_utilizator.grid(column=1,row=1,padx=5,pady=5)

        # Entry si label pentru nume utilizator
        tkinter.Label(frame_date,text='NUME: ').grid(column=0,row=2,padx=5,pady=5)
        entry_nume = tkinter.Entry(frame_date, width=26)
        entry_nume.grid(column=1,row=2,padx=5,pady=5)
        
        # Entry si label pentru prenume utilizator
        tkinter.Label(frame_date,text='PRENUME: ').grid(column=0,row=3,padx=5,pady=5)
        entry_prenume = tkinter.Entry(frame_date, width=26)
        entry_prenume.grid(column=1,row=3,padx=5,pady=5)
        
        # Entry si label pentru sectie utilizator
        tkinter.Label(frame_date,text='SECTIE: ').grid(column=0,row=4,padx=5,pady=5)
        entry_prenume = ttk.Combobox(frame_date,values=['Sectie1','Sectie2'], state='readonly', width=23)
        entry_prenume.grid(column=1,row=4,padx=5,pady=5)
        
        # Entry si label pentru parola utilizator
        tkinter.Label(frame_date,text='PAROLA: ').grid(column=0,row=5,padx=5,pady=5)
        entry_prenume = tkinter.Entry(frame_date, width=26)
        entry_prenume.grid(column=1,row=5,padx=5,pady=5)

        tkinter.Button(frame_date,text='SALVARE',width=21).grid(column=0,row=6,padx=5,pady=3)
        tkinter.Button(frame_date,text='ACTUALIZARE',width=21).grid(column=1,row=6,padx=3,pady=5)




