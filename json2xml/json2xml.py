import dicttoxml
import json
import xml.etree.cElementTree as ET
import os

for file in os.listdir("/home/masta/Pictures/audia6c6ann"):
    if file.endswith(".json"):
        print(file)
f = open("input.json")
data = json.loads(f.read())
f.close()
print(data[0])
print(data[0]['topleft']['x'])

annotation = ET.Element("annotation")

#annotation
ET.SubElement(annotation, "folder").text = "folder_name"
ET.SubElement(annotation, "filename").text = "file_name"
ET.SubElement(annotation, "path").text = "path"

#annotation/source
source = ET.SubElement(annotation, "source")
ET.SubElement(source, "database").text = "Unknown"

#annotation/size
source = ET.SubElement(annotation, "size")
ET.SubElement(source, "width").text = "width"
ET.SubElement(source, "height").text = "height"
ET.SubElement(source, "depth").text = "depth"

#annotation/segmented
ET.SubElement(annotation, "segmented").text = "segmented"

#annotation/object
object = ET.SubElement(annotation, "object")

ET.SubElement(object, "name").text = "redball"
ET.SubElement(object, "pose").text = "Unspecified"
ET.SubElement(object, "truncated").text = str(0)
ET.SubElement(object, "difficult").text = str(0)

bndbox = ET.SubElement(object, "bndbox")
ET.SubElement(bndbox, "xmin").text = str(data[0]['topleft']['x'])
ET.SubElement(bndbox, "ymin").text = str(data[0]['topleft']['y'])
ET.SubElement(bndbox, "xmax").text = str(data[0]['bottomright']['x'])
ET.SubElement(bndbox, "ymax").text = str(data[0]['bottomright']['y'])

tree = ET.ElementTree(annotation)

print(tree)
tree.write("filename.xml")
#xml = dicttoxml.dicttoxml(data)
#print(xml)