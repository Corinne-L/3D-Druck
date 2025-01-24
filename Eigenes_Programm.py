import numpy as np
import streamlit as st
import pandas as pd
import io
import os
import pythoncom
import win32com.client

# Definitionen von Funktionen und Klassen
from Funktionieren.PW_filterung import load_perimeter, load_xyz, filter_points_in_rectangle, save_xyz
from Funktionieren.Splitter import save_dxf, split_and_remove_entities
from Funktionieren.Gebäude import save_all, close_acad, convert, export 
from Funktionieren.Dach_extruden_acad import explode, Netz, to_surface,extrude, export_d, filedia
from Funktionieren.STL_zusammenführen import combine_stl_files 
from Funktionieren.mesh_aus_pw import create_stl_with_flat_base_and_terrain


# Definition Variablen mit Standardwerten
output_folder = ()
output_file_gebaeude = "Gebäude.dxf"
output_file_dach = "Dächer.dxf"
output_filename = "gefilterte_PW.xyz"
output_file_gelaende = "Gelände.stl"
output_file_gesamt = "kombiniert.stl"

# Initialisiere den Seitenzustand
if 'page' not in st.session_state:
    st.session_state.page = "define_output"

if 'output_folder' not in st.session_state:
    st.session_state.output_folder = None

# Streamlit App
st.title("3D Druck erstellen")
st.write("Diese Anwendung dient dazu, ein geschichtetes 3D-Modell zu erstellen, welches anschliessend gedruckt werden kann.")

# Speicherort am Anfang definieren
if st.session_state.page == "define_output":
    st.header("Speicherort definieren")
    output_folder = os.path.join(st.text_input("Gib den Speicherort für die Ausgabedateien an:"), "output")

    if st.button("Speicherort bestätigen"):
        if output_folder != "output":
            try:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)  # Verzeichnis erstellen, falls nicht vorhanden
                st.session_state.output_folder = output_folder
                st.session_state.update(page="start")
            except Exception as e:
                st.error(f"Fehler beim Erstellen des Verzeichnisses: {e}")
        else:
            st.error("Bitte einen gültigen Speicherort eingeben.")

# Startseite: Schritt 1: Dateien hochladen
elif st.session_state.page == "start":
    st.success(f"Speicherort wurde auf {st.session_state.output_folder} gesetzt.")
    st.header("1. Dateien hochladen")
    xyz_filename = st.file_uploader("Lade hier die XYZ-Datei hoch", type="xyz")
    dxf_filename = st.file_uploader("Lade hier die Perimeter-Datei hoch", type="dxf")

    # Schritt 2: Verarbeitung der Dateien
    if xyz_filename and dxf_filename:
        try:
            # Speicherort festlegen
            output_filename = os.path.join(st.session_state.output_folder, "gefilterte_PW.xyz")
            
            # Dateien laden und verarbeiten
            min_x, max_x, min_y, max_y = load_perimeter(dxf_filename)
            points = load_xyz(xyz_filename)
            filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)

            # Die gefilterte Punktwolke automatisch speichern
            save_xyz(output_filename, filtered_points)

            # Bestätigung anzeigen, dass die Datei gespeichert wurde
            st.success(f"Die gefilterte Punktwolke wurde erfolgreich als gefilterte_PW.xyz gespeichert.")
            if st.button("Nächster Schritt", on_click=lambda: st.session_state.update(page="page_1")):
                pass

        except Exception as e:
            st.error(f"Fehler: {e}")

# Seite 1 anzeigen (nach dem Speichern), 
# Schritt 3
elif st.session_state.page == "page_1":
    st.header("2. Splitting der Gebäude in Rumpf und Dach")
    dxf_split = st.file_uploader("Lade hier die **Seperated** Gebäude Datei hoch", type="dxf")
    dxf_split_g = st.file_uploader("Lade hier die **Solid** Gebäude Datei hoch", type="dxf")

    # Layer, die gelöscht werden für Gebäude
    layers_dach = [
        "Roof_Gebaeude Einzelhaus", "Roof_Gebaeude unsichtbar", 
        "Roof_Kapelle", "Roof_Lagertank", 
        "Roof_Lueftungsschacht", "Roof_Mauer gross",
        "Roof_Offenes Gebaeude", "Roof_Sakrales Gebaeude", "0"
    ]
    layers_gebaeude = [
        "Wall", "Floor", "0"
    ]
    
    # Schritt 4: Verarbeitung der Dateien
    if dxf_split and dxf_split_g:
        st.info("Einen Moment bitte, die Daten werden verarbeitet")
        try:
            # Speicherorte festlegen
            output_file_dach = os.path.join(st.session_state.output_folder, "Dächer.dxf")
            output_file_gebaeude = os.path.join(st.session_state.output_folder, "Gebäude.dxf")
            
            # Filterung Dach
            doc_dach, Dach = split_and_remove_entities(dxf_split, layers_gebaeude)
            if Dach:
                save_dxf(doc_dach, output_file_dach)
                st.success(f"Dächer erfolgreich gespeichert als: Dächer.dxf.")
            else:
                st.warning("Keine Dächer gefunden.")

            # Filterung Gebäude
            doc_gebaeude, Gebäude = split_and_remove_entities(dxf_split_g, layers_dach)
            if Gebäude:
                save_dxf(doc_gebaeude, output_file_gebaeude)
                st.success(f"Gebäude erfolgreich gespeichert als: Gebäude.dxf.")
            else:
                st.warning("Keine Gebäude gefunden.")
        
        except Exception as e:
            st.error(f"Fehler: {e}")
        

        try:
            pythoncom.CoInitialize()
            
            # AutoCAD-Instanz starten oder verbinden
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True  # AutoCAD sichtbar machen

            # DXF-Datei öffnen
            st.info(f"Öffne DXF-Datei: {output_file_dach}")
            doc = acad.Documents.Open(output_file_dach)
            
            # Speicherort für die STL-Datei
            output_stl = os.path.join(st.session_state.output_folder, "Dach.stl")

            filedia(doc)
            explode(doc)
            Netz(doc)
            to_surface(doc)
            extrude(doc)
            export_d(doc, output_stl)
            save_all(doc)

            st.success(f"STL-Datei wurde erfolgreich erstellt und als Dach.stl gespeichert")


        except Exception as e:
            st.error(f"Fehler während der Verarbeitung in AutoCAD:: {e}")


        try:
            pythoncom.CoInitialize()
            
            # AutoCAD-Instanz starten oder verbinden
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True  # AutoCAD sichtbar machen

            # DXF-Datei öffnen
            st.info(f"Öffne DXF-Datei: {output_file_gebaeude}")
            doc = acad.Documents.Open(output_file_gebaeude)
            
            # Speicherort für die STL-Datei
            output_stl_g = os.path.join(st.session_state.output_folder, "Gebaede.stl")

            convert(doc)
            export(doc, output_stl_g)
            save_all(doc)
            close_acad(acad)

            st.success(f"STL-Datei wurde erfolgreich erstellt und als Gebaude.stl gespeichert")

        except Exception as e:
            st.error(f"Fehler während der Verarbeitung in AutoCAD:: {e}")

        try:
            # Punktwolke laden
            points = load_xyz("gefilterte_PW.xyz")
            if points is None:
                st.error("Die Punktwolke konnte nicht geladen werden. Das Programm wird beendet.")
            else:
                # Z-Koordinaten für Gelände
                x, y, z = points[:, 0], points[:, 1], points[:, 2]
                min_z, max_z = int(np.floor(np.min(z))), int(np.ceil(np.max(z)))
                n_min_z = min_z - 2  # Basishöhe definieren (z.B. 2 Einheiten unter der minimalen Höhe)

                # STL-Datei für das Gelände erstellen
                output_file_gelaende = os.path.join(st.session_state.output_folder, "Gelände.stl")
                create_stl_with_flat_base_and_terrain(points, n_min_z, output_file_gelaende)
                st.success(f"Das Gelände wurde erfolgreich als STL-Datei erstellt: {output_file_gelaende}")

        except Exception as e:
            st.error(f"Fehler beim Erstellen des Geländes: {e}")

        # Buttons für die Auswahl: Mit oder ohne Gelände
        st.header("Gelände in die finale STL integrieren?")
        st.write("Bitte wähle aus, ob das Gelände in die finale STL integriert werden soll.")

        include_terrain = st.button("Mit Gelände")
        exclude_terrain = st.button("Ohne Gelände")

        # Zusammenführung der STL-Dateien basierend auf der Auswahl
        if include_terrain or exclude_terrain:
            try:
                stl_output_file = os.path.join(st.session_state.output_folder, "Gesamt.stl")

                if include_terrain:
                    # Mit Gelände zusammenführen
                    combine_stl_files(stl_output_file, output_stl_g, output_stl, output_file_gelaende)
                    st.success("STL-Datei wurde erfolgreich zusammengeführt **mit Gelände** und gespeichert.")
                elif exclude_terrain:
                    # Ohne Gelände zusammenführen
                    combine_stl_files(stl_output_file, output_stl_g, output_stl)
                    st.success("STL-Datei wurde erfolgreich zusammengeführt **ohne Gelände** und gespeichert.")

                # Button zum nächsten Schritt anzeigen
                if st.button("Nächster Schritt"):
                    st.session_state.page = "page_2"

            except Exception as e:
                st.error(f"Fehler beim Zusammenführen der STL-Dateien: {e}")


# Seite 2 anzeigen (nach dem Speichern), Schritt 5
if st.session_state.page == "page_2":
    st.header("3. Ergebnis Exportieren")
    st.write("Hier kannst du das Ergebnis exportieren.")
    st.write(f"Gespeicherte Dateien befinden sich im Ordner: {st.session_state.output_folder}")

