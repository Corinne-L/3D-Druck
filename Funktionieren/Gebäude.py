import win32com.client

# AutoCAD-Instanz starten oder verbinden
acad = win32com.client.Dispatch("AutoCAD.Application")
acad.Visible = True  # AutoCAD sichtbar machen

# DXF-Datei öffnen
filename = r"C:\Users\Corinne\OneDrive - Hochschule Luzern\3. Semester_HS24\DC_Programming\3D Druck\solid.dxf"
doc = acad.Documents.Open(filename)

def convert(doc):
    try:
        doc.SendCommand(f"_MESHSMOOTH\n_all\n\n")
        print("Befehl erfolgreich gesendet!")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")

def export(doc):
    try:
        # Export as STL
        stl_filename = r"C:\Users\Corinne\OneDrive - Hochschule Luzern\3. Semester_HS24\DC_Programming\3D Druck\solid.stl"
        doc.SendCommand(f'_STLOUT\n_all\n\n\n{stl_filename}\n\n')
        print("Befehl erfolgreich gesendet!")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")

def save_all(doc): 
    try: 
        doc.SendCommand("_QSAVE\n\n\n\n\nJ\n") 
        print("Alle Dateien erfolgreich gespeichert!") 
    except Exception as e: 
        print(f"Fehler beim Speichern der Dateien: {e}")

def close_acad(acad): 
    try: 
        acad.Quit() 
        print("AutoCAD erfolgreich geschlossen!") 
    except Exception as e: 
        print(f"Fehler beim Schließen von AutoCAD: {e}")

# Funktion aufrufen
convert(doc)
export(doc)
save_all(doc)
close_acad(acad)

