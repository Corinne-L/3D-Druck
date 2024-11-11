## TO-DO Biblotheken einzulesen

import numpy as np
import ezdxf


#Laden einer Punktwolke - XYZ-Format
def load_xyz(filename):
    with open(filename, 'r') as file:
        header = file.readline().strip()
        data = np.loadtxt(file)
    return data


# Laden des Perimeters - DXF Format
def load_perimeter(dxf_filename):
    doc = ezdxf.readfile(dxf_filename)
    msp = doc.modelspace()
    
    rectangle_coords = []
    for entity in msp.query("POLYLINE"):
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


# Filtern der Punktwolke
def filter_points_in_rectangle(points, min_x, max_x, min_y, max_y): 
    x, y, _ = points  
    mask = (x >= min_x) & (x <= max_x) & (y >= min_y) & (y <= max_y)
    return points[mask]

# Speichen der Zugeschnittenen Punktwolke
def save_xyz(filename, points):
    with open(filename, 'w') as file:
        np.savetxt(file, points, fmt='%.3f')

xyz_filename = "input.xyz"   
dxf_filename = "rectangle.dxf"  
output_filename = "filtered_output.xyz"  

points = load_xyz(xyz_filename)
min_x, max_x, min_y, max_y = load_perimeter(dxf_filename)
filtered_points = filter_points_in_rectangle(points, min_x, max_x, min_y, max_y)
save_xyz(output_filename, filtered_points)

print(f"Die gefilterte Punktwolke wurde in '{output_filename}' gespeichert.")


#Test 

import Main_Module.configuration_model