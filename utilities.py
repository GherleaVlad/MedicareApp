'''
Modul folosit pentru stocarea functiilor utiliare - adica functii generale cu diferite aplicabilitati si refolosibile in diferite
contexte din aplicatie
'''

from datetime import datetime
from baza_de_date import get_medici_curanti,get_sectii,get_medici_trimitatori
import os

def pozitionare_fereastra_pe_ecran(fereastra,latime_fereastra,inaltime_fereastra):
    '''
    Functia care calculeaza si returneaza pozitionarea pe ecran a unei ferestre a aplicatiei astfel incat, aceasta indiferent de 
    dimensiunile ei sa fie centrata. Functia primeste 3 parametri si anume: 
    
    1. fereastra - care reprezinta obiectul tkinter (meniu principal (tkinter.Tk) sau fereastra de login(tkinter.TopLevel) pentru a sti la care fereastra se
    face referirea) 
    2. latime_fereastra - latimea dorita pentru o anumita fereastra
    3. inaltime_fereastra - inaltime dorita pentru o anumita fereastra

    Functia returneaza un f string care va fi folosit in cadrul metodei geometry a unei ferestre

    '''

    latime = latime_fereastra
    inaltime = inaltime_fereastra

    latime_ecran = fereastra.winfo_screenwidth()
    inaltime_ecran = fereastra.winfo_screenheight()

    pozitie_x = (latime_ecran - latime) // 2
    pozitie_y = (inaltime_ecran - inaltime) // 2

    return (f"{latime}x{inaltime}+{pozitie_x}+{pozitie_y}")

def data_curenta():
    datacurenta = datetime.today()
    data_formatata = datacurenta.strftime("%d.%m.%Y")
    return data_formatata

def unpack_medici():
    medici = get_medici_curanti()
    
    if medici is None:
        return ''
    else:
        return [f'{medic[1]}  {medic[2]} - {medic[3]}' for medic in medici]

def unpack_sectii():
    sectii = get_sectii()
    
    if sectii is None:
        return ''
    else:
        return [sectie[1] for sectie in sectii]

def unpack_medici_trimitatori():
    medici = get_medici_trimitatori()
    
    if medici is None:
        return ''
    else:
        return [f'{medic[1]}  {medic[2]} - {medic[3]}' for medic in medici]
    
def get_icon_path():
    dirpath = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(dirpath,'Logo.ico')
    return icon_path

