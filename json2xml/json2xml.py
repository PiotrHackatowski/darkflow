import json
import xml.etree.cElementTree as ET
import os
from PIL import Image
from shutil import copyfile

in_label = 'cat'
out_label = 'siam'

img_dir = "C:/Users/Piotr/Desktop/cat_test/"
ann_dir = img_dir + "out/"


final_img_dir = "C:/Users/Piotr/Desktop/cat_test_out/images/"
final_ann_dir = "C:/Users/Piotr/Desktop/cat_test_out/ann/"

if not os.path.exists(final_img_dir):
    os.makedirs(final_img_dir)

if not os.path.exists(final_ann_dir):
    os.makedirs(final_ann_dir)

for file in os.listdir(ann_dir):
    statinfo = os.stat(ann_dir + file)
    if file.endswith(".json") and 50 < statinfo.st_size:
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

        annotation = ET.Element("annotation")

        # annotation
        ET.SubElement(annotation, "folder").text = out_label
        ET.SubElement(annotation, "filename").text = img_file_name
        ET.SubElement(annotation, "path").text = img_file_full_path

        # annotation/source
        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text = "Unknown"

        # annotation/size
        source = ET.SubElement(annotation, "size")
        ET.SubElement(source, "width").text = str(width)
        ET.SubElement(source, "height").text = str(height)
        ET.SubElement(source, "depth").text = "3"

        # annotation/segmented
        ET.SubElement(annotation, "segmented").text = "0"


        for d in data:
            if d and in_label in d['label']:

                print(d)
                print(d['topleft']['x'])

                # annotation/object
                object = ET.SubElement(annotation, "object")

                ET.SubElement(object, "name").text = out_label
                ET.SubElement(object, "pose").text = "Unspecified"
                ET.SubElement(object, "truncated").text = str(0)
                ET.SubElement(object, "difficult").text = str(0)

                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(d['topleft']['x'])
                ET.SubElement(bndbox, "ymin").text = str(d['topleft']['y'])
                ET.SubElement(bndbox, "xmax").text = str(d['bottomright']['x'])
                ET.SubElement(bndbox, "ymax").text = str(d['bottomright']['y'])

        tree = ET.ElementTree(annotation)

        print(tree)
        tree.write(final_ann_dir + file.replace("json", "xml"))
        copyfile(img_file_full_path, final_img_dir + img_file_name)
        #xml = dicttoxml.dicttoxml(data)
        #print(xml)