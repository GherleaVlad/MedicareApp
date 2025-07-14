# MedicareApp

## English

**MedicareApp** is a desktop application for managing patient admissions and clinical records. The project is written in **Python**, using **Tkinter** for the graphical user interface and **SQLite** for data storage.

### Features
- Secure login for administrators and operators
- Patient management: add, update, and delete personal data
- Record hospital admissions and discharges
- Manage medical staff and clinic departments
- View active admissions with filtering and export (CSV/JSON)
- Generate discharge summaries and billing reports
- Simple, intuitive interface suitable for clinics and small hospitals

### Technologies Used
- Python 3.x
- Tkinter (GUI)
- SQLite3 (database)
- JSON and CSV file handling

### How to Run the Application
```bash
python app.py
```
The `medicare.db` database file is automatically created if it does not already exist.

### Project Structure (Recommended)
```
MedicareApp/
│
├── app.py                  # Main application launcher
├── database/               # DB logic and initialization
├── gui/                    # GUI components (Tkinter windows)
├── models/                 # Business logic and data models
├── resources/              # Icons, images, etc.
└── exports/                # CSV/JSON exports (optional)
```

---

## Română

**MedicareApp** este o aplicație desktop pentru gestionarea internărilor și a evidențelor medicale ale pacienților. Proiectul este scris în **Python**, interfața fiind realizată cu **Tkinter**, iar datele sunt stocate în **SQLite**.

### Funcționalități
- Autentificare securizată pentru administratori și operatori
- Administrarea pacienților: adăugare, modificare și ștergere de date personale
- Înregistrarea internărilor și externărilor din clinică
- Gestiunea personalului medical și a secțiilor clinice
- Vizualizarea internărilor active cu opțiuni de filtrare și export (CSV/JSON)
- Generarea fișelor de externare și a deconturilor
- Interfață simplă și intuitivă, potrivită pentru cabinete sau clinici mici

### Tehnologii Utilizate
- Python 3.x
- Tkinter (interfață grafică)
- SQLite3 (bază de date)
- Gestionare fișiere JSON și CSV

### Rulare Aplicație
```bash
python app.py
```
Fișierul `medicare.db` va fi creat automat dacă nu există deja în directorul aplicației.

### Structură Recomandată a Proiectului
```
MedicareApp/
│
├── app.py                  # Lansatorul principal al aplicației
├── database/               # Inițializarea bazei de date și logica SQL
├── gui/                    # Ferestrele aplicației (Tkinter)
├── models/                 # Logica aplicației și clasele de date
├── resources/              # Resurse (iconițe, imagini etc.)
└── exports/                # Exporturi CSV/JSON (opțional)
```


