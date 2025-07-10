import tkinter
import utilities
from baza_de_date import get_pacient_rapoarte
from tkinter import ttk

'''
Modulul fereastra_rapoarte este folosita pentru vizualizarea, tiparirea si exportul rapoartelor.

'''

class FereastraRapoarte(tkinter.Toplevel):
    def __init__(self, master): # Initializare constructor pentru clasa Fereastra Rapoarte (reprezinta tkinter.TopLevel - clasa copil pentru tkinter.Tk)
        super().__init__(master) # Initializare constructor pentru clasa parinte (adica pentru clasa MeniuPrincipal - care reprezinta tkinter.Tk (clasa principala - radacina))
        self.title('Rapoarte') # Numele ferestrei
        self.resizable(False, False) # Dimensiunea nu este modificabila
        self.update_idletasks() # Asteapta initializarea completa a aplicatiei si abia apoi o deschide
        self.geometry(utilities.pozitionare_fereastra_pe_ecran(self,800,600)) # Setam geometria si centrarea pe ecran folosind functia pozitionare_fereastra_pe_ecran cu parametrii fiind dimensiunea dorita a ferestrei

        self.id_pacient = None

        # frame-ul ferestrei folosit pentru centrare
        self.frame_fereastra=tkinter.Frame(self)
        self.frame_fereastra.pack(padx=25,pady=10)


        # frame-ul privind pacientul
        self.frame_pacient = tkinter.Frame(self.frame_fereastra)
        self.frame_pacient.grid(column=0,row=0,padx=5,pady=5)

        tkinter.Label(self.frame_pacient,text='Selectati un pacient din lista: ').pack(pady=5)
        combobox_pacienti = ttk.Combobox(self.frame_pacient,
                                          values=self.unpack_pacienti(),width=65) # Apeleaza functia unpack_pacienti pentru a obtine lista de pacienti
        combobox_pacienti.pack(pady=5)

        # Frameul cu butoane
        self.frame_butoane = tkinter.Frame(self.frame_fereastra)
        self.frame_butoane.grid(column=1,row=0,padx=5,pady=5)

        tkinter.Button(self.frame_butoane,text='Generare fisa externare').pack(pady=10)
        tkinter.Button(self.frame_butoane,text='Generare decont pacient').pack(pady=10)


        # Frameul cu text
        self.frame_text = tkinter.Frame(self.frame_fereastra)
        self.frame_text.grid(column=0,row=1,columnspan=2,padx=5,pady=5)

        self.text = tkinter.Text(self.frame_text)
        self.text.pack(pady=5)

        # Butonul de salvare
        tkinter.Button(self, text='Salvare', width=20).pack(padx=5,pady=5)


    def unpack_pacienti(self):
        pacienti = get_pacient_rapoarte()
        
        print(self.id_pacient)

        if pacienti is None:
            return ''
        else:
            return [f'{pacient[0]} / {pacient[1]} {pacient[2]} / {pacient[3]} / INT: {pacient[8]} / EXT: {pacient[13]}' for pacient in pacienti]

        
