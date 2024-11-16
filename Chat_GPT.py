import numpy as np
import ezdxf

def load_xyz(filename):
    """Lädt die Punktwolke aus einer XYZ-Datei."""
    with open(filename, 'r') as file:
        # Überspringe die Kopfzeile und lese die Daten
        header = file.readline().strip()
        data = np.loadtxt(file)
    return header, data

def load_rectangle_from_dxf(dxf_filename):
    """Lädt die Rechteck-Koordinaten aus einer DXF-Datei."""
    doc = ezdxf.readfile(dxf_filename)
    msp = doc.modelspace()
    
    # Gehe durch alle Linien und extrahiere die Rechteck-Koordinaten
    # Wir gehen davon aus, dass das Rechteck als geschlossener Polyline gezeichnet ist.
    rectangle_coords = []
    for entity in msp.query("LWPOLYLINE"):
        if entity.is_closed:  # Nur geschlossene Polylinien
            for x, y, *_ in entity:
                rectangle_coords.append((x, y))
            break  # Nur das erste Rechteck nehmen
    
    if len(rectangle_coords) != 4:
        raise ValueError("Das DXF enthält kein gültiges Rechteck.")
    
    # Berechne die minimalen und maximalen x- und y-Werte des Rechtecks
    x_coords, y_coords = zip(*rectangle_coords)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    return min_x, max_x, min_y, max_y

def filter_points_in_rectangle(points, min_x, max_x, min_y, max_y):
    """Filtert die Punkte, die innerhalb der Rechteckgrenzen liegen."""
    x, y, _ = points.T  # Nehme x, y, und z-Koordinaten
    mask = (x >= min_x) & (x <= max_x) & (y >= min_y) & (y <= max_y)
    return points[mask]

def save_xyz(filename, header, points):
    """Speichert die gefilterten Punkte in einer neuen XYZ-Datei."""
    with open(filename, 'w') as file:
        file.write(header + '\n')
        np.savetxt(file, points, fmt='%.6f')

# Hauptskript
xyz_filename = "input.xyz"   # Pfad zur XYZ-Datei
dxf_filename = "rectangle.dxf"  # Pfad zur DXF-Datei mit Rechteck
output_filename = "filtered_output.xyz"  # Pfad zur Ausgabe-XYZ-Datei

# Schritt 1: Laden der Punktwolke
header, points = load_xyz(xyz_filename)

# Schritt 2: Rechteckgrenzen aus der DXF-Datei laden
min_x, max_x, min_y, max_y = load_rectangle_from_dxf(dxf_filename)

# Schritt 3: Punktwolke filtern
filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)

# Schritt 4: Gefilterte Punktwolke speichern
save_xyz(output_filename, header, filtered_points)

print(f"Die gefilterte Punktwolke wurde in '{output_filename}' gespeichert.")









#Chat GPT

# Beispiel: Erstellen einer Punktwolke (x, y, z)
# Angenommen, wir haben eine Punktwolke mit zufälligen 3D-Koordinaten (x, y, z)
point_cloud = np.random.rand(1000, 3) * 100  # 1000 Punkte in einem Bereich von 0 bis 100 (Meter)

# Schritt 1: Sortieren der Punktwolke nach den z-Werten
point_cloud_sorted = point_cloud[point_cloud[:, 2].argsort()]

# Schritt 2: Definiere die Schichtdicke (in diesem Fall 50 cm)
layer_thickness = 0.5  # 50 cm

# Schritt 3: Schichtenbildung basierend auf den z-Werten
layers = {}
min_z = np.min(point_cloud_sorted[:, 2])
max_z = np.max(point_cloud_sorted[:, 2])
num_layers = int(np.ceil((max_z - min_z) / layer_thickness))

# Punkte in Schichten einteilen
for i in range(num_layers):
    layer_min_z = min_z + i * layer_thickness
    layer_max_z = layer_min_z + layer_thickness
    layer_points = point_cloud_sorted[(point_cloud_sorted[:, 2] >= layer_min_z) & 
                                      (point_cloud_sorted[:, 2] < layer_max_z)]
    layers[f'Layer_{i + 1}'] = layer_points

# Ausgabe der Anzahl der Punkte pro Schicht
for layer_name, points in layers.items():
    print(f"{layer_name}: {len(points)} Punkte")





#Test 

import Main_Module.configuration_model


dateipfad = input("Gib den Pfad der Datei ein: ")

# Öffne die Datei im Lesemodus
try:
    with open(dateipfad, 'r', encoding='utf-8') as file:
        # Lese den Inhalt der Datei
        inhalt = file.read()
        print(inhalt)
except FileNotFoundError:
    print("Die Datei wurde nicht gefunden.")
except IOError:
    print("Ein Fehler beim Öffnen der Datei ist aufgetreten.")