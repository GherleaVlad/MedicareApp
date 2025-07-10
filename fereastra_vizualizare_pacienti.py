import tkinter
import utilities
from tkinter import ttk
from baza_de_date import get_pacienti_vizualizare
from tkinter import filedialog, messagebox
import csv

'''
Modulul fereastra_vizualizare_pacienti este folosita pentru vizualizarea, tiparirea si exportul internarilor.

'''

class FereastraVizualizarePacienti(tkinter.Toplevel):
    def __init__(self, master): # Initializare constructor pentru clasa Fereastra Rapoarte (reprezinta tkinter.TopLevel - clasa copil pentru tkinter.Tk)
        super().__init__(master) # Initializare constructor pentru clasa parinte (adica pentru clasa MeniuPrincipal - care reprezinta tkinter.Tk (clasa principala - radacina))
        self.title('Vizualizare Internari') # Numele ferestrei
        self.resizable(False, False) # Dimensiunea nu este modificabila
        self.update_idletasks() # Asteapta initializarea completa a aplicatiei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,1400,550)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei
        
        # frame pentru criteriile de filtrare si butoanele de filtrare
        self.criterii_filtrare = tkinter.Frame(self)
        self.criterii_filtrare.grid(column=0, row=0,padx=10, pady=(15,10))

        tkinter.Label(self.criterii_filtrare,text='Alegeti criteriul de filtrare a datelor:').pack()

        self.optiune_sectie = tkinter.IntVar()
        self.optiune_medic = tkinter.IntVar()

        criteriu_sectie = tkinter.Checkbutton(self.criterii_filtrare,text="Filtrare dupa sectie", variable=self.optiune_sectie)
        criteriu_medic = tkinter.Checkbutton(self.criterii_filtrare,text="Filtrare dupa medic", variable=self.optiune_medic)

        criteriu_sectie.pack(pady=5)
        criteriu_medic.pack(pady=5)

        # frame filtrarea datelor pe criteriul selectat 
        self.filtrare_date = tkinter.Frame(self)
        self.filtrare_date.grid(column=1, row=0,padx=10, pady=(15,10))

        tkinter.Label(self.filtrare_date, text='Filtrare dupa sectie:').grid(column=0,row=0,padx=5,pady=5)
        self.combobox_sectie = ttk.Combobox(self.filtrare_date,values=utilities.unpack_sectii(), state='disabled', width=23)
        self.combobox_sectie.grid(column=0,row=1,padx=5,pady=5)

        tkinter.Label(self.filtrare_date, text='Filtrare dupa medici:').grid(column=1,row=0,padx=5,pady=5)
        self.combobox_medic = ttk.Combobox(self.filtrare_date,values=utilities.unpack_medici(), state='disabled', width=23)
        self.combobox_medic.grid(column=1,row=1,padx=5,pady=5)

        self.optiune_sectie.trace_add('write', self.setare_stare_combobox)
        self.optiune_medic.trace_add('write', self.setare_stare_combobox)

        # frame butoane pentru filtrare si refresh (inapoi la toate)
        self.butoane = tkinter.Frame(self)
        self.butoane.grid(column=2, row=0,padx=10, pady=(15,10))

        tkinter.Button(self.butoane, text='FILTRARE', command= lambda: self.filtrare_pacienti(), width=15).pack(padx=5,pady=10)
        tkinter.Button(self.butoane, text='REFRESH', command= lambda: self.refresh_date(), width=15).pack(padx=5,pady=10)


        # frame tabel si tabel efectiv
        self.frame_tabel = tkinter.Frame(self)
        self.frame_tabel.grid(column=0,row=1, columnspan=3,padx=10, pady=10)

        coloane = ('Nume', 'Prenume', 'CNP','Data Nastere', 'Varsta', 'Sex', 'Asigurat', 'Data Internare', 'Medic Curant', 'Diagnostic P', 'Sectie', 'Zile Spitalizare','Data Externare','Diagnostic C')
        self.tabel_date = ttk.Treeview(self.frame_tabel, columns=coloane, show='headings',height=15)

        for coloana in coloane:
            self.tabel_date.heading(coloana,text=coloana, anchor='center')
            self.tabel_date.column(coloana,width=95,anchor='center')

        self.tabel_date.pack(padx=10)

        self.refresh_date()

        tkinter.Button(self,text='EXPORT CSV', command=lambda: self.export_csv()).grid(column=1, row=2, pady=10)
        tkinter.Button(self,text='EXPORT JSON', command=lambda: self.export_json()).grid(column=1, row=3, pady=5)

    def refresh_date(self):
        for rows in self.tabel_date.get_children():
            self.tabel_date.delete(rows)

        for rows in get_pacienti_vizualizare():
            self.tabel_date.insert("", tkinter.END, values=rows)

    def setare_stare_combobox(self,*args):
            if self.optiune_sectie.get():
                self.combobox_sectie.config(state='readonly')
            else:
                self.combobox_sectie.set('')
                self.combobox_sectie.config(state='disabled')
            if self.optiune_medic.get():
                self.combobox_medic.config(state='readonly')
            else:
                self.combobox_medic.set('')
                self.combobox_medic.config(state='disabled')

    def filtrare_pacienti(self):
        """
        Filters and displays patients in the table based on selected section and/or doctor.
        The method retrieves the current filter options from the UI (section and doctor),
        clears the existing patient table, and fetches the full list of patients.
        It then filters the patients according to the selected section and/or doctor,
        and inserts the filtered results back into the table.
        Filtering logic:
            - If the section filter is enabled and a section is selected, only patients
              belonging to the selected section are included.
            - If the doctor filter is enabled and a doctor is selected, only patients
              assigned to the selected doctor are included.
            - Both filters can be applied simultaneously.
        Assumes:
            - `self.optiune_sectie` and `self.optiune_medic` are BooleanVars indicating
              if the respective filters are enabled.
            - `self.combobox_sectie` and `self.combobox_medic` provide the selected values.
            - `get_pacienti_vizualizare()` returns a list of patient records.
            - `self.tabel_date` is a tkinter Treeview widget for displaying patients.
        """
        
        filtrare_dupa_sectie = self.optiune_sectie.get()
        filtrare_dupa_medic = self.optiune_medic.get()
        sectie_selectata = self.combobox_sectie.get()
        medic_selectat = self.combobox_medic.get()
        
        for row in self.tabel_date.get_children():
            self.tabel_date.delete(row)
       
        pacienti = get_pacienti_vizualizare()
        
        pacienti_filtrati = list()
        for pacient in pacienti:

            ok = True
            if filtrare_dupa_sectie and sectie_selectata:
                if str(pacient[10]) != sectie_selectata:
                    ok = False
            if filtrare_dupa_medic and medic_selectat:
                if str(pacient[8]) != medic_selectat:
                    ok = False
            if ok:
                pacienti_filtrati.append(pacient)

        for p in pacienti_filtrati:
            self.tabel_date.insert("", tkinter.END, values=p)
            
    def export_csv(self):
        """
        Functia export_csv exporta pacientii afisati in treeview intr-un fisier CSV, la o locatie aleasa de utilizator.
        """
        # Deschide dialog pentru alegerea locatiei fisierului
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Alegeti locatia de salvare a fisierului",
            parent=self)
        
        if not file_path:
            messagebox.showerror('EROARE', 'Nu ati selectat o cale de salvare a fisierului! Operatiune anulata!', parent = self) 
        else:
            # Preluarea datelor din treeview si export in csv, col
            coloane = self.tabel_date["columns"]
            randuri = [self.tabel_date.item(IdInregistrare)["values"] for IdInregistrare in self.tabel_date.get_children()]

            try:
                with open(file_path, mode="w", newline='') as fisier:
                    writer = csv.writer(fisier)
                    writer.writerow(coloane)
                    writer.writerows(randuri)
                messagebox.showinfo("INFO", f"Date exportate cu succes:\n{file_path}", parent=self)
            except Exception as e:
                messagebox.showerror("EROARE", f"A aparut o eroare la exportul fisierului:\n{e}", parent=self)

    def export_json(self):
        pass

