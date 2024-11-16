#Laden einer Punktwolke - XYZ-Format

import numpy as np

xyz_filename = ("xyz_filename.xyz")

def load_xyz(xyz_filename):
    data = np.loadtxt(xyz_filename, skiprows=1)
    return data

data= load_xyz(xyz_filename)
print(data[5])



"""
# helper function
def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)

# iterate over all entities in modelspace
msp = doc.modelspace()
for e in msp:
    if e.dxftype() == "LINE":
        print_entity(e)

# entity query for all LINE entities in modelspace
for e in msp.query("LINE"):
    print_entity(e)
    """