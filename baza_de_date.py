
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
                       CNP TEXT,
                       data_nastere TEXT,
                       varsta INTEGER,
                       sex TEXT,
                       asigurat TEXT,
                       medic_trimitator TEXT,
                       bilet_trimitere TEXT,
                       diagnostic_prezumtiv TEXT,
                       medic_curant TEXT,
                       sectie TEXT,
                       zile_spitalizare TEXT,
                       data_externarii TEXT,
                       diagnostic_confirmat TEXT,
                       alocatie_hrana TEXT,
                       recomandari TEXT,
                       plan_tratament TEXT
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

def creare_tabela_servicii():
    '''
    Functia folosita pentru crearea tabelei Servicii in care vor fi stocate serviciile efectuate de pacienti.
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicii(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       denumire_serviciu TEXT,
                       Valoare TEXT)''')
        conexiune.commit()

def creare_tabela_pacienti_servicii():
    '''
    Functia folosita pentru crearea tabelei Pacienti_Servicii in care vor fi stocate serviciile efectuate de pacienti.
    Aceasta tabela este o tabela de legatura intre pacienti si servicii.
    '''
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacienti_servicii(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       id_pacient INTEGER,
                       id_serviciu INTEGER,
                       FOREIGN KEY (id_pacient) REFERENCES Pacienti(IdPacient),
                       FOREIGN KEY (id_serviciu) REFERENCES servicii(id))''')
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
        conexiune.commit()

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

# Functia folosita pentru adaugarea pacientilor in baza de date, adaugarea internarilor si externarilor

# Introducere date

def insert_pacient(nume, prenume, cnp, data_nastere, varsta,  sex, asigurat):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(''' INSERT INTO Pacienti (nume, prenume, CNP, data_nastere, varsta, sex, asigurat)
                        VALUES (?, ?, ?, ?, ?, ?, ?) ''', (nume, prenume,  cnp, data_nastere, varsta, sex, asigurat))
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
    
def update_pacienti_date(nume, prenume, cnp, data_nastere, varsta, sex, asigurat, idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Pacienti 
                       SET nume = ? , prenume = ?, CNP = ?, data_nastere = ?, varsta = ?, sex = ?, asigurat = ?
                       WHERE IdPacient = ? AND data_externarii IS NOT NULL ''',(nume, prenume, cnp, data_nastere, varsta, sex, asigurat, idpacient))
        conexiune.commit()

def stergere_pacient_date(idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''DELETE FROM Pacienti WHERE idpacient = ?''', (idpacient,))
        conexiune.commit()

# Internare

def verificare_existent_internare(idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(''' SELECT * FROM Pacienti WHERE idpacient = ? AND SECTIE IS NOT NULL ''', (idpacient,))
        return cursor.fetchone()

def update_pacienti_internare(medic_trimitator, bilet_trimitere, diagnostic_prezumtiv, medic_curant, sectie, idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Pacienti 
                       SET medic_trimitator = ? , bilet_trimitere = ?, diagnostic_prezumtiv = ?, medic_curant = ?, sectie = ? 
                       WHERE IdPacient = ? ''',(medic_trimitator, bilet_trimitere, diagnostic_prezumtiv, medic_curant, sectie, idpacient))
        conexiune.commit()

def get_pacienti_internare():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT 
                        IdPacient,
                        nume,
                        prenume,
                        IFNULL(medic_trimitator, '') AS medic_trimitator,
                        IFNULL(bilet_trimitere, '') AS bilet_trimitere,
                        IFNULL(diagnostic_prezumtiv, '') AS diagnostic_prezumtiv,
                        IFNULL(medic_curant, '') AS medic_curant,
                        IFNULL(sectie, '') AS sectie
                        FROM Pacienti
                    ''')
        return cursor.fetchall()

def get_pacient_pentru_prezentare(idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT 
                        nume,
                        prenume,
                        cnp,
                        data_nastere,
                        varsta,
                        CASE
                            WHEN sex = 'F' THEN 'Feminin'
                            WHEN sex = 'M' THEN 'Masculin'
                            ELSE 'none'
                            END AS sex,
                        CASE
                            WHEN asigurat = '1' THEN 'Asigurat'
                            WHEN asigurat = '0' THEN 'Neasigurat'
                            ELSE 'none'
                            END AS asigurat
                        FROM Pacienti WHERE IdPacient = ?
                    ''',(idpacient,))
        return cursor.fetchone()

def stergere_internare(idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Pacienti 
                       SET medic_trimitator = ? , bilet_trimitere = ?, diagnostic_prezumtiv = ?, medic_curant = ?, sectie = ? 
                       WHERE IdPacient = ?  AND data_externarii IS NULL ''',('', '', '', '', '', idpacient))
        conexiune.commit()

# Externare

def get_pacienti_externare():
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''SELECT 
                        IdPacient,
                        nume,
                        prenume,
                        IFNULL(zile_spitalizare, '') AS zile_spitalizare,
                        IFNULL(data_externarii, '') AS data_externarii,
                        IFNULL(diagnostic_confirmat, '') AS diagnostic_confirmat,
                        IFNULL(alocatie_hrana, '') AS alocatie_hrana,
                        IFNULL(recomandari, '') AS recomandari,
                        IFNULL(plan_tratament, '') AS plan_tratament
                        FROM Pacienti
                    ''')
        return cursor.fetchall()

def verificare_existent_externare(idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(''' SELECT * FROM Pacienti WHERE idpacient = ? AND data_externarii IS NOT NULL  ''', (idpacient,))
        return cursor.fetchone()

def update_pacienti_externare(zile_spitalizare, data_externarii, diagnostic_confirmat, alocatie_hrana, recomandari, plan_tratament, idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Pacienti 
                       SET zile_spitalizare = ?, data_externarii = ? , diagnostic_confirmat = ? , alocatie_hrana = ?, recomandari = ?, plan_tratament = ?
                       WHERE IdPacient = ? ''',(zile_spitalizare, data_externarii, diagnostic_confirmat, alocatie_hrana, recomandari, plan_tratament, idpacient))
        conexiune.commit()

def stergere_externare(idpacient):
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute('''UPDATE Pacienti 
                       SET zile_spitalizare = ?, data_externarii = ? , diagnostic_confirmat = ? , alocatie_hrana = ?, recomandari = ?, plan_tratament = ?
                       WHERE IdPacient = ? ''',('', '', '', '', '', '' , idpacient))
        conexiune.commit()

def cautare_pacient():
    pass

def get_lista_servicii():
    """
    Returneaza o lista de servicii disponibile din baza de date.
    Return: lista de tuple (id_serviciu, nume_serviciu)
    """
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute("SELECT id, denumire_serviciu, valoare FROM servicii")
        rezultate = cursor.fetchall()
        return rezultate

def adauga_serviciu_la_pacient(id_pacient, id_serviciu):
    """
    Adauga o inregistrare in tabela de legatura intre pacient si serviciu.
    """
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(
            "INSERT INTO pacienti_servicii (id_pacient, id_serviciu) VALUES (?, ?)",
            (id_pacient, id_serviciu)
        )
        conexiune.commit()

def get_servicii_pacient(id_pacient):
    """
    Returneaza o lista de tuple (id_serviciu, denumire, valoare) pentru serviciile adaugate pacientului.
    """
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute("""
        SELECT s.id, s.denumire_serviciu, s.valoare
        FROM servicii s
        JOIN pacienti_servicii ps ON s.id = ps.id_serviciu
        WHERE ps.id_pacient = ?
    """, (id_pacient,))
    rezultate = cursor.fetchall()
    return rezultate

def sterge_serviciu_pacient(id_pacient, id_serviciu):
    """
    Sterge serviciul cu id_serviciu pentru pacientul cu id_pacient din tabela de legatura.
    """
    with conectare_baza_date() as conexiune:
        cursor = conexiune.cursor()
        cursor.execute(
        ''' DELETE FROM pacienti_servicii WHERE id_pacient = ? AND id_serviciu = ? ''',
        (id_pacient, id_serviciu)
    )
        conexiune.commit()
