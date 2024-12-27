import ezdxf

# Funktion zum Filtern und Entfernen von Entitäten basierend auf Layern
def split_and_remove_entities(import_file, layers_to_keep):
    try:
        doc = ezdxf.readfile(import_file)
    except IOError:
        print(f"Datei konnte nicht geöffnet werden: {import_file}")
        return None, []

    # Zugriff auf das Modelspace
    msp = doc.modelspace()

    # Liste, um die gewünschten Entitäten zu speichern
    entities_to_export = []

    # Entitäten sammeln und aus dem Modelspace entfernen
    for entity in list(msp):
        if entity.dxf.layer in layers_to_keep:
            entities_to_export.append(entity)
            msp.delete_entity(entity)

    return doc, entities_to_export

def save_dxf(doc, output_file):
    # DXF speichern
    doc.saveas(output_file)
    print(f"Datei gespeichert: {output_file}")

# Dateinamen
import_file = "Häuser.dxf"
output_file_gebaeude = "Gebäude.dxf"
output_file_dach = "Dächer.dxf"

# Layer-Listen definieren
layers_dach = [
    "Roof_Gebaeude Einzelhaus", "Roof_Gebaeude unsichtbar", 
    "Roof_Kapelle", "Roof_Lagertank", 
    "Roof_Lueftungsschacht", "Roof_Mauer gross",
    "Roof_Offenes Gebaeude", "Roof_Sakrales Gebaeude", "0"
]

layers_gebaeude = [
    "Build_Gebaeude Einzelhaus", "Build_Gebaeude unsichtbar",
    "Build_Kapelle", "Build_Lagertank", 
    "Build_Lueftungsschacht", "Build_Mauer gross", "Build_Sakrales Gebaeude","0"
]

# Dächer exportieren
doc_dach, Dach = split_and_remove_entities(import_file, layers_gebaeude)
if Dach:
    save_dxf(doc_dach, output_file_dach)
else:
    print("Keine Dächer gefunden.")

# Gebäude exportieren
doc_gebaeude, Gebäude = split_and_remove_entities(import_file, layers_dach)
if Gebäude:
    save_dxf(doc_gebaeude, output_file_gebaeude)
else:
    print("Keine Gebäude gefunden.")
