## TO-DO Biblotheken einzulesen

import numpy as np
import ezdxf
import streamlit as st
import pandas as pd

dxf_filename = ("Perimeter2.dxf")
xyz_filename = ("xyz_filename.xyz")
output_filename = ("TEST_Output")

# Laden des Perimeters - DXF Format
def load_perimeter(dxf_filename):
    doc = ezdxf.readfile(dxf_filename)
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
    
    return min_x, max_x, min_y, max_y

#Laden einer Punktwolke - XYZ-Format
def load_xyz(xyz_filename):
    points = np.loadtxt(xyz_filename, skiprows=1)
    print (points)
    return points


# Filtern der Punktwolke
def filter_points_in_rectangle(points, min_x, max_x, min_y, max_y): 
    x = points[:, 0]
    y = points[:, 1] 
    z = points[:, 2] 
    mask = (x >= min_x) & (x <= max_x) & (y >= min_y) & (y <= max_y)
    return points[mask]

# Speichen der Zugeschnittenen Punktwolke
def save_xyz(output_filename,filtered_points):
    if filtered_points.size == 0:
        print("Keine Punkte zum Speichern vorhanden.")
        return
    with open(output_filename, 'w') as file:
        np.savetxt(file, filtered_points, fmt='%.3f')
        print(f"Die gefilterte Punktwolke wurde in '{output_filename}' gespeichert.")


min_x, max_x, min_y, max_y = load_perimeter(dxf_filename)
points = load_xyz(xyz_filename)
filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)
save_xyz(output_filename, filtered_points)

