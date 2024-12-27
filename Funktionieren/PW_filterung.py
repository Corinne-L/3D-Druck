import ezdxf
import tempfile
import os
import numpy as np

# Laden des Perimeters - DXF Format
def load_perimeter(dxf_filename:str) -> tuple:
    """
    Lädt den Perimeter (Rechteck) des DXF's und gibt dessen Grenzen zurück.
    mit tempfile wird die Datei temporär gespeichert (braucht es für Streamlit)

    Parameters:
    dxf_filename (str): Der Pfad zur DXF-Datei, die das Rechteck enthält.

    Returns:
    Tuple[float, float, float, float]: Ein Tuple mit den minimalen und maximalen x- und y-Koordinaten
                                        des Rechtecks (min_x, max_x, min_y, max_y).
    
    """
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
def load_xyz(xyz_filename: str) -> np.ndarray:
    """
    Ladet eine Punktwolke im XYZ-Format und löscht die Kopfzeile

    Parameters:
    xyz_filename (str): Der Pfad zur Datei, die die Punktwolke im XYZ-Format enthält.

    Returns:
    np.ndarray: Ein NumPy-Array der Form (n, 3), das die x-, y- und z-Koordinaten der Punkte enthält.
    """
    points = np.loadtxt(xyz_filename, skiprows=1)
    return points

# Filtern einer Punktwolke
def filter_points_in_rectangle(points:np.ndarray, min_x:float, max_x:float, min_y:float, max_y:float) -> np.ndarray: 
    """
    Filtert Punkte aus einer Punktwolke, die innerhalb eines bestimmten Rechtecks liegen.

    Parameters:
    points (np.ndarray): Ein NumPy-Array der Punktwolke, wobei jede Zeile die (x, y, z)-Koordinaten eines Punktes enthält.
    min_x (float): Die minimale x-Koordinate des Rechtecks.
    max_x (float): Die maximale x-Koordinate des Rechtecks.
    min_y (float): Die minimale y-Koordinate des Rechtecks.
    max_y (float): Die maximale y-Koordinate des Rechtecks.

    Returns:
    np.ndarray: Ein gefiltertes NumPy-Array der Form (n, 3) mit den Punkten, die innerhalb des Rechtecks liegen.
    """
    
    x = points[:, 0]
    y = points[:, 1] 
    z = points[:, 2] 

    # Versatz des Rechteckes um 2 Meter nach aussen, damit am Schluss das ganze Rechteck abgedeckt wird
    extended_min_x = min_x - 2
    extended_max_x = max_x + 2
    extended_min_y = min_y - 2
    extended_max_y = max_y + 2

    #Erstellung einer Maske
    maske = (x >  extended_min_x) & (x < extended_max_x) & (y > extended_min_y) & (y < extended_max_y)
    return points[maske]

# Speichen der Zugeschnittenen Punktwolke
def save_xyz(output_filename:str,filtered_points:np.ndarray) -> None:
    """
    Speichert die gefilterte Punktwolke in einer neuen Datei im XYZ-Format.

    Parameters:
    output_filename (str): Der Pfad zur Ausgabedatei, in der die gefilterte Punktwolke gespeichert wird.
    filtered_points (np.ndarray): Ein NumPy-Array der gefilterten Punktwolke.

    Returns:
    None: Gibt keine Rückgabewerte zurück, da die gefilterte Punktwolke in einer Datei gespeichert wird.
    """
    if filtered_points.size == 0:
        print("Keine Punkte zum Speichern vorhanden.")
        return
    with open(output_filename, "w") as file:
        np.savetxt(file, filtered_points, fmt="%.3f")
        print(f"Die gefilterte Punktwolke wurde in {output_filename} gespeichert.")
