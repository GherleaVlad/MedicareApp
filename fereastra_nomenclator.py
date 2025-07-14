import tkinter
import utilities
from tkinter import ttk
from baza_de_date import *
from tkinter import messagebox, filedialog
import json

class Fereastra_nomenclator(tkinter.Toplevel):
    def __init__(self,master): # Constructorul clasei Fereastra_nomenclator (clasa care mosteneste TopLevel din Tkinter)
        super().__init__(master) # Initializarea clasei parinte (clasa Meniu Principal)
        self.title('Nomenclator') # Titlul ferestrei
        self.resizable(False, False) # Imposibilitate de redimensionare fereastra
        self.update_idletasks() # Asteapta initializarea completa a ferestrei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,725,450)) # Setam geometria si centrarea pe ecran
        self.iconbitmap(r'C:\Users\vladg\OneDrive\Documents\GitHub\MedicareApp\Logo.ico') # Setam iconita aplicatiei
        
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
        self.id_medic = None

        tkinter.Label(self.frame_date_medic,text='Nume: ').grid(column=0,row=0,pady=5)
        tkinter.Label(self.frame_date_medic,text='Prenume: ').grid(column=0,row=1,pady=5)
        tkinter.Label(self.frame_date_medic,text='Parafa: ').grid(column=0,row=2,pady=5)
        tkinter.Label(self.frame_date_medic, text='Activ/Inactiv: ').grid(column=0,row=3,pady=5)

        self.entry_nume = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_nume.grid(column=1,row=0,padx=5,pady=5)

        self.entry_prenume = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_prenume.grid(column=1,row=1,padx=5,pady=5)


        self.entry_parafa = tkinter.Entry(self.frame_date_medic,width=26)
        self.entry_parafa.grid(column=1,row=2,padx=5,pady=5)

        self.activ_var = tkinter.IntVar()
        self.activ_checkbox = tkinter.Checkbutton(self.frame_date_medic, variable=self.activ_var)
        self.activ_checkbox.grid(column=1,row=3,padx=5,pady=5)


        self.frame_butoane = tkinter.Frame(self)
        self.frame_butoane.grid(column=1,row=0,padx=(10,10),pady=(10,10))

        tkinter.Button(self.frame_butoane,text='Adaugare',command=lambda: self.adaugare_medic(),width=25).grid(column=0,row=1,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare', command=lambda: self.modificare_medic(),width=25).grid(column=0,row=2,pady=5)
        tkinter.Button(self.frame_butoane,text='Stergere', command=lambda: self.stergere_medic(),width=25).grid(column=0,row=3,pady=5)


        coloane = ('IdMedic','Nume','Prenume','Parafa','Activ')
        self.tabel_medici_curanti = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_medici_curanti.heading(coloana,text=coloana,anchor='center')
            self.tabel_medici_curanti.column(coloana,width=125,anchor='center')

        self.tabel_medici_curanti.grid(column=0,row=1,columnspan=2,rowspan=2,padx=(50,10),pady=(10,10))

        self.tabel_medici_curanti.bind("<ButtonRelease-1>", self.load_selected_medic)

        self.refresh_medici()

    def refresh_medici(self):
        
        for rows in self.tabel_medici_curanti.get_children():
            self.tabel_medici_curanti.delete(rows)

        for rows in get_medici_curanti():
            self.tabel_medici_curanti.insert("", tkinter.END , values=rows)

    def adaugare_medic(self):
        nume = self.entry_nume.get().upper()
        prenume = self.entry_prenume.get().upper()
        parafa = self.entry_parafa.get().upper()
        activ = self.activ_var.get()

        date_existente = verificare_existenta_medic_curant(parafa)

        if nume and prenume and parafa:

            if date_existente is None:
                insert_medic_curant(nume, prenume, parafa, activ)
                messagebox.showinfo( 'INFO', 'Medic adaugat cu succes! ', parent = self)

            else:

                messagebox.showerror('EROARE', 'Medicul este deja configurat! ', parent = self)

        else:

            messagebox.showerror('EROARE', 'Introduceti date valide! ', parent = self)

        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_parafa.delete(0, tkinter.END)
        self.activ_var.set(int('0'))
        self.refresh_medici()

    def modificare_medic(self):
        nume = self.entry_nume.get().upper()
        prenume = self.entry_prenume.get().upper()
        parafa = self.entry_parafa.get().upper()
        activ = self.activ_var.get()

        if nume and prenume and parafa:

            if verificare_existenta_medic_curant(parafa) is not None:
                
                intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI', 
                                                f'Pentru parafa medicului : {parafa}\nDoriti efectuarea urmatoarelor modificari:\nNume: {nume}\nPrenume: {prenume}\nStatus: {"Inactiv" if activ == 0 else "Activ"}?',
                                                parent = self)
                
                if intrebare: 
                    update_medic_curant(nume, prenume, activ, self.id_medic)
                    messagebox.showinfo('INFO', 'Medicul a fost modificat cu succes!', parent = self)
                
                else:
                    messagebox.showwarning('AVERTIZARE', 'Datele medicului nu au fost modificate', parent = self)
 
            else:
                messagebox.showerror('EROARE', 'Medicul nu este configurat', parent = self)

        else:

            messagebox.showerror('EROARE', 'Selectati o inregistrare din lista! ', parent = self)
        
        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_parafa.delete(0, tkinter.END)
        self.activ_var.set(int('0'))
        self.refresh_medici()

    def stergere_medic(self):
        idmedic = self.id_medic
        nume = self.entry_nume.get().upper()
        prenume = self.entry_prenume.get().upper()
        parafa = self.entry_parafa.get().upper()

        string_medic = f'{nume}  {prenume} - {parafa}'

        if idmedic:
            if verificare_existenta_inregistrari(string_medic) is None:
                
                intrebare = messagebox.askyesno('CONFIRMARE STERGERE','Confirmati stergerea medicului selectat?', parent = self)
                
                if intrebare:
                    stergere_medic_curant(idmedic)
                    messagebox.showinfo('INFO','Medic sters cu succes!', parent = self)
                else:
                    messagebox.showwarning('INFO','Operatiune anulata', parent = self)            
            else:
                messagebox.showerror('EROARE','Stergerea medicului curant nu este posibila deoarece exista inregistrari asociate acestuia.', parent = self)
        else:
            messagebox.showerror('EROARE','Selectati un medic din lista', parent = self)


        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_parafa.delete(0, tkinter.END)
        self.activ_var.set(int('0'))
        self.refresh_medici()

    def load_selected_medic(self, event):
        selected = self.tabel_medici_curanti.selection()

        if selected:
            values = self.tabel_medici_curanti.item(selected[0])["values"]

            self.id_medic = values[0]

            self.entry_nume.delete(0, tkinter.END)
            self.entry_nume.insert(0, values[1])

            self.entry_prenume.delete(0, tkinter.END)
            self.entry_prenume.insert(0, values[2])

            self.entry_parafa.delete(0, tkinter.END)
            self.entry_parafa.insert(0, values[3])

            self.activ_var.set(int(values[4]))


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

        tkinter.Button(self.frame_butoane,text='Adaugare', command= lambda: self.adaugare_medic(),width=25).grid(column=0,row=1,pady=5)
        tkinter.Button(self.frame_butoane,text='Modificare', command= lambda: self.modificare_medic(),width=25).grid(column=0,row=2,pady=5)
        tkinter.Button(self.frame_butoane,text='Incarcare nomenclator medici', command= lambda: self.incarcare_nomenclator(),width=25).grid(column=0,row=3,pady=5)

        coloane = ('IdMedic','Nume','Prenume','Parafa', 'Activ')
        self.tabel_medici_trimitatori = ttk.Treeview(self, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_medici_trimitatori.heading(coloana,text=coloana,anchor='center')
            self.tabel_medici_trimitatori.column(coloana,width=125,anchor='center')

        self.tabel_medici_trimitatori.grid(column=0,row=1,columnspan=2,rowspan=2,padx=(50,10),pady=(10,10))

        self.tabel_medici_trimitatori.bind("<ButtonRelease-1>", self.load_selected_medic)

        self.refresh_medici()

    def refresh_medici(self):
        
        for rows in self.tabel_medici_trimitatori.get_children():
            self.tabel_medici_trimitatori.delete(rows)

        for rows in get_medici_trimitatori():
            self.tabel_medici_trimitatori.insert("", tkinter.END , values=rows)

    def adaugare_medic(self):
        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()
        parafa = self.entry_parafa.get().capitalize()

        date_existente = verificare_existenta_medic_trimitator(parafa)

        if nume and prenume and parafa:

            if date_existente is None:
                insert_medic_trimitator(nume, prenume, parafa)
                messagebox.showinfo( 'INFO', 'Medic adaugat cu succes! ', parent = self)

            else:

                messagebox.showerror('EROARE', 'Medicul este deja configurat! ', parent = self)

        else:

            messagebox.showerror('EROARE', 'Introduceti date valide! ', parent = self)
        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_parafa.delete(0, tkinter.END)
        self.refresh_medici()

    def modificare_medic(self):
        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()
        parafa = self.entry_parafa.get().capitalize()

        if nume and prenume and parafa:

            if verificare_existenta_medic_trimitator(parafa) is not None:
                
                intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI', 
                                                f'Pentru parafa medicului : {parafa}\nDoriti efectuarea urmatoarelor modificari:\nNume: {nume}\nPrenume: {prenume}\n?',
                                                parent = self)
                
                if intrebare: 
                    update_medic_trimitator(nume, prenume, self.id_medic)
                    messagebox.showinfo('INFO', 'Medicul a fost modificat cu succes!', parent = self)
                
                else:
                    messagebox.showwarning('AVERTIZARE', 'Datele medicului nu au fost modificate', parent = self)
 
            else:
                messagebox.showerror('EROARE', 'Medicul nu este configurat', parent = self)

        else:

            messagebox.showerror('EROARE', 'Selectati o inregistrare din lista! ', parent = self)
        
        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_parafa.delete(0, tkinter.END)
        self.refresh_medici()

    def load_selected_medic(self, event):
        selected = self.tabel_medici_trimitatori.selection()

        if selected:
            values = self.tabel_medici_trimitatori.item(selected[0])["values"]

            self.id_medic = values[0]

            self.entry_nume.delete(0, tkinter.END)
            self.entry_nume.insert(0, values[1])

            self.entry_prenume.delete(0, tkinter.END)
            self.entry_prenume.insert(0, values[2])

            self.entry_parafa.delete(0, tkinter.END)
            self.entry_parafa.insert(0, values[3])

    def incarcare_nomenclator(self):
        cale_fisier = filedialog.askopenfilename(
            title='Selectati fisierul JSON pentru medicii trimitatori',
            filetypes=[('Fișier JSON', '*.json')],
            parent=self
        )

        if cale_fisier:
            medici_trimitatori_existenti = get_medici_trimitatori() 
            parafe_nomenclator = [medic[3] for medic in medici_trimitatori_existenti]

            with open(cale_fisier, 'r') as fisier:
                data = json.load(fisier)

                for medic_nou in data:
                    parafa_noua = medic_nou.get('parafa')
                    
                    if parafa_noua not in parafe_nomenclator:
                        insert_medic_trimitator(
                            medic_nou.get('nume'),
                            medic_nou.get('prenume'),
                            parafa_noua
                        )

                parafe_json = [parafa.get('parafa') for parafa in data]

                for parafe_medici_existenti in parafe_nomenclator:
                    if parafe_medici_existenti not in parafe_json:
                        update_parafe_inexistente(parafe_medici_existenti)
                        


            messagebox.showinfo('SUCCES', 'Nomenclator încărcat cu succes!', parent=self)
            self.refresh_medici()

        else:
            messagebox.showerror('EROARE', 'Nu ați selectat un fișier valid!', parent=self)
