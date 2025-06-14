
'''
Modulul baza_de_date reprezinta fisierul .py in care sunt stocate toate operatiunile legate de baza de date si anume operatiunea de conectare, operatiunile de creare a structurii tabelei
respectiv operatiunile CRUD (create, read, update, delete).
'''

import sqlite3

# Conectarea la baza de date
def conectare_baza_date():
    conn = sqlite3.connect('medicare.db')
    return conn

# Crearea tabelelor din baza de date - complet mai putin tabela pacient (idk)

def creare_tabela_operatori():
    '''
    Functia folosita pentru crearea tabelei unde vor fi stocati utilizatorii in baza de date.
    IdOperator este cheia primata a tabelei Operatori. utilizator si parola reprezinta datele de acces in aplicatie. Administrator este o coloana
    care o sa accepte valori de tip 0 sau 1 pentru a determina daca un operator care se creaza sau logheaza este admin sau nu (folosim integer pentru ca
    in sqllite nu avem in baza de date valori de tip bit)
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Operatori(
                       IdOperator INTEGER PRIMARY KEY AUTOINCREMENT,
                       utilizator TEXT,
                       parola TEXT,
                       nume TEXT,
                       prenume TEXT,
                       sectie TEXT,
                       activ TEXT)''')
        conexiune.commit()

def creare_tabela_pacienti():
    '''
    Functia folosita pentru crearea tabelei unde vor fi stocati pacientii in baza de date.
    IdPacient este cheia primara a tabelei Pacienti. Restul coloanelor reprezinta entry-urile introduse de catre utilizator
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pacienti(
                       IdPacient INTEGER PRIMARY KEY AUTOINCREMENT,
                       nume TEXT,
                       prenume TEXT,
                       data_nastere TEXT,
                       varsta INTEGER,
                       CNP INTEGER,
                       sex TEXT,
                       asigurat TEXT
                       )
                       ''')
        conexiune.commit()

def creare_tabela_sectii():
    '''
    Functia folosita pentru crearea tabelei Sectii in care vor fi stocate sectiile clinicii.
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sectii(
                       IdSectie INTEGER PRIMARY KEY AUTOINCREMENT,
                       denumire TEXT,
                       sef_sectie TEXT)''')
        conexiune.commit()

def creare_tabela_medici_trimitatori():
    '''
    Functia folosita pentru crearea tabelei Medici_Trimitatori in care vor fi stocati medicii trimitatori (nomenclator national de medici).
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Medici_Trimitatori(
                       IdMedicTrimitator INTEGER PRIMARY KEY AUTOINCREMENT,
                       nume TEXT,
                       prenume TEXT,
                       parafa TEXT,
                       activ TEXT)''')
        conexiune.commit()

def creare_tabela_medici_curanti():
    '''
    Functia folosita pentru crearea tabelei Medici_Curanti in care vor fi medicii curanti (medicii din cadrul clinicii).
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Medici_Curanti(
                       IdMedicCurant INTEGER PRIMARY KEY AUTOINCREMENT,
                       nume TEXT,
                       prenume TEXT,
                       parafa TEXT,
                       activ TEXT)''')
        conexiune.commit()

# Functii pentru operatiuni CRUD (create, read, update, delete) pentru tabelele: Sectii, Medici_Curanti, Medici_Trimitatori, Operatori, Pacienti

# Tabela Sectii - complet

def insert_sectie(sectie,sef_sectie):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''INSERT INTO Sectii (denumire, sef_sectie)
                        VALUES (?,?)''', (sectie,sef_sectie))
        conexiune.commit()

def verificare_sectie(sectie):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Sectii WHERE denumire = ? ''' , (sectie,))  
        return cursor.fetchone()

def get_sectii():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Sectii''')
        return cursor.fetchall()
    
def update_sectii(sef_sectie,idsectie):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Sectii SET sef_sectie = ? WHERE IdSectie = ? ''', (sef_sectie,idsectie))
        conexiune.commit()

# Tabela Medici_Curanti

def insert_medic_curant(nume, prenume, parafa, activ):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''INSERT INTO Medici_Curanti (nume, prenume, parafa, activ)
                        VALUES (?,?,?,?)''', (nume, prenume, parafa, activ))
        conexiune.commit()

def update_medic_curant(nume, prenume, activ, id_medic):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Medici_Curanti SET nume = ?, prenume = ?, activ = ? WHERE IdMedicCurant = ? ''', (nume,prenume,activ,id_medic))
        conexiune.commit()

def get_medici_curanti():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Medici_Curanti''')
        return cursor.fetchall()

def verificare_existenta_medic_curant(parafa):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Medici_Curanti WHERE parafa = ?''',(parafa,))
        return cursor.fetchone()
    
# Tabela Medici_Trimitatori

def insert_medic_trimitator(nume, prenume, parafa):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''INSERT INTO Medici_Trimitatori (nume, prenume, parafa, activ)
                        VALUES (?,?,?,?)''', (nume, prenume, parafa, '1'))
        conexiune.commit()

def update_medic_trimitator(nume, prenume, id_medic):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Medici_Trimitatori SET nume = ?, prenume = ? WHERE IdMedicTrimitator = ? ''', (nume, prenume,id_medic))
        conexiune.commit()

def get_medici_trimitatori():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Medici_Trimitatori''')
        return cursor.fetchall()
    
def verificare_existenta_medic_trimitator(parafa):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Medici_Trimitatori WHERE parafa = ?''',(parafa,))
        return cursor.fetchone()    

def update_parafe_inexistente(parafa):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Medici_Trimitatori SET activ = ? WHERE parafa = ? ''', ('0', parafa))
        conexiune.commit()


# Tabela Operatori

def cautare_operator(utilizator, parola): 
    ''' Functia utilizata pentru verificarea datelor de conectare in aplicatie '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('SELECT * FROM Operatori WHERE utilizator = ? AND parola = ?',(utilizator,parola))
        return cursor.fetchone()

def insert_operator(utilizator, parola, nume, prenume, sectie):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''INSERT INTO Operatori (utilizator, parola , nume, prenume, sectie, activ)
                        VALUES (?,?,?,?,?,?)''', (utilizator, parola, nume, prenume, sectie, '1'))
        conexiune.commit()

def update_operator(nume, prenume, sectie, idoperator):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Operatori SET nume = ? , prenume = ?, sectie = ? WHERE IdOperator = ? ''', (nume, prenume, sectie, idoperator))
        conexiune.commit()

def inactivare_operator(idoperator):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(''' UPDATE Operatori SET activ = ? WHERE IdOperator = ? ''' , ('0',idoperator))

def verificare_operator_dupa_utilizator(utilizator):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Operatori WHERE utilizator = ? ''' , (utilizator,))  
        return cursor.fetchone()

def verificare_operator_dupa_nume_prenume(nume, prenume):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Operatori WHERE nume = ? AND prenume = ? ''' , (nume,prenume))  
        return cursor.fetchone()

def get_operatori():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Operatori''')
        return cursor.fetchall()

# Functia folosita pentru adaugarea pacientilor in baza de date


def insert_pacient(nume, prenume, data_nastere, varsta, cnp, sex, asigurat):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(''' INSERT INTO Pacienti (nume, prenume, data_nastere, varsta, CNP, sex, asigurat)
                        VALUES (?, ?, ?, ?, ?, ?, ?) ''', (nume, prenume, data_nastere, varsta, cnp, sex, asigurat))
        conexiune.commit()

def verificare_existenta_pacient(cnp):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT * FROM Pacienti WHERE CNP = ? ORDER BY IdPacient''' , (cnp,))  
        return cursor.fetchone()

def get_pacienti():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(''' SELECT * FROM Pacienti ''')
        return cursor.fetchall()
    
def update_pacienti():
    pass

def cautare_pacient():
    pass




