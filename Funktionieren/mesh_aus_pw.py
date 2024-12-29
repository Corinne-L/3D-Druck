import numpy as np
import ezdxf
from scipy.spatial import Delaunay

def load_xyz(xyz_filename: str) -> np.ndarray:
    """
    Ladet eine Punktwolke im XYZ-Format und löscht die Kopfzeile.

    Parameters:
    xyz_filename (str): Der Pfad zur Datei, die die Punktwolke im XYZ-Format enthält.

    Returns:
    np.ndarray: Ein NumPy-Array der Form (n, 3), das die x-, y- und z-Koordinaten der Punkte enthält.
    """
    try:
        points = np.loadtxt(xyz_filename, skiprows=1)
        if points.shape[1] != 3:
            raise ValueError("Die Datei muss 3 Spalten für x, y und z enthalten.")
        return points
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        return None


# Punktwolke laden
points = load_xyz("gefilterte_PW.xyz")

if points is None:
    print("Die Punktwolke konnte nicht geladen werden. Das Programm wird beendet.")
else:
    # Delaunay-Triangulation (3D)
    tri = Delaunay(points[:, :2])  # Triangulation in 2D mit x und y, aber wir speichern auch z-Koordinaten.

    # DXF-Dokument erstellen
    doc = ezdxf.new(dxfversion='R2000')
    msp = doc.modelspace()

    # Für jedes Dreieck in der Triangulation Linien als 3D-Flächen (faces) hinzufügen
    for simplex in tri.simplices:
        p1, p2, p3 = points[simplex]  # Holen der 3D-Koordinaten (x, y, z)
        
        # Erstelle 3D-Fläche (face) für jedes Dreieck
        msp.add_3dface([p1, p2, p3])

    # Speichern der DXF-Datei
    doc.saveas("triangulation_3d.dxf")

    print("3D-DXF-Datei 'triangulation_3d.dxf' gespeichert.")
