'''
Modul folosit pentru stocarea functiilor utiliare - adica functii generale cu diferite aplicabilitati si refolosibile in diferite
contexte din aplicatie
'''

from datetime import datetime


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


