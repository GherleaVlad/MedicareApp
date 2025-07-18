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
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,960,500)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei
        self.iconbitmap(utilities.get_icon_path())  # Setam iconita aplicatiei        
        
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
        self.frame_date_pacient.externare_refresh(self.frame_externare.refresh_pacienti)


        # POZITIONARE EFECTIVA IN APLICATIE PENTRU TAB-URI
        self.notebook.add(self.frame_date_pacient, text='Date Pacient')
        self.notebook.add(self.frame_internare, text='Internare')
        self.notebook.add(self.frame_externare, text='Externare')

class DatePacient(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.id_pacient = None
        self._refresh_internare = None
        self._refresh_externare = None
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

        self.tabel_pacient.grid(column=0,row=1,columnspan=3,rowspan=2, padx=(45,5),pady=10)

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_pacient)

        self.refresh_pacienti()

    def internare_refresh(self, callback):
        """Set function used to refresh internare tab."""
        self._refresh_internare = callback

    def externare_refresh(self, callback):
        """Set function used to refresh externare tab."""
        self._refresh_externare = callback

    def refresh_pacienti(self):
        """
        Reîncarcă tabelul cu pacienți din baza de date.
        Șterge toate rândurile existente și inserează datele actualizate.
        Apelează funcțiile de refresh pentru tab-urile de internare și externare dacă sunt setate.
        """
        
        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_pacienti():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

        if self._refresh_internare:
            self._refresh_internare()

        if self._refresh_externare:
            self._refresh_externare()

    def adaugare_pacient(self):
        """
        Adaugă un pacient nou în baza de date pe baza datelor introduse în câmpurile formularului.
        Verifică dacă toate câmpurile obligatorii sunt completate și dacă pacientul cu CNP-ul respectiv nu există deja.
        Dacă datele sunt valide și pacientul nu există, îl adaugă în baza de date și afișează un mesaj de succes.
        În caz contrar, afișează un mesaj de eroare corespunzător.
        La final, resetează câmpurile formularului și actualizează lista pacienților.
        """

        nume = self.entry_nume.get().title().strip()
        prenume = self.entry_prenume.get().title().strip()
        cnp = self.entry_cnp.get().strip()
        data_nastere = self.entry_data_nastere.get().strip()
        varsta = self.entry_varsta.get().strip()
        sex = self.entry_sex.get()
        asigurat = self.asigurat_var.get()

        pacient_existent = verificare_existenta_pacient(cnp)

        if nume and prenume and cnp and data_nastere and varsta and sex :

            if len(cnp) == 13 and cnp.isdigit():

                if varsta.isdigit() and int(varsta) > 0 :

                    if pacient_existent:
                        intrebare = messagebox.askyesno('Validare operatie', 'Pacientul a mai fost internat in trecut. Doriti adaugarea unei noi internari?', parent = self)
                        
                        if intrebare:
                            insert_pacient(nume, prenume, cnp, data_nastere, varsta, sex, asigurat)
                            messagebox.showinfo('INFO', 'Pacientul a fost adaugat cu succes!', parent = self)

                            self.entry_nume.delete(0, tkinter.END)
                            self.entry_prenume.delete(0, tkinter.END)
                            self.entry_cnp.delete(0, tkinter.END)
                            self.entry_data_nastere.delete(0, tkinter.END)
                            self.entry_varsta.delete(0, tkinter.END)
                            self.entry_sex.set('')
                            self.asigurat_var.set(int('0'))

                    else:
                        insert_pacient(nume, prenume, cnp, data_nastere, varsta, sex, asigurat)
                        messagebox.showinfo('INFO', 'Pacientul a fost adaugat cu succes!', parent = self)
                        
                        self.entry_nume.delete(0, tkinter.END)
                        self.entry_prenume.delete(0, tkinter.END)
                        self.entry_cnp.delete(0, tkinter.END)
                        self.entry_data_nastere.delete(0, tkinter.END)
                        self.entry_varsta.delete(0, tkinter.END)
                        self.entry_sex.set('')
                        self.asigurat_var.set(int('0'))

                else:

                    messagebox.showerror('EROARE', 'Verificati varsta pacientului!' , parent = self)

            else:

                messagebox.showerror('EROARE', 'Codul numeric personal trebuie sa contina 13 cifre!', parent = self)

        else:

            messagebox.showerror('EROARE', 'Introduceti toate datele necesare adaugarii pacientului', parent = self)

        self.refresh_pacienti()

    def modificare_pacient(self):
        """
        Modifică datele pacientului selectat din tabel.
        Verifică dacă toate câmpurile sunt completate și dacă pacientul nu este internat.
        Dacă utilizatorul confirmă modificarea, actualizează datele pacientului și afișează un mesaj de succes.
        În caz contrar, afișează un mesaj de avertizare sau eroare.
        La final, resetează câmpurile formularului și actualizează lista pacienților.
        """        
        
        idpacient = self.id_pacient
        nume = self.entry_nume.get().title().strip()
        prenume = self.entry_prenume.get().title().strip()
        cnp = self.entry_cnp.get().strip()
        data_nastere = self.entry_data_nastere.get().strip()
        varsta = self.entry_varsta.get().strip()
        sex = self.entry_sex.get()
        asigurat = self.asigurat_var.get()

        if nume and prenume and cnp and data_nastere and varsta and sex:
            
            if not verificare_existent_internare(idpacient):


                if len(cnp) == 13 and cnp.isdigit():

                    intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI', 'Confirmati modificarea datelor pentru pacientul selectat?', parent = self)

                    if intrebare:

                        update_pacienti_date(nume, prenume, cnp, data_nastere, varsta, sex, asigurat, idpacient)
                        messagebox.showinfo('INFO','Datele au fost actualizate', parent = self)

                    else:
                        messagebox.showwarning('AVERTIZARE','Datele nu au fost modificate', parent = self)
        
                        self.entry_nume.delete(0, tkinter.END)
                        self.entry_prenume.delete(0, tkinter.END)
                        self.entry_cnp.delete(0, tkinter.END)
                        self.entry_data_nastere.delete(0, tkinter.END)
                        self.entry_varsta.delete(0, tkinter.END)
                        self.entry_sex.set('')
                        self.asigurat_var.set(int('0'))
                
                else:

                    messagebox.showerror('EROARE','Codul numeric personal trebuie sa contina 13 cifre!', parent=self)

            else:

                messagebox.showerror('EROARE','Pacientul este internat! Datele nu pot fi modificate.', parent=self)
        else:

            messagebox.showerror('EROARE','Verificati datele introduse!', parent = self)

        self.refresh_pacienti()

    def stergere_pacient(self):
        """
        Șterge pacientul selectat din tabel și din baza de date.
        Verifică dacă pacientul nu este internat înainte de ștergere.
        Dacă nu este internat, cere confirmarea utilizatorului și șterge pacientul.
        Afișează mesaje informative sau de eroare după caz.
        La final, resetează câmpurile formularului și actualizează lista pacienților.
        """        
        
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
        """
        Încarcă datele pacientului selectat din tabel în câmpurile formularului pentru editare.
        Setează id-ul pacientului pentru operațiuni ulterioare (modificare/ștergere).
        """        
        
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
        self.id_pacient = None

        # FRAME-UL CARE CONTINE DATELE DE INTERNARE ALE PACIENTULUI
        self.frame_date_internare = tkinter.Frame(self)
        self.frame_date_internare.grid(column=0,row=0, padx=10, pady=10)
        
        # LABEL + ENTRY PENTRU MEDICUL TRIMITATOR
        tkinter.Label(self.frame_date_internare,text='DATA INTERNARE: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_data_internare = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_data_internare.grid(column=1, row=0, padx=5, pady=5)

        # LABEL + ENTRY PENTRU MEDICUL TRIMITATOR
        tkinter.Label(self.frame_date_internare,text='MEDIC TRIMITATOR: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_medic_trimitator = ttk.Combobox(self.frame_date_internare, values=utilities.unpack_medici_trimitatori(), state='readonly', width=23)
        self.entry_medic_trimitator.grid(column=1, row=1, padx=5, pady=5)

        # LABEL + ENTRY PENTRU BILETUL DE TRIMITERE
        tkinter.Label(self.frame_date_internare,text='BILET TRIMITERE: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_bilet_trimitere = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_bilet_trimitere.grid(column=1,row=2,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTICUL PREZUMTIV
        tkinter.Label(self.frame_date_internare,text='DIAGNOSTIC PREZUMTIV: ').grid(column=0,row=3,padx=5,pady=5)
        self.entry_diagnostic_prezumtiv = tkinter.Entry(self.frame_date_internare, width=26)
        self.entry_diagnostic_prezumtiv.grid(column=1,row=3,padx=5,pady=5)

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

        self.label_prezentare = tkinter.Label(self.frame_prezentare_pacient, text='', width=35, height=6)
        self.label_prezentare.grid(column=0,row=0,padx=10,pady=10)

        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=2,row=0,padx=10,pady=10)
        
        tkinter.Button(self.frame_butoane,text='Adaugare Internare', command=lambda: self.adaugare_internare()).grid(column=0,row=0,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare Internare', command=lambda: self.modificare_internare()).grid(column=0,row=1,padx=5,pady=5)
        tkinter.Button(self.frame_butoane,text='Stergere Internare', command=lambda: self.stergere_internare()).grid(column=1,row=0,padx=5,pady=5)

        coloane = ('IdPacient', 'Nume', 'Prenume', 'Data Internare', 'Medic Trimitator', 'Bilet Trimitere', 'Diagnostic P', 'Medic Curant', 'Sectie')
        self.tabel_pacient = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_pacient.heading(coloana,text=coloana,anchor='center')
            self.tabel_pacient.column(coloana,width=103,anchor='center')

        self.tabel_pacient.grid(column=0,row=1,columnspan=3,rowspan=2, padx=10,pady=10)

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_pacient)

        self.refresh_pacienti()

    def refresh_pacienti(self):
        """
        Reîncarcă tabelul cu pacienți internați din baza de date.
        Șterge toate rândurile existente și inserează datele actualizate.
        """

        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_pacienti_internare():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

    def adaugare_internare(self):
        """
        Adaugă o internare nouă pentru pacientul selectat.
        Preia datele din câmpurile formularului și le validează.
        Dacă datele sunt valide, actualizează baza de date și afișează un mesaj de succes.
        La final, resetează câmpurile formularului și actualizează lista internărilor.
        """        
        
        idpacient = self.id_pacient
        data_internare = self.entry_data_internare.get().strip()
        medic_trimitator = self.entry_medic_trimitator.get()
        bilet_trimitere = self.entry_bilet_trimitere.get().strip()
        diagnostic_prezumtiv = self.entry_diagnostic_prezumtiv.get().strip()
        medic_curant = self.entry_medic_curant.get()
        sectie = self.entry_sectie.get()

        if medic_trimitator and bilet_trimitere and diagnostic_prezumtiv and medic_curant and sectie:

            update_pacienti_internare(data_internare, medic_trimitator, bilet_trimitere, diagnostic_prezumtiv, medic_curant, sectie, idpacient)
            messagebox.showinfo('INFO','Internare adaugata cu succes!', parent = self)


        else:
            messagebox.showerror('EROARE','Nu ati completat toate datele necesare!', parent = self)

        self.entry_data_internare.delete(0, tkinter.END)
        self.entry_medic_trimitator.set('')
        self.entry_bilet_trimitere.delete(0, tkinter.END)
        self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
        self.entry_medic_curant.set('')
        self.entry_sectie.set('')
        
        self.refresh_pacienti()

    def modificare_internare(self):
        """
        Modifică datele de internare ale pacientului selectat.
        Verifică dacă pacientul nu a fost externat și dacă datele sunt valide.
        Dacă utilizatorul confirmă modificarea, actualizează datele și afișează un mesaj de succes.
        La final, resetează câmpurile formularului și actualizează lista internărilor.
        """        
        
        idpacient = self.id_pacient
        data_internare = self.entry_data_internare.get().strip()
        medic_trimitator = self.entry_medic_trimitator.get()
        bilet_trimitere = self.entry_bilet_trimitere.get().strip()
        diagnostic_prezumtiv = self.entry_diagnostic_prezumtiv.get().strip()
        medic_curant = self.entry_medic_curant.get()
        sectie = self.entry_sectie.get()

        if medic_trimitator and bilet_trimitere and diagnostic_prezumtiv and medic_curant and sectie:
            
            if not verificare_existent_externare(idpacient):

                intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI','Confirmati modificarea datelor de internare a pacientului selectat?', parent = self)

                if intrebare:
                    update_pacienti_internare(data_internare, medic_trimitator, bilet_trimitere, diagnostic_prezumtiv, medic_curant, sectie, idpacient)
                    messagebox.showinfo('INFO','Internare modificata cu succes!', parent = self)
                else:
                    messagebox.showwarning('AVERTIZARE','Operatiune anulata', parent = self)
            else:

                messagebox.showerror('EROARE','Pacientul selectat a fost externat! Datele nu pot fi modificate', parent = self)

        else:
            messagebox.showerror('EROARE','Nu ati completat toate datele necesare!', parent = self)

        self.entry_data_internare.delete(0, tkinter.END)
        self.entry_medic_trimitator.set('')
        self.entry_bilet_trimitere.delete(0, tkinter.END)
        self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
        self.entry_medic_curant.set('')
        self.entry_sectie.set('')
        
        self.refresh_pacienti()

    def stergere_internare(self):
        """
        Șterge internarea pacientului selectat.
        Verifică dacă pacientul nu a fost externat înainte de ștergere.
        Dacă nu a fost externat, cere confirmarea utilizatorului și șterge internarea.
        La final, resetează câmpurile formularului și actualizează lista internărilor.
        """        
        
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
        
        self.entry_data_internare.delete(0, tkinter.END)
        self.entry_medic_trimitator.set('')
        self.entry_bilet_trimitere.delete(0, tkinter.END)
        self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
        self.entry_medic_curant.set('')
        self.entry_sectie.set('')
        
        self.refresh_pacienti()

    def prezentare_pacient(self, idpacient):
        """
        Afișează datele pacientului selectat într-un label de prezentare.
        Preia datele din baza de date și le afișează într-un format sumarizat.
        """        
        pacient_selectat = get_pacient_pentru_prezentare(idpacient)
        self.label_prezentare.config(text=f'PACIENTUL\nNume: {pacient_selectat[0]}\nPrenume: {pacient_selectat[1]}\nCNP: {pacient_selectat[2]}\nData nastere: {pacient_selectat[3]}\nVarsta:{pacient_selectat[4]}\nSex: {pacient_selectat[5]}\nStatus: {pacient_selectat[6]}')
       
    def load_selected_pacient(self, event):
        """
        Încarcă datele de internare ale pacientului selectat din tabel în câmpurile formularului pentru editare.
        Setează id-ul pacientului pentru operațiuni ulterioare (modificare/ștergere).
        Actualizează și prezentarea sumarizată a pacientului.
        """        
        
        selected =  self.tabel_pacient.selection()
        if selected:
            values = self.tabel_pacient.item(selected[0])["values"]
            self.id_pacient = values[0]

            self.entry_data_internare.delete(0, tkinter.END)
            self.entry_data_internare.insert(0, values[3])

            self.entry_medic_trimitator.set(values[4])
            
            self.entry_bilet_trimitere.delete(0, tkinter.END)
            self.entry_bilet_trimitere.insert(0, values[5])

            self.entry_diagnostic_prezumtiv.delete(0, tkinter.END)
            self.entry_diagnostic_prezumtiv.insert(0, values[6])
            
            self.entry_medic_curant.set(values[7])
            self.entry_sectie.set(values[8])

            self.prezentare_pacient(self.id_pacient)

class Externare(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.id_pacient = None
        # FRAME-UL CARE CONTINE DATELE PERSONALE ALE PACIENTULUI
        self.frame_date_externare = tkinter.Frame(self)
        self.frame_date_externare.grid(column=0, row=0, padx=(10,10), pady=(10,10))

        # LABEL + ENTRY PENTRU ZILE SPITALIZARE
        tkinter.Label(self.frame_date_externare,text='ZILE SPITALIZARE: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_zile_spitalizare = tkinter.Entry(self.frame_date_externare, width=26)
        self.entry_zile_spitalizare.grid(column=1,row=0,padx=5,pady=5)

        tkinter.Label(self.frame_date_externare,text='DATA EXTERNARII: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_data_externarii = tkinter.Entry(self.frame_date_externare, width=26)
        self.entry_data_externarii.grid(column=1,row=1,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTIC INITIAL
        tkinter.Label(self.frame_date_externare,text='DIAGNOSTIC CONFIRMAT: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_diagnostic = tkinter.Entry(self.frame_date_externare, width=26)
        self.entry_diagnostic.grid(column=1,row=2,padx=5,pady=5)

        # LABEL + ENTRY PENTRU DIAGNOSTIC INITIAL
        tkinter.Label(self.frame_date_externare,text='ALOCATIE DE HRANA: ').grid(column=0,row=3,padx=5,pady=5)
        self.entry_alocatie_hrana = ttk.Combobox(self.frame_date_externare,values=['Hrana basic - 25 lei', 'Hrana premium - 30 lei', 'Hrana gold - 50 lei'],state='readonly', width=24)
        self.entry_alocatie_hrana.grid(column=1,row=3,padx=5,pady=5)

        tkinter.Label(self.frame_date_externare, text='SERVICII EFECTUATE: ').grid(column=0,row=4,padx=5,pady=5)
        tkinter.Button(self.frame_date_externare, text='SERVICIILE EFECTUATE',command=lambda: self.adaugare_servicii()).grid(column=1,row=4,padx=5,pady=5)

        tkinter.Button(self.frame_date_externare,text='ADAUGARE EXTERNARE', command=lambda: self.adaugare_externare()).grid(column=0,row=5,padx=5,pady=5)
        tkinter.Button(self.frame_date_externare,text='MODIFICARE EXTERNARE', command=lambda: self. modificare_externare()).grid(column=1,row=5,padx=5,pady=5)

        self.frame_text = tkinter.Frame(self)
        self.frame_text.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))

        tkinter.Label(self.frame_text, text='RECOMANDARI:').grid(column=0,row=0,padx=5,pady=5)
        self.text_recomandari = tkinter.Text(self.frame_text, width=30, height=7)
        self.text_recomandari.grid(column=0,row=1,padx=10,pady=5)

        tkinter.Label(self.frame_text, text='PLAN DE TRATAMENT:').grid(column=1,row=0,padx=5,pady=5)
        self.text_plan_tratament = tkinter.Text(self.frame_text, width=30, height=7)
        self.text_plan_tratament.grid(column=1,row=1,padx=10,pady=5)

        tkinter.Button(self.frame_text,text='STERGERE EXTERNARE', command= lambda: self.stergere_externare()).grid(column=0,row=2,padx=5,pady=5)

        coloane = ('IdPacient','Nume','Prenume','Zile Spitalizare', 'Data Externarii', 'Diagnostic C', 'Alocatie Hrana')
        self.tabel_pacient = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_pacient.heading(coloana,text=coloana,anchor='center')
            self.tabel_pacient.column(coloana,width=103,anchor='center')

        self.tabel_pacient.grid(column=0,row=1,columnspan=3,rowspan=2, padx=10,pady=10)

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_pacient)

        self.refresh_pacienti()

    def refresh_pacienti(self):
        """
        Reîncarcă tabelul cu pacienți externați din baza de date.
        Șterge toate rândurile existente și inserează datele actualizate.
        """       
       
        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_pacienti_externare():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

    def adaugare_externare(self):
        """
        Adaugă o externare nouă pentru pacientul selectat.
        Preia datele din câmpurile formularului și le validează.
        Dacă datele sunt valide, actualizează baza de date și afișează un mesaj de succes.
        La final, resetează câmpurile formularului și actualizează lista externărilor.
        """        
        
        idpacient = self.id_pacient
        zile_spitalizare = self.entry_zile_spitalizare.get().strip()
        data_externarii = self.entry_data_externarii.get().strip()
        diagnostic_confirmat = self.entry_diagnostic.get().strip()
        alocatie_hrana = self.entry_alocatie_hrana.get()
        recomandari = self.text_recomandari.get("1.0", "end-1c").strip()
        plan_tratament = self.text_plan_tratament.get("1.0", "end-1c").strip()

        if zile_spitalizare and data_externarii and diagnostic_confirmat and alocatie_hrana:
            update_pacienti_externare(zile_spitalizare, data_externarii, diagnostic_confirmat, alocatie_hrana, recomandari, plan_tratament, idpacient)
            messagebox.showinfo('INFO','Externare adaugata cu succes!', parent = self)

            self.entry_zile_spitalizare.delete(0, tkinter.END)
            self.entry_data_externarii.delete(0, tkinter.END)
            self.entry_diagnostic.delete(0, tkinter.END)
            self.entry_alocatie_hrana.set('')
            self.text_recomandari.delete("1.0", "end")
            self.text_plan_tratament.delete("1.0", "end")
            self.refresh_pacienti()

        else:
            messagebox.showerror('EROARE', 'Nu ati introdus datele necesare', parent = self)

        self.refresh_pacienti()

    def modificare_externare(self):
        """
        Modifică datele de externare ale pacientului selectat.
        Verifică dacă datele sunt valide și cere confirmarea utilizatorului.
        Dacă utilizatorul confirmă modificarea, actualizează datele și afișează un mesaj de succes.
        La final, resetează câmpurile formularului și actualizează lista externărilor.
        """        
        
        idpacient = self.id_pacient
        zile_spitalizare = self.entry_zile_spitalizare.get().strip()
        data_externarii = self.entry_data_externarii.get().strip()
        diagnostic_confirmat = self.entry_diagnostic.get().strip()
        alocatie_hrana = self.entry_alocatie_hrana.get()
        recomandari = self.text_recomandari.get("1.0", "end-1c").strip()
        plan_tratament = self.text_plan_tratament.get("1.0", "end-1c").strip()

        if zile_spitalizare and data_externarii and diagnostic_confirmat and alocatie_hrana:
            
            intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI', 'Confirmati modificarea externarii pentru pacientul selectat?', parent = self)
            
            if intrebare:
                update_pacienti_externare(zile_spitalizare, data_externarii, diagnostic_confirmat, alocatie_hrana, recomandari, plan_tratament, idpacient)
                messagebox.showinfo('INFO','Externare modificata cu succes!', parent = self)

                self.entry_zile_spitalizare.delete(0, tkinter.END)
                self.entry_data_externarii.delete(0, tkinter.END)
                self.entry_diagnostic.delete(0, tkinter.END)
                self.entry_alocatie_hrana.set('')
                self.text_recomandari.delete("1.0", "end")
                self.text_plan_tratament.delete("1.0", "end")
                self.refresh_pacienti()

            else: 
                messagebox.showwarning('INFO','Operatiune de modificare a externarii anulata!', parent = self)

        else:
            messagebox.showerror('EROARE', 'Nu ati introdus datele necesare', parent = self)
        
        self.refresh_pacienti()

    def stergere_externare(self):
        """
        Șterge externarea pacientului selectat.
        Cere confirmarea utilizatorului înainte de ștergere.
        La final, resetează câmpurile formularului și actualizează lista externărilor.
        """        
        
        id_pacient = self.id_pacient

        if id_pacient:

            intrebare = messagebox.askyesno('CONFIRMARE STERGERE','Confirmati stergerea externarii pentru pacientul selectat?', parent = self)

            if intrebare:

                stergere_externare(id_pacient)
                messagebox.showinfo('INFO', 'Externare a fost stearsa cu succes', parent = self)

                self.entry_zile_spitalizare.delete(0, tkinter.END)
                self.entry_data_externarii.delete(0, tkinter.END)
                self.entry_diagnostic.delete(0, tkinter.END)
                self.entry_alocatie_hrana.set('')
                self.text_recomandari.delete("1.0", "end")
                self.text_plan_tratament.delete("1.0", "end")
                self.refresh_pacienti()

            else:

                messagebox.showwarning('INFO', 'Operatiune de stergere a externarii anulata!', parent = self)
        else:
            messagebox.showerror('EROARE','Selectati un pacient din lista!', parent = self)


        self.refresh_pacienti()

    def load_selected_pacient(self, event):
        """
        Încarcă datele de externare ale pacientului selectat din tabel în câmpurile formularului pentru editare.
        Setează id-ul pacientului pentru operațiuni ulterioare (modificare/ștergere).
        """        
        selected =  self.tabel_pacient.selection()
        if selected:
            values = self.tabel_pacient.item(selected[0])["values"]
            self.id_pacient = values[0]

            self.entry_zile_spitalizare.delete(0, tkinter.END)
            self.entry_zile_spitalizare.insert(0, values[3])
            
            self.entry_data_externarii.delete(0, tkinter.END)
            self.entry_data_externarii.insert(0, values[4])

            self.entry_diagnostic.delete(0, tkinter.END)
            self.entry_diagnostic.insert(0, values[5])
            
            self.entry_alocatie_hrana.set(values[6])

            self.text_recomandari.delete("1.0", "end")
            self.text_recomandari.insert("1.0", values[7])

            self.text_plan_tratament.delete("1.0", "end")
            self.text_plan_tratament.insert("1.0", values[8])

    def adaugare_servicii(self):
        """
        Deschide o fereastră nouă pentru adăugarea serviciilor efectuate pentru pacientul selectat.
        Permite selectarea și adăugarea serviciilor, precum și vizualizarea și ștergerea serviciilor deja adăugate.
        """        

        if not self.id_pacient:
            messagebox.showerror('EROARE', 'Selectati un pacient din lista!', parent=self)
        else:
            # Creeaza o noua fereastra pentru adaugarea serviciilor
            fereastra_servicii = tkinter.Toplevel(self)
            fereastra_servicii.title("Adaugare Servicii")
            fereastra_servicii.geometry(utilities.pozitionare_fereastra_pe_ecran(self,600,650))
            fereastra_servicii.resizable(False, False)

            frame_fereastra = tkinter.Frame(fereastra_servicii)
            frame_fereastra.pack(padx=15, pady=20)
            # Preia lista de servicii din baza de date
            try:
                lista_servicii = get_lista_servicii()
            except Exception as e:
                messagebox.showerror('EROARE', f"Eroare la preluarea serviciilor: {e}", parent=fereastra_servicii)
                fereastra_servicii.destroy()
                return

            # Creeaza un frame pentru lista de servicii cu scroll
            frame_lista = tkinter.Frame(frame_fereastra)
            frame_lista.pack(pady=5)

            lista_box = tkinter.Listbox(frame_lista, selectmode="multiple", width=43, height=15, font=("Arial", 10))
            for serviciu in lista_servicii:
                lista_box.insert(tkinter.END, f"ID: {serviciu[0]} - {serviciu[1]} - {serviciu[2]}".center(50))
            # lista_box.pack(side="left", fill="both", expand=True)
            lista_box.pack()

            def adauga_la_pacient():
                selectii = lista_box.curselection()
                if not selectii:
                    messagebox.showerror("EROARE", "Selectati cel putin un serviciu din lista!", parent=fereastra_servicii)
                else:
                    iduri_servicii = [lista_servicii[i][0] for i in selectii]
                    try:
                        for id_serviciu in iduri_servicii:
                            adauga_serviciu_la_pacient(self.id_pacient, id_serviciu)  # Functie care face legatura in BD
                        messagebox.showinfo("Succes", "Serviciile au fost adaugate pacientului!", parent=fereastra_servicii)
                        refresh_treeview_servicii()
                    except Exception as e:
                        messagebox.showerror("EROARE", f"Eroare la adaugarea serviciilor: {e}", parent=fereastra_servicii)

            tkinter.Button(frame_fereastra, text="Adauga serviciile selectate", command=lambda: adauga_la_pacient()).pack(pady=5)
            
            # Frame pentru Treeview cu serviciile deja adaugate
            frame_tabel = tkinter.Frame(frame_fereastra)
            frame_tabel.pack(pady=5)

            tkinter.Label(frame_tabel, text="Servicii adaugate pacientului:").pack(pady=5)
            coloane = ("ID", "Denumire", "Valoare")
            tree_servicii = ttk.Treeview(frame_tabel, columns=coloane, show="headings", height=8)
            for coloana in coloane:
                tree_servicii.heading(coloana, text=coloana, anchor="center")
                tree_servicii.column(coloana, width=120, anchor="center")
            tree_servicii.pack(pady=5)

            tkinter.Button(frame_fereastra, text="Stergere serviciu selectat", command=lambda: sterge_serviciu_selectat()).pack(pady=5)

            def refresh_treeview_servicii():
                # Sterge tot
                for row in tree_servicii.get_children():
                    tree_servicii.delete(row)

                # Adauga serviciile pacientului
                servicii_pacient = get_servicii_pacient(self.id_pacient)
                for servicii in servicii_pacient:
                    tree_servicii.insert("", "end", values=servicii)

            def sterge_serviciu_selectat():
                selected = tree_servicii.selection()
                if selected:
                    item = selected[0]   
                    valoare = tree_servicii.item(item, "values")
                    id_serviciu = valoare[0]
                    try:
                        sterge_serviciu_pacient(self.id_pacient, id_serviciu)
                        tree_servicii.delete(item)
                    except Exception as e:
                        messagebox.showerror("EROARE", f"Eroare la stergerea serviciului: {e}", parent=fereastra_servicii)
                    refresh_treeview_servicii()
                else: 
                    messagebox.showerror("EROARE", "Selectati un serviciu din lista de jos pentru stergere!", parent=fereastra_servicii)
                    
            refresh_treeview_servicii()

