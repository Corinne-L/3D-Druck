from stl import mesh
import numpy as np

def combine_stl_files(stl_output_file: str, *input_files: str):
    """
    Kombiniert mehrere STL-Dateien zu einer einzigen und speichert diese.

    Parameters:
    stl_output_file (str): Der Name der Ausgabedatei.
    input_files (str): Die Namen der Eingabedateien.

    Returns:
    None: Die Funktion gibt nichts zurück sondern Speichert die kombinerten STL in einer Datei. 
    """
    # Laden der STL-Dateien
    meshes: list[mesh.Mesh]= [mesh.Mesh.from_file(file) for file in input_files]

    # Kombinieren der Meshes
    combined_mesh = mesh.Mesh(np.concatenate([m.data for m in meshes]))

    # Exportieren des kombinierten Mesh in eine neue STL-Datei
    combined_mesh.save(stl_output_file)
    print(f"STL-Dateien erfolgreich zusammengeführt und in '{stl_output_file}' exportiert!")

# Beispielaufruf der Funktion
combine_stl_files("kombiniert.stl", "solid.stl", "dach.stl")
