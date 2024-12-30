import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Laden einer Punktwolke - XYZ-Format
def load_xyz(xyz_filename):
    points = np.loadtxt(xyz_filename)
    return points

# Parameter
Schichtstaerke = 1  # Abstand zwischen den Höhenlinien
FILTERED_POINTS_FILE = "gefilterte_PW.xyz"
OUTPUT_FILENAME = "Hoehenlinien_und_Randpunkte.xyz"

# XYZ-Punkte laden
points = load_xyz(FILTERED_POINTS_FILE)
x, y, z = points[:, 0], points[:, 1], points[:, 2]

# Höhenlimits bestimmen
min_z, max_z = int(np.floor(np.min(z))), int(np.ceil(np.max(z)))
contour_levels = np.arange(min_z, max_z + Schichtstaerke, Schichtstaerke)

# Gitter erstellen und Daten interpolieren
grid_x, grid_y = np.linspace(np.min(x), np.max(x), 200), np.linspace(np.min(y), np.max(y), 200)
grid_x, grid_y = np.meshgrid(grid_x, grid_y)
grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')

# Konturen berechnen und anzeigen
contour = plt.contour(grid_x, grid_y, grid_z, levels=contour_levels, cmap="terrain")

# Alle Punkte der Höhenlinien extrahieren
hoehenlinien_punkte = []

# Randpunkte extrahieren: Randpunkte der Punktwolke, die sich an den äußeren Grenzen befinden
randpunkte = []

# Grenzen der Punktwolke festlegen (min/max für x und y)
min_x, max_x = np.min(x), np.max(x)
min_y, max_y = np.min(y), np.max(y)

# Randpunkte der Punktwolke filtern: Punkte, die sich an den Randbereichen (x, y) befinden
for i in range(len(x)):
    if x[i] == min_x or x[i] == max_x or y[i] == min_y or y[i] == max_y:
        randpunkte.append([x[i], y[i], z[i]])

randpunkte = np.array(randpunkte)  # In NumPy-Array umwandeln

# Alle Punkte der Höhenlinien und Randpunkte extrahieren
hoehenlinien_punkte = []

# Die Levels direkt aus der contour-Instanz entnehmen
for i, collection in enumerate(contour.collections):
    for path in collection.get_paths():
        if len(path.vertices) > 2:  # Nur Linien mit mehr als 2 Punkten
            # Alle Punkte auf der Höhenlinie extrahieren
            for vertex in path.vertices:
                x, y = vertex
                z = contour_levels[i]  # Z-Wert des aktuellen Levels
                hoehenlinien_punkte.append([x, y, z])

# Randpunkte auf derselben Höhe hinzufügen, wenn sie höher als die Höhenlinie liegen
zusatz_punkte = []

for randpunkt in randpunkte:
    rand_x, rand_y, rand_z = randpunkt
    for i, level in enumerate(contour_levels):
        if rand_z > level:  # Wenn der Z-Wert des Randpunkts höher ist als das Höhenlinien-Level
            zusatz_punkte.append([rand_x, rand_y, level])  # Punkt zum selben Höhenlevel hinzufügen

hoehenlinien_punkte = np.array(hoehenlinien_punkte)  # In NumPy-Array umwandeln
zusatz_punkte = np.array(zusatz_punkte)  # In NumPy-Array umwandeln

# Alle Punkte (Höhenlinien + Randpunkte) zusammen speichern
alle_punkte = np.vstack([hoehenlinien_punkte, zusatz_punkte])

# Alle Punkte im XYZ-Format speichern
np.savetxt(OUTPUT_FILENAME, alle_punkte, fmt="%.6f", delimiter=" ")

print(f"Höhenlinien- und Randpunkte gespeichert in: {OUTPUT_FILENAME}")
