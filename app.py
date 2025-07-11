
import baza_de_date 
from meniu_principal import MeniuPrincipal

if __name__ == '__main__':
    baza_de_date.creare_tabela_operatori()
    baza_de_date.creare_tabela_pacienti()
    baza_de_date.creare_tabela_sectii()
    baza_de_date.creare_tabela_medici_trimitatori()
    baza_de_date.creare_tabela_medici_curanti()
    baza_de_date.creare_tabela_servicii()
    baza_de_date.creare_tabela_pacienti_servicii()
    baza_de_date.populare_tabela_servicii()
    app = MeniuPrincipal()
    app.mainloop()

