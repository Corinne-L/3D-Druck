from stl import mesh
import numpy as np

# Laden der STL-Dateien
mesh1 = mesh.Mesh.from_file("solid.stl")
mesh2 = mesh.Mesh.from_file("dach.stl")
mesh3 = mesh.Mesh.from_file("gelände.stl")

# Kombiniere der Meshes
combined_mesh = mesh.Mesh(np.concatenate([mesh1.data, mesh2.data, mesh3.data]))

# Exportiere das kombinierte Mesh in eine neue STL-Datei
combined_mesh.save("kombiniert.stl")
print("STL-Dateien erfolgreich zusammengeführt und exportiert!")