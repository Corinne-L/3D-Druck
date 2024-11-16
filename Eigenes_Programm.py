## TO-DO Biblotheken einzulesen

import numpy as np
import ezdxf
import streamlit as st
import pandas as pd
import tempfile
import os

# Definitoinen von Funktionen und Klassen


# Laden des Perimeters - DXF Format
def load_perimeter(dxf_filename):
    with tempfile.NamedTemporaryFile(delete=False) as temp_dxf:
        temp_dxf.write(dxf_filename.read())  # Schreiben des Inhalts in die temporäre Datei
        temp_dxf_path = temp_dxf.name  # Pfad zur temporären Datei
    doc = ezdxf.readfile(temp_dxf_path)
    msp = doc.modelspace()
    rectangle_coords = []
    for entity in msp.query("LWPOLYLINE"):
        if entity.is_closed: 
            for x, y, *_ in entity:
                rectangle_coords.append((x, y))
            break 
    
    if len(rectangle_coords) != 4:
        raise ValueError("Das DXF enthält kein gültiges Rechteck.")
    
    x_coords, y_coords = zip(*rectangle_coords)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

     # Temporäre Datei löschen, wenn sie nicht mehr benötigt wird
    os.remove(temp_dxf_path)

    return min_x, max_x, min_y, max_y

#Laden einer Punktwolke - XYZ-Format
def load_xyz(xyz_filename):
    points = np.loadtxt(xyz_filename, skiprows=1)
    return points


# Filtern der Punktwolke
def filter_points_in_rectangle(points, min_x, max_x, min_y, max_y): 
    x = points[:, 0]
    y = points[:, 1] 
    z = points[:, 2] 
    mask = (x >= min_x) & (x <= max_x) & (y >= min_y) & (y <= max_y)
    return points[mask]

# Speichen der Zugeschnittenen Punktwolke
def save_xyz(output_filename,filtered_points):
    if filtered_points.size == 0:
        print("Keine Punkte zum Speichern vorhanden.")
        return
    with open(output_filename, 'w') as file:
        np.savetxt(file, filtered_points, fmt='%.3f')
        print(f"Die gefilterte Punktwolke wurde in '{output_filename}' gespeichert.")

#Definition Variabeln


## Streamlit
st.title("3D Druck erstellen")
st.write("Diese anwendung dient dazu ein geschichtetes 3D Modell zu erstellen, welches anschliessend gedruckt werden kann.")

xyz_filename = st.file_uploader("Lade hier die xyz-Datei hoch", type="xyz")
dxf_filename = st.file_uploader("Lade hier den Perimeter hoch", type="dxf")

if xyz_filename and dxf_filename:
    try:
        min_x, max_x, min_y, max_y = load_perimeter(dxf_filename)
        points = load_xyz(xyz_filename)
        filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)

        save_button = st.button("Gefilterte Punktwolke speichern")
        if save_button:
            output_filename = "gefilterte_PW.xyz"
            save_xyz(output_filename, filtered_points)
            st.success(f"Die gefilterte Punktwolke wurde als '{output_filename}' gespeichert.")
            
    except Exception as e:
        st.error(f"Fehler: {e}")  
