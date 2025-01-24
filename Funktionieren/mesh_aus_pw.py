import numpy as np
from scipy.spatial import Delaunay
from stl import mesh
import trimesh

def load_xyz(xyz_filename: str) -> np.ndarray:
    """
    Lädt eine Punktwolke im XYZ-Format und löscht die Kopfzeile.
    """
    try:
        points = np.loadtxt(xyz_filename, skiprows=1)
        if points.shape[1] != 3:
            raise ValueError("Die Datei muss 3 Spalten für x, y und z enthalten.")
        return points
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        return None


def create_stl_with_flat_base_and_terrain(points: np.ndarray, base_height: float, output_filename: str):
    """
    Erstellt eine STL-Datei mit einer flachen Basis und der oberen Oberfläche basierend auf der Punktwolke.
    
    Parameters:
    points (np.ndarray): Die Punkte (n, 3) als Eingabe.
    base_height (float): Höhe der Basis in Z-Richtung.
    output_filename (str): Name der Ausgabedatei.
    """
    # Original Z-Werte sichern (für die Oberseite)
    original_z = points[:, 2]

    # Delaunay-Triangulation nur in x, y
    tri = Delaunay(points[:, :2])

    vertices = []
    faces = []

    for simplex in tri.simplices:
        # Originalpunkte des Dreiecks (für die flache Basis)
        p1, p2, p3 = points[simplex]
        
        # Punkte der oberen Oberfläche (ursprüngliche Höhen)
        p1_top = np.copy(p1)
        p1_top[2] = original_z[simplex[0]]
        
        p2_top = np.copy(p2)
        p2_top[2] = original_z[simplex[1]]
        
        p3_top = np.copy(p3)
        p3_top[2] = original_z[simplex[2]]

        # Setze die Z-Koordinaten der Basis auf die feste Höhe
        p1[2] = base_height
        p2[2] = base_height
        p3[2] = base_height

        # Füge die Basispunkte und die Oberflächenpunkte hinzu
        base_index = len(vertices)
        vertices.extend([p1, p2, p3])  # Basisdreieck
        vertices.extend([p1_top, p2_top, p3_top])  # Oberflächendreieck

        # Dreiecke für Basisfläche, obere Fläche und Seitenflächen
        faces.append([base_index, base_index + 1, base_index + 2])  # Basisdreieck
        faces.append([base_index + 3, base_index + 4, base_index + 5])  # Oberflächendreieck
        faces.append([base_index, base_index + 1, base_index + 4])  # Seite 1
        faces.append([base_index, base_index + 4, base_index + 3])  # Seite 1
        faces.append([base_index + 1, base_index + 2, base_index + 5])  # Seite 2
        faces.append([base_index + 1, base_index + 5, base_index + 4])  # Seite 2
        faces.append([base_index + 2, base_index, base_index + 3])  # Seite 3
        faces.append([base_index + 2, base_index + 3, base_index + 5])  # Seite 3

    # Konvertiere die Listen in NumPy-Arrays
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Erstelle ein Trimesh-Objekt
    trimesh_model = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Speichern ohne die Notwendigkeit, das Mesh zu überprüfen oder zu vereinfachen
    trimesh_model.export(output_filename)
    print(f"STL-Datei '{output_filename}' erfolgreich erstellt!")

# Punktwolke laden
points = load_xyz("gefilterte_PW.xyz")

x, y, z = points[:, 0], points[:, 1], points[:, 2]

# Generate contour levels based on the Z-range and layer thickness
min_z, max_z = int(np.floor(np.min(z))), int(np.ceil(np.max(z)))
n_min_z = min_z - 2

if points is None:
    print("Die Punktwolke konnte nicht geladen werden. Das Programm wird beendet.")
else:
    # Basishöhe definieren
    base_height = n_min_z  # Beispielhöhe für die flache Basis

    # STL-Datei erstellen
    create_stl_with_flat_base_and_terrain(points, base_height, "Gelände.stl")
