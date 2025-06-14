import tkinter
import utilities
from tkinter import ttk
from datetime import datetime, date
from baza_de_date import insert_pacient, get_pacienti, update_pacienti, verificare_existenta_pacient
from tkinter import messagebox
from tkcalendar import DateEntry


'''
Modulul Fereastra pacientii contine clasele FereastraPacient si notebook-urile acesteia DatePacient, Internare, Externare
Notebook-urile reprezinta taburile din fereastra pacient care ne permite adaugarea, stergerea, modificarea unui pacient cat si a datelor privind internarea si externarea acestuia
'''

class FereastraPacient(tkinter.Toplevel):
    def __init__(self, master): # Initializare constructor pentru clasa Fereastra Pacient (reprezinta tkinter.TopLevel - clasa copil pentru tkinter.Tk)
        super().__init__(master) # Initializare constructor pentru clasa parinte (adica pentru clasa MeniuPrincipal - care reprezinta tkinter.Tk (clasa principala - radacina))
        self.title('Pacient') # Numele ferestrei
        self.resizable(False, False) # Dimensiunea nu este modificabila
        self.update_idletasks() # Asteapta initializarea completa a aplicatiei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,850,550)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei

        # MODIFICARE STIL TAB-URI
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[5, 3], font=('TkDefaultFont', 8))

        # NOTEBOOK PENTRU A PUTEA PUNE TABURI IN FEREASTRA
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both',padx=5,pady=5)

        # ADAUGAREA FRAMEURILOR DEFINITE IN CLASE IN TABUL AFERENT FIECAREI OPERATIUNI
        self.frame_date_pacient = DatePacient(self.notebook)
        self.frame_internare = Internare(self.notebook)
        self.frame_externare = Externare(self.notebook)

        # POZITIONARE EFECTIVA IN APLICATIE PENTRU TAB-URI
        self.notebook.add(self.frame_date_pacient, text='Date Pacient')
        self.notebook.add(self.frame_internare, text='Internare')
        self.notebook.add(self.frame_externare, text='Externare')

class DatePacient(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # FRAME-UL CARE CONTINE DATELE PERSONALE ALE PACIENTULUI
        self.frame_date_personale = tkinter.Frame(self)
        self.frame_date_personale.grid(column=0, row=0, padx=(10,10), pady=(10,10))


        # LABEL + ENTRY PENTRU NUMELE PACIENTULUI
        tkinter.Label(self.frame_date_personale,text='NUME: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_nume = tkinter.Entry(self.frame_date_personale,width=26)
        self.entry_nume.grid(column=1,row=0,padx=5,pady=5)

        # LABEL + ENTRY PENTRU PRENUMELE PACIENTULUI
        tkinter.Label(self.frame_date_personale,text='PRENUME: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_prenume = tkinter.Entry(self.frame_date_personale,width=26)
        self.entry_prenume.grid(column=1,row=1,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DATA DE NASTERE A PACIENTULUI
        tkinter.Label(self.frame_date_personale,text='CNP: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_cnp = tkinter.Entry(self.frame_date_personale,width=26)
        self.entry_cnp.grid(column=1,row=2,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DATA DE NASTERE A PACIENTULUI
        tkinter.Label(self.frame_date_personale,text='DATA NASTERE: ').grid(column=2,row=0,padx=5,pady=5)
        self.entry_varsta = DateEntry(self.frame_date_personale,width=23, date_pattern='dd.mm.yyyy')
        self.entry_varsta.grid(column=3,row=0,padx=5,pady=5)

        self.varsta_pacient = None
        tkinter.Button(self.frame_date_personale, text='V', command= lambda: self.calcul_varsta()).grid(column=4, row=0, padx=2, pady=2)

        # LABEL PENTRU VARSTA PACIENTULUI (CALCULATA AUTOMAT IN FUNCTIE DE VARSTA)
        tkinter.Label(self.frame_date_personale,text='VARSTA: ').grid(column=2,row=1,padx=5,pady=5)
        self.label_varsta = tkinter.Label(self.frame_date_personale,text='')
        self.label_varsta.grid(column=3,row=1,padx=5,pady=5)


        # LABEL + ENTRY PENTRU DATA DE NASTERE A PACIENTULUI
        tkinter.Label(self.frame_date_personale,text='SEX: ').grid(column=2,row=2,padx=5,pady=5)
        self.entry_sex = ttk.Combobox(self.frame_date_personale,values=['F','M'], state='readonly',width=23)
        self.entry_sex.grid(column=3,row=2,padx=5,pady=5)
        
        tkinter.Label(self.frame_date_personale, text='ASIGURAT: ').grid(column=0, row=4, padx=5, pady=5)

        self.asigurat_var = tkinter.IntVar()
        self.asigurat_checkbox = tkinter.Checkbutton(self.frame_date_personale, variable=self.asigurat_var)
        self.asigurat_checkbox.grid(column=1, row=4, padx=5, pady=5)


        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=2,row=0, padx=10, pady=(10,10))

        tkinter.Button(self.frame_butoane,text='Adaugare Pacient', command=lambda: self.adaugare_pacient()).grid(column=0,row=0,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare Pacient').grid(column=0,row=1,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Stergere Pacient').grid(column=1,row=0,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Cautare Pacient').grid(column=1,row=1,padx=5,pady=5)
        

        coloane = ('IdPacient','Nume','Prenume','Data Nasterii','Varsta','CNP','Sex', 'Asigurat')
        self.tabel_pacient = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_pacient.heading(coloana,text=coloana,anchor='center')
            self.tabel_pacient.column(coloana,width=81,anchor='center')

        self.tabel_pacient.grid(column=0,row=1,columnspan=3,rowspan=2, pady=(10,10))

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_pacient)

        self.refresh_pacienti()

    def refresh_pacienti(self):
        
        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_pacienti():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

    def adaugare_pacient(self):
        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()
        cnp = self.entry_cnp.get()
        data_nastere = self.entry_varsta.get_date()
        varsta = self.varsta
        sex = self.entry_sex.get()
        asigurat = self.asigurat_var.get()

        pacient_existent = verificare_existenta_pacient(cnp)

        if pacient_existent:
            intrebare = messagebox.askyesno('Validare operatie', 'Pacientul a mai fost internat in trecut. Doriti adaugarea unei noi internari?', parent = self)
            
            if intrebare:
                insert_pacient(nume, prenume, data_nastere, varsta, cnp, sex, asigurat)
                messagebox.showinfo('INFO', 'Pacientul a fost adaugat cu succes!', parent = self)


        else:
            insert_pacient(nume, prenume, data_nastere, varsta, cnp, sex, asigurat)
            messagebox.showinfo('INFO', 'Pacientul a fost adaugat cu succes!', parent = self)

        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_cnp.delete(0, tkinter.END)
        self.entry_varsta.set_date(date.today())
        self.entry_sex.set('')
        self.asigurat_var.set(int('0'))

        self.refresh_pacienti()

    def calcul_varsta(self):
        data_nastere = self.entry_varsta.get_date()
        data_curenta = datetime.today()
        self.varsta = data_curenta.year - data_nastere.year
        self.label_varsta.config(text=f'{self.varsta} ANI')

    def modificare_pacient(self):
        pass

    def stergere_pacient(self):
        pass

    def cautare_pacient(self):
        pass
    
    def load_selected_pacient(self, event):
        selected =  self.tabel_pacient.selection()
        if selected:
            values = self.tabel_pacient.item(selected[0])["values"]

            self.id_pacient = values[0]

            self.entry_nume.delete(0, tkinter.END)
            self.entry_nume.insert(0, values[1])

            self.entry_prenume.delete(0, tkinter.END)
            self.entry_prenume.insert(0, values[2])

            self.entry_varsta.set_date(values[3])

            self.label_varsta.config(text=values[4])

            self.entry_cnp.delete(0, tkinter.END)
            self.entry_cnp.insert(0, values[5])

            self.entry_sex.delete(0, tkinter.END)
            self.entry_sex.insert(0, values[6])

            self.asigurat_var.set(int(values[7]))








class Internare(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # FRAME-UL CARE CONTINE DATELE PERSONALE ALE PACIENTULUI

        # FRAME-UL CARE CONTINE DATELE DE INTERNARE ALE PACIENTULUI
        self.frame_date_internare = tkinter.Frame(self)
        self.frame_date_internare.grid(column=1,row=0, padx=(20,10), pady=(10,10))

        # LABEL + ENTRY PENTRU SECTIA PE CARE VA FI INTERNAT PACIENTUL
        tkinter.Label(self.frame_date_internare,text='SECTIE: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_sectie = ttk.Combobox(self.frame_date_internare, values=['Sectia1','Sectia2'], state='readonly',width=23)
        self.entry_sectie.grid(column=1, row=0, padx=5, pady=5)
        
        # LABEL + ENTRY PENTRU MEDICUL TRIMITATOR
        tkinter.Label(self.frame_date_internare,text='MEDIC TRIMITATOR: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_medic_trimitator = ttk.Combobox(self.frame_date_internare, values=['Sectia1','Sectia2'], state='readonly', width=23)
        self.entry_medic_trimitator.grid(column=1, row=1, padx=5, pady=5)

        # LABEL + ENTRY PENTRU BILETUL DE TRIMITERE
        tkinter.Label(self.frame_date_internare,text='BILET TRIMITERE: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_bilet_trimitere = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_bilet_trimitere.grid(column=1,row=2,padx=5,pady=5)

        # LABEL + ENTRY PENTRU MEDICUL CURANT
        tkinter.Label(self.frame_date_internare,text='MEDICUL CURANT: ').grid(column=0,row=3,padx=5,pady=5)
        self.entry_medic_curant = ttk.Combobox(self.frame_date_internare, values=['Medic1','Medic2'], state='readonly', width=23)
        self.entry_medic_curant.grid(column=1, row=3, padx=5, pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTIC INITIAL
        tkinter.Label(self.frame_date_internare,text='DIAGNOSTIC: ').grid(column=0,row=4,padx=5,pady=5)
        self.entry_diagnostic = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_diagnostic.grid(column=1,row=4,padx=5,pady=5)


class Externare(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # FRAME-UL CARE CONTINE DATELE PERSONALE ALE PACIENTULUI
        self.frame_date_personale = tkinter.Frame(self)
        self.frame_date_personale.grid(column=0, row=0, padx=(10,20), pady=(10,10))
