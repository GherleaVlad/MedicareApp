import tkinter
import utilities
from tkinter import ttk
from baza_de_date import *
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
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,1050,300)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei
        self.iconbitmap(utilities.get_icon_path())  # Setam iconita aplicatiei        
              
        self.id_operator = None

        self.frame_tabel = tkinter.Frame(self)
        self.frame_tabel.grid(column=1,row=0,padx=(20,20),pady=(20,20))
        
        frame_date = tkinter.Frame(self)
        frame_date.grid(column=0,row=0,padx=(20,20),pady=(20,5))

        coloane = ('IdOperator', 'Utilizator', 'Parola','Nume', 'Prenume', 'Sectie', 'Activ')
        self.tabel_operatori = ttk.Treeview(self.frame_tabel, columns=coloane, show='headings',height=11)

        for coloana in coloane:
            self.tabel_operatori.heading(coloana,text=coloana, anchor='center')
            self.tabel_operatori.column(coloana,width=90,anchor='center')

        self.tabel_operatori.bind("<ButtonRelease-1>", self.load_selected_operator)

        self.tabel_operatori.pack()
        
        # Entry si label pentru utilizator
        tkinter.Label(frame_date,text='UTILIZATOR: ').grid(column=0,row=0,padx=5,pady=5)
        self.entry_utilizator = tkinter.Entry(frame_date, width=26)
        self.entry_utilizator.grid(column=1,row=0,padx=5,pady=5)

        # Entry si label pentru nume utilizator
        tkinter.Label(frame_date,text='NUME: ').grid(column=0,row=1,padx=5,pady=5)
        self.entry_nume = tkinter.Entry(frame_date, width=26)
        self.entry_nume.grid(column=1,row=1,padx=5,pady=5)
        
        # Entry si label pentru prenume utilizator
        tkinter.Label(frame_date,text='PRENUME: ').grid(column=0,row=2,padx=5,pady=5)
        self.entry_prenume = tkinter.Entry(frame_date, width=26)
        self.entry_prenume.grid(column=1,row=2,padx=5,pady=5)
        
        # Entry si label pentru sectie utilizator
        tkinter.Label(frame_date,text='SECTIE: ').grid(column=0,row=3,padx=5,pady=5)
        self.entry_sectie = ttk.Combobox(frame_date,values=utilities.unpack_sectii(), state='readonly', width=23)
        self.entry_sectie.grid(column=1,row=3,padx=5,pady=5)
        
        # Entry si label pentru parola utilizator
        tkinter.Label(frame_date,text='PAROLA: ').grid(column=0,row=4,padx=5,pady=5)
        self.entry_parola = tkinter.Entry(frame_date, width=26)
        self.entry_parola.grid(column=1,row=4,padx=5,pady=5)

        tkinter.Button(frame_date,text='SALVARE', command=lambda: self.adaugare_operator(),width=21).grid(column=0,row=5,padx=5,pady=3)
        tkinter.Button(frame_date,text='MODIFICARE', command = lambda: self.modificare_operator() ,width=21).grid(column=1,row=5,padx=3,pady=5)
        tkinter.Button(frame_date,text='SCHIMBARE PAROLA', command=lambda: self.schimbare_parola(),width=21).grid(column=0,row=6,padx=3,pady=5)
        tkinter.Button(frame_date,text='INACTIVARE', command= lambda: self.dezactivare_operator() ,width=21).grid(column=1,row=6,padx=3,pady=5)

        self.refresh_operatori()

    def refresh_operatori(self):

        for rows in self.tabel_operatori.get_children():
            self.tabel_operatori.delete(rows)

        for rows in get_operatori():
            self.tabel_operatori.insert("", tkinter.END, values=rows)

    def adaugare_operator(self):
        utilizator = self.entry_utilizator.get().strip()
        nume = self.entry_nume.get().strip()
        prenume = self.entry_prenume.get().strip()
        sectie = self.entry_sectie.get()
        parola = self.entry_parola.get().strip()

        date_existente_utilizator = verificare_operator_dupa_utilizator(utilizator)
        date_existente_nume_prenume = verificare_operator_dupa_nume_prenume(nume, prenume)

        if utilizator and nume and prenume and sectie and parola:
            
            if date_existente_utilizator is None:
                if date_existente_nume_prenume is None:
                    insert_operator(utilizator, parola, nume, prenume, sectie)       
                    messagebox.showinfo('INFO', 'Operator adaugata cu succes!', parent = self)

                else:
                    messagebox.showerror('EROARE', 'Operatorul este deja configurat!', parent = self)

            else:
                messagebox.showerror('EROARE', 'Operatorul este deja configurat!', parent = self)

        else:

            messagebox.showerror('EROARE', 'Introduceti date valide!', parent = self)

        self.entry_utilizator.delete(0, tkinter.END)
        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_sectie.set('')
        self.entry_parola.delete(0, tkinter.END)

        self.refresh_operatori()

    def modificare_operator(self):
        utilizator = self.entry_utilizator.get().strip()
        nume = self.entry_nume.get().strip()
        prenume = self.entry_prenume.get().strip()
        sectie = self.entry_sectie.get()

        if nume and prenume and sectie:
            
            if verificare_operator_dupa_utilizator(utilizator) is not None:

                intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI', 
                                                f'Pentru operatorul : {utilizator}\nDoriti efectuarea urmatoarelor modificari:\nNume: {nume}\nPrenume: {prenume}\nSectie: {sectie} ?',
                                                parent = self)
                
                if intrebare: 
                    update_operator(nume, prenume, sectie, self.id_operator)
                    messagebox.showinfo('INFO', 'Operator modificat cu succes!', parent = self)
                
                else:
                    messagebox.showwarning('AVERTIZARE', 'Datele nu au fost modificate', parent = self)

            else:
                messagebox.showerror('EROARE', 'Operatorul nu este configurat', parent = self)
        else:
            messagebox.showerror('EROARE', 'Selectati un operator din lista!', parent = self)

        self.entry_utilizator.delete(0, tkinter.END)
        self.entry_nume.delete(0, tkinter.END)
        self.entry_prenume.delete(0, tkinter.END)
        self.entry_sectie.set('')
        self.entry_parola.delete(0, tkinter.END)

        self.refresh_operatori()

    def dezactivare_operator(self):
            
            utilizator = self.entry_utilizator.get().strip()

            if self.id_operator:
                intrebare = messagebox.askyesno('CONFIRMARE INACTIVARE', 
                                                f'Doriti inactivarea operatorului: {utilizator}',
                                                parent = self)
                
                if intrebare:
                    inactivare_operator(self.id_operator)
                    messagebox.showinfo('INFO', 'Operator inactivat!', parent = self)

                else:
                    messagebox.showwarning('AVERTIZARE', 'Datele nu au fost modificate', parent = self)

            else:
                messagebox.showerror('EROARE', 'Selectati un operator din lista!', parent = self)

            self.entry_utilizator.delete(0, tkinter.END)
            self.entry_nume.delete(0, tkinter.END)
            self.entry_prenume.delete(0, tkinter.END)
            self.entry_sectie.set('')
            self.entry_parola.delete(0, tkinter.END)

            self.refresh_operatori()

    def load_selected_operator(self, event):
            selected = self.tabel_operatori.selection()
            if selected:
                values = self.tabel_operatori.item(selected[0])["values"]

                self.id_operator = values[0]

                self.entry_utilizator.delete(0, tkinter.END)
                self.entry_utilizator.insert(0, values[1])

                self.entry_parola.delete(0, tkinter.END)
                self.entry_parola.insert(0, values[2])

                self.entry_nume.delete(0, tkinter.END)
                self.entry_nume.insert(0, values[3])

                self.entry_prenume.delete(0, tkinter.END)
                self.entry_prenume.insert(0, values[4])

                self.entry_sectie.set(values[5])

    def schimbare_parola(self):
        
        if self.id_operator:
            fereastra_schimbare_parola = tkinter.Toplevel(self)
            fereastra_schimbare_parola.title("Adaugare Servicii")
            fereastra_schimbare_parola.geometry(utilities.pozitionare_fereastra_pe_ecran(self,300,250))
            fereastra_schimbare_parola.resizable(False, False)

            frame_fereastra = tkinter.Frame(fereastra_schimbare_parola)
            frame_fereastra.pack(padx=10,pady=20)

            tkinter.Label(frame_fereastra, text='Parola veche:').grid(column=0,row=0,padx=5,pady=5)
            tkinter.Label(frame_fereastra, text='Parola noua:').grid(column=0,row=1,padx=5,pady=5)
            tkinter.Label(frame_fereastra, text='Confirmare parola:').grid(column=0,row=2,padx=5,pady=5)

            entry_parola_veche = tkinter.Entry(frame_fereastra, width=20)
            entry_parola_noua = tkinter.Entry(frame_fereastra, width=20)
            entry_confirmare_parola = tkinter.Entry(frame_fereastra, width=20)

            entry_parola_veche.grid(column=1,row=0,padx=5,pady=5)
            entry_parola_noua.grid(column=1,row=1,padx=5,pady=5)
            entry_confirmare_parola.grid(column=1,row=2,padx=5,pady=5)
            
            tkinter.Button(fereastra_schimbare_parola,text='SCHIMBARE PAROLA', command=lambda: modificare_parola(), width=20).pack(padx=5,pady=5)

            def modificare_parola():
                
                idoperator = self.id_operator

                if verificare_parola_corecta(idoperator, entry_parola_veche.get()):

                    intrebare = messagebox.askyesno('CONFIRMARE MODIFICARI','Confirmati modificarea parolei?', parent = fereastra_schimbare_parola)

                    if intrebare:

                        functie_schimbare_parola(entry_parola_noua.get(),idoperator)
                        messagebox.showinfo('INFO','Parola modificata cu succes', parent = fereastra_schimbare_parola)
                        fereastra_schimbare_parola.destroy()
                        self.refresh_operatori()
                    else:
                        messagebox.showwarning('AVERTIZARE','Operatiune anulata!',parent = fereastra_schimbare_parola)
                        fereastra_schimbare_parola.destroy()
                        self.refresh_operatori()
                else:
                    messagebox.showerror('EROARE','Parola veche incorecta!', parent = fereastra_schimbare_parola)

        else:
                messagebox.showerror('EROARE','Selectati un operator din lista!', parent = self)




    
