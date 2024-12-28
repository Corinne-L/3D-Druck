import win32com.client
import streamlit as st

""" from Funktionieren.Gebäude import save_all, close_acad """



def explode(doc):
    try:
        doc.SendCommand(f"_EXPLODE\n_all\n\n")
        st.success("Befehl erfolgreich gesendet!")
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")

def Netz(doc):
    try:
        doc.SendCommand(f"_MESHSMOOTH\n_all\n\n")
        st.success("Befehl erfolgreich gesendet!")
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")

def to_surface(doc):
    try:
        doc.SendCommand(f"_convtosurface\n_all\n\n")
        st.success("Befehl erfolgreich gesendet!")
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")

def extrude(doc):
    try:
        doc.SendCommand(f"_extrude\n_all\n\nr\n0,0,0\n0,0,-1\n")
        st.success("Befehl erfolgreich gesendet!")
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")

def export_d(doc, output_stl):
    try:
        # Export as STL
        stl_filename = output_stl
        doc.SendCommand(f'_STLOUT\n_all\n\n\n{stl_filename}\n\n')
        st.success("Befehl erfolgreich gesendet!")
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")


""" # AutoCAD-Instanz starten oder verbinden
acad = win32com.client.Dispatch("AutoCAD.Application")
acad.Visible = True  # AutoCAD sichtbar machen

# DXF-Datei öffnen
filename = r"C:\Users\Corinne\OneDrive - Hochschule Luzern\3. Semester_HS24\DC_Programming\3D Druck\block2.dxf"
doc = acad.Documents.Open(filename)
output_stl =r"C:\Users\Corinne\OneDrive - Hochschule Luzern\3. Semester_HS24\DC_Programming\3D Druck\dach.stl" """


""" # Funktion aufrufen
explode(doc)
Netz(doc)
to_surface(doc)
extrude(doc)
export_d(doc)
save_all(doc)
close_acad(acad) """


