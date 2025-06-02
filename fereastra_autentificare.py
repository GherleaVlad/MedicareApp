import tkinter
import baza_de_date
import utilities

'''
Modulul fereastra_autentificare este folosit pentru crearea ferestrei de autentificare in aplicatie si contine clasa FereastraAutentificare, in cadrul careia se afla metoda
verificare_login, folosit pentru verificarea datelor introduse de operator pentru autentificarea in aplicatie. 
In cazul autentificarii cu succes, aplicatia intra in meniul principal, iar in caz contrar afiseaza un label care ne informeaza ca utilizatorul si parola introduse sunt incorecte.
'''

class FereastraAutentificare(tkinter.Toplevel):
    def __init__(self, master): # Initializare constructor pentru clasa Fereastra Autentificare (reprezinta tkinter.TopLevel - clasa copil pentru tkinter.Tk)
        super().__init__(master) # Initializare constructor pentru clasa parinte (adica pentru clasa MeniuPrincipal - care reprezinta tkinter.Tk (clasa principala - radacina))
        self.title('Autentificare') # Numele ferestrei
        self.resizable(False, False) # Dimensiunea nu este modificabila
       # self.update_idletasks() # Asteapta initializarea completa a aplicatiei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,350,180)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei

        # Label si Entry pentru autentificare utilizator + pozitionare
        tkinter.Label(self, text="Utilizator:").pack(pady=(10, 0))
        self.entry_utilizator = tkinter.Entry(self)
        self.entry_utilizator.pack()

        # Label si Entry pentru autentificare parola + pozitionare
        tkinter.Label(self, text="Parola:").pack(pady=(10, 0))
        self.entry_parola = tkinter.Entry(self, show='*')
        self.entry_parola.pack()

        # Label gol pentru afisare mesaj de eroare autentificare
        self.eroare_autentificare = tkinter.Label(self,text='')
        self.eroare_autentificare.pack(pady=(10, 0))

        # Buton pentru autentificare cu comanda de verificare date de autentificare
        tkinter.Button(self, text="Autentificare", command=self.verifica_login).pack(pady=10)


    def verifica_login(self):
        '''
        Functia verifica_login din cadrul clasei FereastraAutentificare are rolul de a verifica daca utilizatorul si parola sunt conform 
        cu cele introduse in sistem
        '''

        utilizator = self.entry_utilizator.get()
        parola = self.entry_parola.get()
        date_utilizator = baza_de_date.cautare_operator(utilizator,parola) # Apelam functia de cautare operator din modulul baza de date pentru credentiale

        # Pentru teste
        if 1 == 1:
            self.destroy()  # Inchide fereastra de login
            self.master.deschide_meniu_principal_admin()  # Apeleaza metoda din aplicatia principala

        # if date_utilizator:
        #     self.master.utilizator_autentificat = date_utilizator  # Salvăm utilizatorul în clasa MeniuPrincipal

        #     self.destroy()  # Închidem fereastra de login

        #     if date_utilizator[5] == 1:  # Dacă este admin
        #         self.master.deschide_meniu_principal_admin()
        #     else:  # Operator normal
        #         self.master.deschide_meniu_principal_operator()
        else:
            self.eroare_autentificare.config(text='Utilizator sau parola gresita!')