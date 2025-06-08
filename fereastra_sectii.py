import tkinter
import utilities
from tkinter import ttk
from baza_de_date import insert_sectie, verificare_sectie, get_sectii,update_sectii
from tkinter import messagebox

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


        self.frame_tabel = tkinter.Frame(self)
        self.frame_tabel.grid(column=1,row=0,padx=(20,20),pady=(20,20))
        
        frame_date = tkinter.Frame(self)
        frame_date.grid(column=0,row=0,padx=(20,20),pady=(20,5))

        coloane = ('IdSectie', 'Denumire','Medic Sef Sectie')
        self.tabel_pacient = ttk.Treeview(self.frame_tabel, columns=coloane, show='headings')

        for coloana in coloane:
            self.tabel_pacient.heading(coloana,text=coloana)
            self.tabel_pacient.column(coloana,width=120,anchor="center")

        self.tabel_pacient.bind("<ButtonRelease-1>", self.load_selected_sectie)

        self.tabel_pacient.pack()
        
        # Butoane si Entry-uri pentru introducere operator

        # Entry si label pentru sectie
        tkinter.Label(frame_date,text='SECTIE: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_sectie = tkinter.Entry(frame_date, width=26)
        self.entry_sectie.grid(column=1,row=0,padx=5,pady=5)

        # Entry si label pentru medic sef de sectie
        tkinter.Label(frame_date,text='SEF SECTIE: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_sef_sectie = ttk.Combobox(frame_date, values=['Medic1','Medic2'], state='readonly', width=23)
        self.entry_sef_sectie.grid(column=1,row=1,padx=5,pady=5)
        
        tkinter.Button(frame_date,text='SALVARE',command=lambda: self.adaugare_sectie(),width=21).grid(column=0,row=2,padx=5,pady=3)
        tkinter.Button(frame_date,text='ACTUALIZARE', command=lambda: self.modificare_sectie(),width=21).grid(column=1,row=2,padx=3,pady=5)
        
        tkinter.Label(self, text='ATENTIE! \n Poate fi modificat doar medicul sef de sectie \n pentru o sectie configurata! ').grid(column=0,row=1,padx=(5,0))

        self.refresh_sectii()

    def refresh_sectii(self):
        for rows in self.tabel_pacient.get_children():
            self.tabel_pacient.delete(rows)

        for rows in get_sectii():
            self.tabel_pacient.insert("", tkinter.END, values=rows)

    def adaugare_sectie(self):
        sectie = self.entry_sectie.get().strip()
        sef_sectie = self.entry_sef_sectie.get()
        
        date_existente = verificare_sectie(sectie)

        if sectie and sef_sectie:
            if date_existente is None:
                insert_sectie(sectie,sef_sectie)       
                messagebox.showinfo('INFO', 'Sectie adaugata cu succes!', parent=self)

            else:
                messagebox.showerror('EROARE', 'Sectia este deja configurata!', parent=self)

        else:
            messagebox.showerror('EROARE', 'Introduceti date valide!', parent=self)

        self.entry_sectie.delete(0, tkinter.END)
        self.entry_sef_sectie.set('')

        self.refresh_sectii()

    def modificare_sectie(self):
        sectie = self.entry_sectie.get().strip()
        sef_sectie = self.entry_sef_sectie.get()
        
        if sectie and sef_sectie:

            if verificare_sectie(sectie) is not None:
                
                if self.id_sectie:
                    intrebare = messagebox.askyesno('CONFIRMARE MODIFICARE', 
                                                f'Doriti modificarea sefului de sectie pentru sectia: {sectie}',
                                                parent = self)
                
                if intrebare:
                    update_sectii(sef_sectie,self.id_sectie)
                    messagebox.showinfo('INFO', 'Sectie modificata!', parent = self)
                else:
                    messagebox.showwarning('AVERTIZARE', 'Datele nu au fost modificate!', parent = self)

            else:
                messagebox.showerror('EROARE', 'Sectia nu este configurata!', parent = self)

        else:
            messagebox.showerror('EROARE', 'Selectati o inregistrare!', parent = self)

        self.entry_sectie.delete(0, tkinter.END)
        self.entry_sef_sectie.set('')

        self.refresh_sectii()
            
    def load_selected_sectie(self, event):
        selected = self.tabel_pacient.selection()
        if selected:
            values = self.tabel_pacient.item(selected[0])["values"]

            self.id_sectie = values[0]

            self.entry_sectie.delete(0, tkinter.END)
            self.entry_sectie.insert(0, values[1])

            self.entry_sef_sectie.set(values[2])

