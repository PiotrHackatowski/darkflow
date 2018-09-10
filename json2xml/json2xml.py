import dicttoxml
import json
import xml.etree.cElementTree as ET
import os
from PIL import Image

ann_dir = "/home/masta/Pictures/audia6c6ann/"
img_dir = "/home/masta/Pictures/audia6c6/"

for file in os.listdir(ann_dir):
    if file.endswith(".json"):
        print(file)
        img_file_name = file.replace("json", "jpg")
        img_file_full_path = img_dir + img_file_name


        im = Image.open(img_file_full_path)
        width, height = im.size

        print(width)
        print(height)

        f = open(ann_dir + file)
        data = json.loads(f.read())
        f.close()

        if data:

            print(data[0])
            print(data[0]['topleft']['x'])

            annotation = ET.Element("annotation")

            #annotation
            ET.SubElement(annotation, "folder").text = "audia6c6"
            ET.SubElement(annotation, "filename").text = img_file_name
            ET.SubElement(annotation, "path").text = img_file_full_path

            #annotation/source
            source = ET.SubElement(annotation, "source")
            ET.SubElement(source, "database").text = "Unknown"

            #annotation/size
            source = ET.SubElement(annotation, "size")
            ET.SubElement(source, "width").text = str(width)
            ET.SubElement(source, "height").text = str(height)
            ET.SubElement(source, "depth").text = "3"

            #annotation/segmented
            ET.SubElement(annotation, "segmented").text = "0"

            #annotation/object
            object = ET.SubElement(annotation, "object")

            ET.SubElement(object, "name").text = "audia6c6fl"
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
            tree.write(file.replace("json", "xml"))
            #xml = dicttoxml.dicttoxml(data)
            #print(xml)