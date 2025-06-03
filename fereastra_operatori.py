import tkinter
import utilities
from tkinter import ttk
from baza_de_date import insert_operator, verificare_operator_dupa_utilizator, verificare_operator_dupa_nume_prenume, get_operatori
from tkinter import messagebox

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

        self.frame_tabel = tkinter.Frame(self)
        self.frame_tabel.grid(column=1,row=0,padx=(20,20),pady=(20,20))
        
        frame_date = tkinter.Frame(self)
        frame_date.grid(column=0,row=0,padx=(20,20),pady=(20,5))

        coloane = ('IdOperator', 'Utilizator', 'Parola','Nume', 'Prenume', 'Sectie')
        self.tabel_operatori = ttk.Treeview(self.frame_tabel, columns=coloane, show='headings',height=11)

        for coloana in coloane:
            self.tabel_operatori.heading(coloana,text=coloana)
            self.tabel_operatori.column(coloana,width=90,anchor='center')

        self.tabel_operatori.bind("<ButtonRelease-1>", self.load_selected_operator)

        self.tabel_operatori.pack()
        
        # Butoane si Entry-uri pentru introducere operator

        tkinter.Button(frame_date,text='INCARCA UTILIZATORI', command= lambda: self.load_all_operatori(),width=25, relief='groove').grid(column=0,row=0,padx=5,pady=5,columnspan=2)

        # Entry si label pentru utilizator
        tkinter.Label(frame_date,text='UTILIZATOR: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_utilizator = tkinter.Entry(frame_date, width=26)
        self.entry_utilizator.grid(column=1,row=1,padx=5,pady=5)

        # Entry si label pentru nume utilizator
        tkinter.Label(frame_date,text='NUME: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_nume = tkinter.Entry(frame_date, width=26)
        self.entry_nume.grid(column=1,row=2,padx=5,pady=5)
        
        # Entry si label pentru prenume utilizator
        tkinter.Label(frame_date,text='PRENUME: ').grid(column=0,row=3,padx=5,pady=5)
        self.entry_prenume = tkinter.Entry(frame_date, width=26)
        self.entry_prenume.grid(column=1,row=3,padx=5,pady=5)
        
        # Entry si label pentru sectie utilizator
        tkinter.Label(frame_date,text='SECTIE: ').grid(column=0,row=4,padx=5,pady=5)
        self.entry_sectie = ttk.Combobox(frame_date,values=['Sectie1','Sectie2'], state='readonly', width=23)
        self.entry_sectie.grid(column=1,row=4,padx=5,pady=5)
        
        # Entry si label pentru parola utilizator
        tkinter.Label(frame_date,text='PAROLA: ').grid(column=0,row=5,padx=5,pady=5)
        self.entry_parola = tkinter.Entry(frame_date, width=26)
        self.entry_parola.grid(column=1,row=5,padx=5,pady=5)

        tkinter.Button(frame_date,text='SALVARE', command=lambda: self.adaugare_operator(),width=21).grid(column=0,row=6,padx=5,pady=3)
        tkinter.Button(frame_date,text='ACTUALIZARE',width=21).grid(column=1,row=6,padx=3,pady=5)

    def adaugare_operator(self):
        utilizator = self.entry_utilizator.get()
        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()
        sectie = self.entry_sectie.get()
        parola = self.entry_parola.get()

        date_existente_utilizator = verificare_operator_dupa_utilizator(utilizator)
        date_existente_nume_prenume = verificare_operator_dupa_nume_prenume(nume, prenume)

        if (date_existente_utilizator is None) or (date_existente_nume_prenume is None):
            insert_operator(utilizator, parola, nume, prenume, sectie)       
            messagebox.showinfo('Mesaj', 'Operator adaugata cu succes!')
            self.focus_force() # Pentru intoarcerea in fereastra sectii dupa ce afiseaza mesajul de eroare

        else:
            messagebox.showerror('EROARE', 'Operatorul este deja configurat!')
            self.focus_force() # Pentru intoarcerea in fereastra sectii dupa ce afiseaza mesajul de eroare             

    def load_all_operatori(self):
        self.tabel_operatori.delete(*self.tabel_operatori.get_children())
        for row in get_operatori():
            self.tabel_operatori.insert("", tkinter.END, values=row)

    def load_selected_operator(self, event):
        selected = self.tabel_operatori.selection()
        if selected:
            values = self.tabel_operatori.item(selected[0])["values"]
            self.entry_utilizator.delete(0, tkinter.END)
            self.entry_utilizator.insert(0, values[1])

            self.entry_parola.delete(0, tkinter.END)
            self.entry_parola.insert(0, values[2])

            self.entry_nume.delete(0, tkinter.END)
            self.entry_nume.insert(0, values[3])

            self.entry_prenume.delete(0, tkinter.END)
            self.entry_prenume.insert(0, values[4])

            self.entry_sectie.set(values[5])

