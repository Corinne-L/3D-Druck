## TO-DO Biblotheken einzulesen

import numpy as np
import streamlit as st
import pandas as pd



# Definitoinen von Funktionen und Klassen
from PW_filterung import load_perimeter, load_xyz, filter_points_in_rectangle, save_xyz

#Definition Variabeln


## Streamlit
st.title("3D Druck erstellen")
st.write("Diese anwendung dient dazu ein geschichtetes 3D Modell zu erstellen, welches anschliessend gedruckt werden kann.")

xyz_filename = st.file_uploader("Lade hier die xyz-Datei hoch", type="xyz")
dxf_filename = st.file_uploader("Lade hier den Perimeter hoch", type="dxf")

Schichtstaerke = st.number_input(
    label = "Geben Sie hier die Schichtstärke in Meter an",
    min_value = 0.25,
    value = 1.0,
    step = 0.25,
    format = "%.2f"
    )

if xyz_filename and dxf_filename and Schichtstaerke:
    try:
        min_x, max_x, min_y, max_y = load_perimeter(dxf_filename)
        points = load_xyz(xyz_filename)
        filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)
        output_filename = st.text_input("Geben Sie den Namen der Ausgabedatei ein:")
        save_button = st.button("Gefilterte Punktwolke speichern")
        if save_button:
            if not output_filename.endswith(".xyz"):
                output_filename += ".xyz"
            save_xyz(output_filename, filtered_points)
            st.success(f"Die gefilterte Punktwolke wurde als {output_filename} gespeichert.")
        else:
            st.error("Bitte geben Sie einen gültigen Dateinamen ein.")
            st.success(f"Die gefilterte Punktwolke wurde als {output_filename} gespeichert.")
            
    except Exception as e:
        st.error(f"Fehler: {e}")  


PW_sortiert_Z = filtered_points [filtered_points[:, 2].argsort()]

# Schritt 3: Schichtenbildung basierend auf den z-Werten
layers = {}
min_z = np.min(PW_sortiert_Z[:, 2])
max_z = np.max(PW_sortiert_Z[:, 2])
num_layers = int(np.ceil((max_z - min_z) / Schichtstaerke))

# Punkte in Schichten einteilen
for i in range(num_layers):
    layer_min_z = min_z + i * Schichtstaerke
    layer_max_z = layer_min_z + Schichtstaerke
    layer_points = PW_sortiert_Z[(PW_sortiert_Z[:, 2] >= layer_min_z) & 
                                      (PW_sortiert_Z[:, 2] < layer_max_z)]
    layers[f"Layer_{i + 1}"] = layer_points
    

# Ausgabe der Anzahl der Punkte pro Schicht
for layer_name, points in layers.items():
    print(f"{layer_name}: {len(points)} Punkte")
