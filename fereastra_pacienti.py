import tkinter
import utilities
from tkinter import ttk
from baza_de_date import *
from tkinter import messagebox


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
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,950,500)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei

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

        # asiguram sincronizarea refresh-ului intre tab-uri
        self.frame_date_pacient.internare_refresh(self.frame_internare.refresh_pacienti)

        # POZITIONARE EFECTIVA IN APLICATIE PENTRU TAB-URI
        self.notebook.add(self.frame_date_pacient, text='Date Pacient')
        self.notebook.add(self.frame_internare, text='Internare')
        self.notebook.add(self.frame_externare, text='Externare')

class DatePacient(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._refresh_internare = None
        # FRAME-UL CARE CONTINE DATELE PERSONALE ALE PACIENTULUI
        self.frame_date_personale = tkinter.Frame(self)
        self.frame_date_personale.grid(column=0, row=0, padx=45, pady=20)

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
        self.entry_data_nastere = tkinter.Entry(self.frame_date_personale,width=26)
        self.entry_data_nastere.grid(column=3,row=0,padx=5,pady=5)

        tkinter.Label(self.frame_date_personale,text='VARSTA: ').grid(column=2,row=1,padx=5,pady=5)
        self.entry_varsta = tkinter.Entry(self.frame_date_personale,width=26)
        self.entry_varsta.grid(column=3,row=1,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DATA DE NASTERE A PACIENTULUI
        tkinter.Label(self.frame_date_personale,text='SEX: ').grid(column=2,row=2,padx=5,pady=5)
        self.entry_sex = ttk.Combobox(self.frame_date_personale,values=['F','M'], state='readonly',width=23)
        self.entry_sex.grid(column=3,row=2,padx=5,pady=5)
        
        tkinter.Label(self.frame_date_personale, text='ASIGURAT: ').grid(column=0, row=4, padx=5, pady=5)

        self.asigurat_var = tkinter.IntVar()
        self.asigurat_checkbox = tkinter.Checkbutton(self.frame_date_personale, variable=self.asigurat_var)
        self.asigurat_checkbox.grid(column=1, row=4, padx=5, pady=5)


        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=2,row=0, padx=(10,5), pady=20)

        tkinter.Button(self.frame_butoane,text='Adaugare Pacient', command=lambda: self.adaugare_pacient()).grid(column=0,row=0,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare Pacient', command=lambda: self.modificare_pacient()).grid(column=0,row=1,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Stergere Pacient', command=lambda: self.stergere_pacient()).grid(column=1,row=0,padx=5,pady=5)


        coloane = ('IdPacient','Nume','Prenume','CNP','Data Nasterii', 'Varsta','Sex', 'Asigurat')
        self.tabel_pacient = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_pacient.heading(coloana,text=coloana,anchor='center')
            self.tabel_pacient.column(coloana,width=95,anchor='center')

        self.tabel_pacient.grid(column=0,row=1,columnspan=3,rowspan=2, padx=(35,5),pady=10)

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_pacient)

        self.refresh_pacienti()

    def internare_refresh(self, callback):
        """Set function used to refresh internare tab."""
        self._refresh_internare = callback

    def refresh_pacienti(self):
        
        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_pacienti():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

        if self._refresh_internare:
            self._refresh_internare()

    def adaugare_pacient(self):
        nume = self.entry_nume.get().strip()
        prenume = self.entry_prenume.get().strip()
        cnp = self.entry_cnp.get()
        data_nastere = self.entry_data_nastere.get().strip()
        varsta = self.entry_varsta.get().strip()
        sex = self.entry_sex.get()
        asigurat = self.asigurat_var.get()

        pacient_existent = verificare_existenta_pacient(cnp)

        if nume and prenume and cnp and data_nastere and varsta and sex :

            if len(cnp) == 13 and cnp.isdigit():

                if int(varsta) > 0 :

                    if pacient_existent:
                        intrebare = messagebox.askyesno('Validare operatie', 'Pacientul a mai fost internat in trecut. Doriti adaugarea unei noi internari?', parent = self)
                        
                        if intrebare:
                            insert_pacient(nume, prenume, cnp, data_nastere, varsta, sex, asigurat)
                            messagebox.showinfo('INFO', 'Pacientul a fost adaugat cu succes!', parent = self)

                    else:
                        insert_pacient(nume, prenume, cnp, data_nastere, varsta, sex, asigurat)
                        messagebox.showinfo('INFO', 'Pacientul a fost adaugat cu succes!', parent = self)

                else:

                    messagebox.showerror('EROARE', 'Verificati varsta pacientului!' , parent = self)

            else:

                messagebox.showerror('EROARE', 'Codul numeric personal trebuie sa contina 13 cifre!', parent = self)

        else:

            messagebox.showerror('EROARE', 'Introduceti toate datele necesare adaugarii pacientului', parent = self)

        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_cnp.delete(0, tkinter.END)
        self.entry_data_nastere.delete(0, tkinter.END)
        self.entry_varsta.delete(0, tkinter.END)
        self.entry_sex.set('')
        self.asigurat_var.set(int('0'))

        self.refresh_pacienti()

    def modificare_pacient(self):
        idpacient = self.id_pacient
        nume = self.entry_nume.get().strip()
        prenume = self.entry_prenume.get().strip()
        cnp = self.entry_cnp.get()
        data_nastere = self.entry_data_nastere.get().strip()
        varsta = self.entry_varsta.get().strip()
        sex = self.entry_sex.get()
        asigurat = self.asigurat_var.get()

        if nume and prenume and cnp and data_nastere and varsta and sex:
            
            if len(cnp) == 13 and cnp.isdigit():

                intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI', 'Confirmati modificarea datelor pentru pacientul selectat?', parent = self)

                if intrebare:

                    update_pacienti_date(nume, prenume, cnp, data_nastere, varsta, sex, asigurat, idpacient)
                    messagebox.showinfo('INFO','Datele au fost actualizate', parent = self)

                else:
                    messagebox.showwarning('AVERTIZARE','Datele nu au fost modificate', parent = self)
            
            else:

                messagebox.showerror('EROARE','Codul numeric personal trebuie sa contina 13 cifre!', parent=self)

        else:

            messagebox.showerror('EROARE','Verificati datele introduse', parent = self)

        # self.entry_nume.delete(0, tkinter.END)
        # self.entry_prenume.delete(0, tkinter.END)
        # self.entry_cnp.delete(0, tkinter.END)
        # self.entry_data_nastere.delete(0, tkinter.END)
        # self.entry_varsta.delete(0, tkinter.END)
        # self.entry_sex.set('')
        # self.asigurat_var.set(int('0'))

        self.refresh_pacienti()

    def stergere_pacient(self):
        idpacient = self.id_pacient

        if not verificare_existent_internare(idpacient):

            intrebare = messagebox.askyesno('CONFIRMARE STERGERE', 'Confirmati stergerea pacientului?', parent=self)

            if intrebare:
                stergere_pacient_date(idpacient)
                messagebox.showinfo('INFO', 'Pacientul a fost sters cu succes', parent = self)
            else:
                messagebox.showwarning('AVERTIZARE', 'Operatie de stergere anulata!', parent = self)
        else:
            messagebox.showerror('EROARE','Pacientul este internat! Operatiunea de stergere nu poate fi facuta', parent = self)
        
        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_cnp.delete(0, tkinter.END)
        self.entry_data_nastere.delete(0, tkinter.END)
        self.entry_varsta.delete(0, tkinter.END)
        self.entry_sex.set('')
        self.asigurat_var.set(int('0'))

        self.refresh_pacienti()

    def load_selected_pacient(self, event):
        selected =  self.tabel_pacient.selection()
        if selected:
            values = self.tabel_pacient.item(selected[0])["values"]

            self.id_pacient = values[0]

            self.entry_nume.delete(0, tkinter.END)
            self.entry_nume.insert(0, values[1])

            self.entry_prenume.delete(0, tkinter.END)
            self.entry_prenume.insert(0, values[2])

            self.entry_cnp.delete(0, tkinter.END)
            self.entry_cnp.insert(0, values[3])

            self.entry_data_nastere.delete(0, tkinter.END)
            self.entry_data_nastere.insert(0, values[4])

            self.entry_varsta.delete(0, tkinter.END)
            self.entry_varsta.insert(0, values[5])

            self.entry_sex.set(values[6])

            self.asigurat_var.set(values[7])

            
class Internare(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # FRAME-UL CARE CONTINE DATELE DE INTERNARE ALE PACIENTULUI
        self.frame_date_internare = tkinter.Frame(self)
        self.frame_date_internare.grid(column=0,row=0, padx=10, pady=10)
        
        # LABEL + ENTRY PENTRU MEDICUL TRIMITATOR
        tkinter.Label(self.frame_date_internare,text='MEDIC TRIMITATOR: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_medic_trimitator = ttk.Combobox(self.frame_date_internare, values=utilities.unpack_medici_trimitatori(), state='readonly', width=23)
        self.entry_medic_trimitator.grid(column=1, row=0, padx=5, pady=5)

        # LABEL + ENTRY PENTRU BILETUL DE TRIMITERE
        tkinter.Label(self.frame_date_internare,text='BILET TRIMITERE: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_bilet_trimitere = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_bilet_trimitere.grid(column=1,row=1,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTICUL PREZUMTIV
        tkinter.Label(self.frame_date_internare,text='DIAGNOSTIC PREZUMTIV: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_diagnostic_prezumtiv = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_diagnostic_prezumtiv.grid(column=1,row=2,padx=5,pady=5)

        # LABEL + ENTRY PENTRU MEDICUL CURANT
        tkinter.Label(self.frame_date_internare,text='MEDICUL CURANT: ').grid(column=0,row=4,padx=5,pady=5)
        self.entry_medic_curant = ttk.Combobox(self.frame_date_internare, values=utilities.unpack_medici(), state='readonly', width=23)
        self.entry_medic_curant.grid(column=1, row=4, padx=5, pady=5)

        # LABEL + ENTRY PENTRU SECTIA PE CARE VA FI INTERNAT PACIENTUL
        tkinter.Label(self.frame_date_internare,text='SECTIE: ').grid(column=0,row=5,padx=5,pady=5)
        self.entry_sectie = ttk.Combobox(self.frame_date_internare, values=utilities.unpack_sectii(), state='readonly',width=23)
        self.entry_sectie.grid(column=1, row=5, padx=5, pady=5)
        
        # FRAME-UL CARE CONTINE PREZENTAREA PACIENTULUI
        self.frame_prezentare_pacient = tkinter.Frame(self)
        self.frame_prezentare_pacient.grid(column=1,row=0, padx=10, pady=10)

        self.label_prezentare = tkinter.Label(self.frame_prezentare_pacient, text='', width=35, height=5)
        self.label_prezentare.grid(column=0,row=0,padx=10,pady=10)

        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=2,row=0,padx=10,pady=10)
        
        tkinter.Button(self.frame_butoane,text='Adaugare Internare', command=lambda: self.adaugare_internare()).grid(column=0,row=0,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare Internare', command=lambda: self.modificare_internare()).grid(column=0,row=1,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Stergere Internare', command=lambda: self.stergere_internare()).grid(column=1,row=0,padx=5,pady=5)

        coloane = ('IdPacient','Nume','Prenume','Medic Trimitator', 'Bilet Trimitere', 'Diagnostic P', 'Medic Curant', 'Sectie')
        self.tabel_pacient = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_pacient.heading(coloana,text=coloana,anchor='center')
            self.tabel_pacient.column(coloana,width=103,anchor='center')

        self.tabel_pacient.grid(column=0,row=1,columnspan=3,rowspan=2, padx=10,pady=10)

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_pacient)

        self.refresh_pacienti()

    def refresh_pacienti(self):
        
        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_pacienti_pentru_internare():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

    def adaugare_internare(self):
        idpacient = self.id_pacient
        medic_trimitator = self.entry_medic_trimitator.get()
        bilet_trimitere = self.entry_bilet_trimitere.get()
        diagnostic_prezumtiv = self.entry_diagnostic_prezumtiv.get()
        medic_curant = self.entry_medic_curant.get()
        sectie = self.entry_sectie.get()

        if medic_trimitator and bilet_trimitere and diagnostic_prezumtiv and medic_curant and sectie:

            update_pacienti_internare(medic_trimitator, bilet_trimitere, diagnostic_prezumtiv, medic_curant, sectie, idpacient)
            messagebox.showinfo('INFO','Internare adaugata cu succes!', parent = self)


        else:
            messagebox.showerror('EROARE','Nu ati completat toate datele necesare!', parent = self)

        self.entry_medic_trimitator.set('')
        self.entry_bilet_trimitere.delete(0, tkinter.END)
        self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
        self.entry_medic_curant.set('')
        self.entry_sectie.set('')
        
        self.refresh_pacienti()

    def modificare_internare(self):
        idpacient = self.id_pacient
        medic_trimitator = self.entry_medic_trimitator.get()
        bilet_trimitere = self.entry_bilet_trimitere.get()
        diagnostic_prezumtiv = self.entry_diagnostic_prezumtiv.get()
        medic_curant = self.entry_medic_curant.get()
        sectie = self.entry_sectie.get()

        if medic_trimitator and bilet_trimitere and diagnostic_prezumtiv and medic_curant and sectie:
            
            if not verificare_existent_externare(idpacient):

                update_pacienti_internare(medic_trimitator, bilet_trimitere, diagnostic_prezumtiv, medic_curant, sectie, idpacient)
                messagebox.showinfo('INFO','Internare modificata cu succes!', parent = self)

            else:

                messagebox.showerror('EROARE','Pacientul selectat a fost externat! Datele nu pot fi modificate', parent = self)

        else:
            messagebox.showerror('EROARE','Nu ati completat toate datele necesare!', parent = self)

        self.entry_medic_trimitator.set('')
        self.entry_bilet_trimitere.delete(0, tkinter.END)
        self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
        self.entry_medic_curant.set('')
        self.entry_sectie.set('')
        
        self.refresh_pacienti()

    def stergere_internare(self):
        idpacient = self.id_pacient

        if idpacient:

            if not verificare_existent_externare(idpacient):

                intrebare = messagebox.askyesno('CONFIRMARE STERGERE', 'Doriti stergerea internarii pentru pacientul selectat?' , parent = self)

                if intrebare:

                    stergere_internare(idpacient)
                    messagebox.showinfo('INFO', 'Internarea pacientului a fost stearsa cu succes!' , parent = self)

            else:
                
                messagebox.showerror('EROARE','Pacientul selectat a fost externat! Stergerea internarii nu este posibila', parent = self)

        else:

            messagebox.showerror('EROARE','Selectati un pacient din lista!', parent = self)

        self.entry_medic_trimitator.set('')
        self.entry_bilet_trimitere.delete(0, tkinter.END)
        self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
        self.entry_medic_curant.set('')
        self.entry_sectie.set('')
        
        self.refresh_pacienti()

    def prezentare_pacient(self, idpacient):
        pacient_selectat = get_pacient_pentru_prezentare(idpacient)
        self.label_prezentare.config(text=f'PACIENTUL\nNume: {pacient_selectat[0]}\nPrenume: {pacient_selectat[1]}\nCNP: {pacient_selectat[2]}\nData nastere: {pacient_selectat[3]}\nSex: {pacient_selectat[4]}\nStatus: {pacient_selectat[5]}')
       
    def load_selected_pacient(self, event):
        selected =  self.tabel_pacient.selection()
        if selected:
            values = self.tabel_pacient.item(selected[0])["values"]
            self.id_pacient = values[0]

            self.entry_medic_trimitator.set(values[3])
            
            self.entry_bilet_trimitere.delete(0, tkinter.END)
            self.entry_bilet_trimitere.insert(0, values[4])

            self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
            self.entry_diagnostic_prezumtiv.insert(0, values[5])
            
            self.entry_medic_curant.set(values[6])
            self.entry_sectie.set(values[7])

            self.prezentare_pacient(self.id_pacient)



class Externare(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # FRAME-UL CARE CONTINE DATELE PERSONALE ALE PACIENTULUI
        self.frame_date_externare = tkinter.Frame(self)
        self.frame_date_externare.grid(column=0, row=0, padx=(10,20), pady=(10,10))

        # LABEL + ENTRY PENTRU DIAGNOSTIC INITIAL
        tkinter.Label(self.frame_date_externare,text='DATA EXTERNARII: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_data_externarii = tkinter.Entry(self.frame_date_externare, width=26)
        self.entry_data_externarii.grid(column=1,row=0,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTIC INITIAL
        tkinter.Label(self.frame_date_externare,text='DIAGNOSTIC CONFIRMAT: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_diagnostic = tkinter.Entry(self.frame_date_externare, width=26)
        self.entry_diagnostic.grid(column=1,row=0,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTIC INITIAL
        tkinter.Label(self.frame_date_externare,text='ALOCATIE DE HRANA: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_alocatie_hrana = ttk.Combobox(self.frame_date_externare,values=['Alocatie1', 'Alocatie2'],state='readonly', width=24)
        self.entry_alocatie_hrana.grid(column=1,row=1,padx=5,pady=5)

        tkinter.Label(self.frame_date_externare, text='SERVICII EFECTUATE: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_servicii_efectuate = ttk.Combobox(self.frame_date_externare,values=['Alocatie1', 'Alocatie2'],state='readonly', width=24)
        self.entry_servicii_efectuate.grid(column=1,row=2,padx=5,pady=5)

        self.frame_text = tkinter.Frame(self)
        self.frame_text.grid(column=0, row=1, padx=(10, 20), pady=(10, 10))

        tkinter.Label(self.frame_text, text='RECOMANDARI:').pack(anchor='center', padx=10,pady=10)
        self.text_recomandari = tkinter.Text(self.frame_text, width=40, height=7)
        self.text_recomandari.pack()

        tkinter.Label(self.frame_text, text='PLAN DE TRATAMENT:').pack(anchor='center', padx=10,pady=10)
        self.text_plan_tratament = tkinter.Text(self.frame_text, width=40, height=7)
        self.text_plan_tratament.pack()
