import ezdxf
import tempfile
import os
import streamlit as st

# Funktion zum Filtern und Entfernen von Entitäten basierend auf Layern
def split_and_remove_entities(dxf_split, layers_to_remove):
    # Überprüfe, ob dxf_split eine Datei ist und Inhalt enthält
    if dxf_split is None:
        st.error("Die DXF-Datei wurde nicht hochgeladen oder ist leer.")
        st.stop()  # Stoppt die Ausführung

    try:
        # Temporäre Datei erstellen
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as temp_dxf:
            temp_dxf.write(dxf_split.read())  # Schreiben des Inhalts in die temporäre Datei
            temp_dxf_path = temp_dxf.name  # Pfad zur temporären Datei
    except Exception as e:
        st.error(f"Fehler beim Erstellen der temporären Datei: {e}")
        st.stop()  # Stoppt die Ausführung

    try:
        # DXF-Datei einlesen
        doc = ezdxf.readfile(temp_dxf_path)
    except ezdxf.DXFError as e:
        st.error(f"Fehler beim Lesen der DXF-Datei: {e}")
        os.remove(temp_dxf_path)  # Temporäre Datei löschen
        st.stop()  # Stoppt die Ausführung

    msp = doc.modelspace()

    # Liste, um die gewünschten Entitäten zu speichern
    entities_to_export = []

    # Entitäten sammeln und aus dem Modelspace entfernen
    for entity in list(msp):
        if entity.dxf.layer in layers_to_remove:
            entities_to_export.append(entity)
            msp.delete_entity(entity)

    os.remove(temp_dxf_path)  # Temporäre Datei löschen
    return doc, entities_to_export

def save_dxf(doc, output_file):
    # DXF speichern
    doc.saveas(output_file)
    print(f"Datei gespeichert: {output_file}")

""" # Dateinamen
dxf_split = "Häuser.dxf"
output_file_gebaeude = "Gebäude.dxf"
output_file_dach = "Dächer.dxf"

# Layer-Listen definieren
layers_dach = [
    "Roof_Gebaeude Einzelhaus", "Roof_Gebaeude unsichtbar", 
    "Roof_Kapelle", "Roof_Lagertank", 
    "Roof_Lueftungsschacht", "Roof_Mauer gross",
    "Roof_Offenes Gebaeude", "Roof_Sakrales Gebaeude", "0"
]

layers_gebaeude = [
    "Build_Gebaeude Einzelhaus", "Build_Gebaeude unsichtbar",
    "Build_Kapelle", "Build_Lagertank", 
    "Build_Lueftungsschacht", "Build_Mauer gross", "Build_Sakrales Gebaeude","0"
]

# Dächer exportieren
doc_dach, Dach = split_and_remove_entities(dxf_split, layers_gebaeude)
if Dach:
    save_dxf(doc_dach, output_file_dach)
else:
    print("Keine Dächer gefunden.")

# Gebäude exportieren
doc_gebaeude, Gebäude = split_and_remove_entities(dxf_split, layers_dach)
if Gebäude:
    save_dxf(doc_gebaeude, output_file_gebaeude)
else:
    print("Keine Gebäude gefunden.") """
