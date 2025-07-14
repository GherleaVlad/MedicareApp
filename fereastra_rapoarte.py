import tkinter
import utilities
from baza_de_date import get_pacient_rapoarte, get_pacient_fisa_externare, get_pacient_decont
from tkinter import ttk
from tkinter import messagebox, filedialog

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
        self.iconbitmap(r'C:\Users\vladg\OneDrive\Documents\GitHub\MedicareApp\Logo.ico') # Setam iconita aplicatiei
        
        self.id_pacient = None

        # frame-ul ferestrei folosit pentru centrare
        self.frame_fereastra=tkinter.Frame(self)
        self.frame_fereastra.pack(padx=25,pady=10)


        # frame-ul privind pacientul
        self.frame_pacient = tkinter.Frame(self.frame_fereastra)
        self.frame_pacient.grid(column=0,row=0,padx=5,pady=5)

        tkinter.Label(self.frame_pacient,text='Selectati un pacient din lista: ').pack(pady=5)
        self.combobox_pacienti = ttk.Combobox(self.frame_pacient,
                                          values=self.unpack_pacienti(),width=65) # Apeleaza functia unpack_pacienti pentru a obtine lista de pacienti
        self.combobox_pacienti.pack(pady=5)

        self.combobox_pacienti.bind("<<ComboboxSelected>>", self.get_selected)

        # Frameul cu butoane
        self.frame_butoane = tkinter.Frame(self.frame_fereastra)
        self.frame_butoane.grid(column=1,row=0,padx=5,pady=5)

        tkinter.Button(self.frame_butoane,text='Generare fisa externare', command=lambda: self.generare_fisa_externare()).pack(pady=10)
        tkinter.Button(self.frame_butoane,text='Generare decont pacient', command=lambda: self.generare_decont_pacient()).pack(pady=10)

        # Frameul cu text
        self.frame_text = tkinter.Frame(self.frame_fereastra)
        self.frame_text.grid(column=0,row=1,columnspan=2,padx=5,pady=5)

        self.text = tkinter.Text(self.frame_text)
        self.text.pack(pady=5)

        # Butonul de salvare
        tkinter.Button(self, text='Salvare', command=lambda: self.salvare_text(),width=20).pack(padx=5,pady=5)

    def unpack_pacienti(self):
        pacienti = get_pacient_rapoarte()

        if pacienti is None:
            return ''
        else:
            return [f'{pacient[0]} / {pacient[1]} {pacient[2]} / {pacient[3]} / INT: {pacient[8]} / EXT: {pacient[13]}' for pacient in pacienti]
        
    def get_selected(self, event):
        pacient = self.combobox_pacienti.get()
        if pacient:
            self.id_pacient = pacient[0]

    def generare_fisa_externare(self):
        
        date_externare = get_pacient_fisa_externare(self.id_pacient)

        if self.id_pacient is None:
            messagebox.showerror('EROARE', 'Selectati un pacient din lista!', parent = self)
            return
        
        else:

            if date_externare is None:
                messagebox.showerror('EROARE', 'Nu exista date de externare pentru acest pacient!', parent = self)
                return
            
            else:
                fisa_externare = f'''
            Fisa de externare

Nume pacient: {date_externare[1]}                       Recomandari:
Prenume pacient: {date_externare[2]}                    {date_externare[17]}
CNP: {date_externare[3]}
Nascut la : {date_externare[4]}
Varsta: {date_externare[5]} ani
Sex: {date_externare[6]}
{date_externare[7]}

Internat la data de: {date_externare[8]}                Plan de tratament:
In cadrul sectiei: {date_externare[9]}                  {date_externare[18]}

In baza biletului de trimitere: {date_externare[10]}
Trimis de: {date_externare[11]}
Diagnostic prezumtiv: {date_externare[12]}

Medic curant: {date_externare[13]}
Numarul zilelor de spitalizare: {date_externare[14]}
Diagnostic confirmat: {date_externare[15]}

Externat la data de: {date_externare[16]}
'''

                self.text.delete(1.0, tkinter.END)
                self.text.insert(tkinter.END, fisa_externare)

    def generare_decont_pacient(self):
        
        date_decont = get_pacient_decont(self.id_pacient)

        zile_spitalizare = int(date_decont[1][6])
        alocatie_hrana = date_decont[1][7]


        alocatie_hrana_total = alocatie_hrana * zile_spitalizare

        lista_servicii = list()
        

        valoare_totala_servicii = 0

        for servicii in date_decont:
            lista_servicii.append(f'{servicii[8]} - {servicii[9]}')
            valoare_totala_servicii += float(servicii[9])

        valoare_totala_decont = alocatie_hrana_total+valoare_totala_servicii

        lista_servicii_de_afisat = '\n'.join(lista_servicii)


        if self.id_pacient is None:
            messagebox.showerror('EROARE', 'Selectati un pacient din lista!', parent = self)
            return
        
        else:

            if date_decont is None:
                messagebox.showerror('EROARE', 'Nu exista date de externare pentru acest pacient!', parent = self)
                return

            fisa_decont = f'''
            Decont pacient

Pacientului {date_decont[1][1]} {date_decont[1][2]}, detinator al codului numeric personal
{date_decont[1][3]}, nascut la data {date_decont[1][4]}, in varsta de {date_decont[1][5]} ani,
a fost spitalizat pe o durata de {zile_spitalizare} zile.

Alocatia de hrana atribuita pacientului a fost in valoare de {alocatie_hrana} lei/zi.

Costul total al hranei pe perioada spitalizarii este de: {alocatie_hrana_total} lei.

Serviciile efectuate pacientului sunt: 
{lista_servicii_de_afisat}

Costul total cu serviciile efectuate pacientului sunt in valoare de: {valoare_totala_servicii} lei.

Valoarea totala a decontului: {valoare_totala_decont} lei.

            '''

            self.text.delete(1.0, tkinter.END)
            self.text.insert(tkinter.END, fisa_decont)

    def salvare_text(self):
        continut = self.text.get("1.0", tkinter.END).strip()
        if not continut:
            messagebox.showwarning("ATENTIE", "Nu exista continut de salvat!", parent=self)
            return
        
        fisier = filedialog.asksaveasfilename(
            parent=self,
            title="Salveaza raportul",
            defaultextension=".txt",
            filetypes=[("Fisier text", "*.txt")]
            )
        
        if fisier:
            try:
                with open(fisier, "w", encoding="utf-8") as f:
                    f.write(continut)
                messagebox.showinfo("INFO", "Raportul a fost salvat!", parent=self)
            except Exception as e:
                messagebox.showerror("EROARE", f"Eroare la salvare: {e}", parent=self)

