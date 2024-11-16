import streamlit as st
import pandas as pd

# Titel 
st.title("3D Druck erstellen")

# Text
st.write("Diese anwendung dient dazu ein geschichtetes 3D Modell zu erstellen, welches anschliessend gedruckt werden kann.")


# Datei hochladen
xyz_filename = st.file_uploader("Lade hier die xyz-Datei hoch", type="xyz")
dxf_filename = st.file_uploader("Lade hier den Perimeter hoch", type="dxf")

if xyz_filename and dxf_filename:
    try:
        points = load_xyz(xyz_filename)
        min_x, max_x, min_y, max_y = load_perimeter(dxf_filename)
        filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)

        # Output speichern und bereitstellen
        st.write(f"Gefilterte Punkte: {filtered_points.shape[0]}")
        if st.button("Download gefilterter Punktwolke"):
            csv = "\n".join(" ".join(map(str, row)) for row in filtered_points)
            st.download_button(
                label="Gefilterte Punktwolke herunterladen",
                data=csv,
                file_name="filtered_output.xyz",
                mime="text/plain",
            )

    except Exception as e:
        st.error(f"Fehler: {e}")