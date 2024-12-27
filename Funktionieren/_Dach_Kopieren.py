import ezdxf

# Datei öffnen
input_file = "block.dxf"
output_file = "test1.dxf"

# DXF Datei laden
doc = ezdxf.readfile(input_file)

# Modellspace holen
msp = doc.modelspace()

# Layer für Dächer definieren
roof_layer = "Roof"

# Extrusion um einen Meter nach unten
extrusion_distance = -1.0

# Neue Entitäten für das extrudierte Dach erstellen
for entity in msp.query(f'INSERT[layer=="{roof_layer}"]'):
    try:
        # Originalposition der Entität
        original_insert = entity.dxf.insert
        
        #Eine neue Position für das extrudierte Dach berechnen
        new_insert = (original_insert[0], original_insert[1], original_insert[2] + extrusion_distance)
        
        # Eine neue INSERT-Entität (Blockreferenz) hinzufügen
        new_entity = msp.add_blockref(
            name=entity.dxf.name,  # Name des Blocks
            insert=new_insert  # Neue Einfügeposition
        )
       
    except Exception as e:
        print(f"Fehler bei der Bearbeitung von INSERT-Entität: {e}")

# Geänderte DXF speichern
doc.saveas(output_file)

print(f"Die Datei wurde erfolgreich extrudiert und unter {output_file} gespeichert.")

