import numpy as np


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

