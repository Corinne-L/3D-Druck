import win32com.client
import streamlit as st



def convert(doc):
    try:
        doc.SendCommand(f"_MESHSMOOTH\n_all\n\n")
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")

def export(doc, output_stl_g):
    try:
        # Export as STL
        stl_filename = output_stl_g
        doc.SendCommand(f'_STLOUT\n_all\n\n\n{stl_filename}\n\n')
    except Exception as e:
        st.warning(f"Fehler beim Verarbeiten der Datei: {e}")

def save_all(doc): 
    try: 
        doc.SendCommand("_QSAVE\n\n\n\n\n") 
    except Exception as e: 
        st.warning(f"Fehler beim Speichern der Dateien: {e}")

def close_acad(acad): 
    try: 
        acad.Quit() 
        st.success("AutoCAD erfolgreich geschlossen!") 
    except Exception as e: 
        st.warning(f"Fehler beim Schließen von AutoCAD: {e}")



## AutoCAD-Instanz starten oder verbinden
#acad = win32com.client.Dispatch("AutoCAD.Application")
#acad.Visible = True  # AutoCAD sichtbar machen

# DXF-Datei öffnen
#filename = r"C:\Users\Corinne\OneDrive - Hochschule Luzern\3. Semester_HS24\DC_Programming\3D Druck\solid.dxf"
#doc = acad.Documents.Open(filename) 



 ## Funktion aufrufen
#convert(doc)
#export(doc)
#save_all(doc)
#close_acad(acad) 
