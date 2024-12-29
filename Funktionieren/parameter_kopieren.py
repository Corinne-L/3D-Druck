import tempfile
import ezdxf
import numpy as np

def save_rectangles_to_dxf(rectangles, output_filename):
    """
    Speichert eine Liste von Rechtecken in eine neue DXF-Datei, einschließlich der Höhen.

    Parameters:
    rectangles (list of list of tuple): Eine Liste von Rechtecken, wobei jedes Rechteck
                                         eine Liste von 3D-Koordinaten ist.
    output_filename (str): Der Pfad zur Ausgabe-DXF-Datei.
    """
    doc = ezdxf.new()  # Erstelle ein neues DXF-Dokument
    msp = doc.modelspace()  # Zugriff auf den Modelspace

    for rectangle in rectangles:
        # Stelle sicher, dass das Rechteck geschlossen ist, indem wir den ersten Punkt am Ende hinzufügen
        closed_rectangle = rectangle + [rectangle[0]]
        # Füge das Rechteck als 3D-POLYLINE hinzu
        msp.add_polyline3d(closed_rectangle)

    # Speichern der Datei
    doc.saveas(output_filename)
    print(f"DXF-Datei wurde unter {output_filename} gespeichert.")


def create_rectangles_at_heights(dxf_filename, heights):
    """
    Lädt ein Rechteck aus einer DXF-Datei und kopiert es auf verschiedene Höhen.

    Parameters:
    dxf_filename (str): Der Pfad zur DXF-Datei, die das Rechteck enthält.
    heights (list of float): Eine Liste von Höhen, auf die das Rechteck kopiert werden soll.

    Returns:
    list of list of tuple: Eine Liste von Rechtecken, wobei jedes Rechteck eine Liste von 3D-Koordinaten ist.
    """
    

    # Laden des Rechtecks aus der DXF-Datei
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
        return rectangle_coords

    rectangle_coords = load_perimeter(dxf_filename)

    # Rechtecke auf verschiedenen Höhen erstellen
    rectangles = []
    for height in heights:
        rectangle_3d = [(x, y, height) for x, y in rectangle_coords]
        rectangles.append(rectangle_3d)

    return rectangles

def load_xyz(xyz_filename):
    points = np.loadtxt(xyz_filename)
    return points

FILTERED_POINTS_FILE = "gefilterte_PW.xyz"
Schichtstaerke = 1 


points = load_xyz(FILTERED_POINTS_FILE)
x, y, z = points[:, 0], points[:, 1], points[:, 2]

# Höhenlimits bestimmen
min_z, max_z = int(np.floor(np.min(z))), int(np.ceil(np.max(z)))
contour_levels = np.arange(min_z, max_z + Schichtstaerke, Schichtstaerke)
print (contour_levels)
print (type(contour_levels))

# Beispielaufruf
heights = contour_levels.tolist()  # Höhen, auf denen das Rechteck kopiert werden soll
dxf_path = "Perimeter2.dxf"
dxf_output_path = "output_with_rectangles.dxf"  # Ausgabe-DXF-Datei

with open(dxf_path, "rb") as dxf_file:
    rectangles_at_heights = create_rectangles_at_heights(dxf_file, heights)

save_rectangles_to_dxf(rectangles_at_heights, dxf_output_path)
