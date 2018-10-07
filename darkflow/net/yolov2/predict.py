import numpy as np
import math
import cv2
import os
import json
#from scipy.special import expit
#from utils.box import BoundBox, box_iou, prob_compare
#from utils.box import prob_compare2, box_intersection
from ...utils.box import BoundBox
from ...cython_utils.cy_yolo2_findboxes import box_constructor

import xml.etree.cElementTree as ET

def expit(x):
	return 1. / (1. + np.exp(-x))

def _softmax(x):
    e_x = np.exp(x - np.max(x))
    out = e_x / e_x.sum()
    return out

def findboxes(self, net_out):
	# meta
	meta = self.meta
	boxes = list()
	boxes=box_constructor(meta,net_out)
	return boxes

def postprocess(self, net_out, im, save = True):
	"""
	Takes net output, draw net_out, save to disk
	"""
	boxes = self.findboxes(net_out)

	# meta
	meta = self.meta
	threshold = meta['thresh']
	colors = meta['colors']
	labels = meta['labels']
	if type(im) is not np.ndarray:
		imgcv = cv2.imread(im)
	else: imgcv = im
	h, w, _ = imgcv.shape
	
	resultsForJSON = []


	resultsForXML = build_xml(w, h)


	for b in boxes:

		boxResults = self.process_box(b, h, w, threshold)
		if boxResults is None:
			continue
		left, right, top, bot, mess, max_indx, confidence = boxResults

		if mess != self.FLAGS.labelToChange:
			continue

		thick = int((h + w) // 300)
		if self.FLAGS.xml:
			if self.FLAGS.labelToChange and self.FLAGS.newLabel and self.FLAGS.labelToChange == mess:
				mess = self.FLAGS.newLabel
				resultsForXML = add_object_to_xml(resultsForXML, mess, top, left, right, bot)

		if self.FLAGS.json:
			resultsForJSON.append({"label": mess, "confidence": float('%.2f' % confidence), "topleft": {"x": left, "y": top}, "bottomright": {"x": right, "y": bot}})
			#continue

		cv2.rectangle(imgcv,
			(left, top), (right, bot),
			colors[max_indx], thick)
		cv2.putText(imgcv, mess, (left, top - 12),
			0, 1e-3 * h, colors[max_indx],thick//3)

	if not save: return imgcv

	outfolder = os.path.join(self.FLAGS.imgdir, 'out')
	img_name = os.path.join(outfolder, os.path.basename(im))
	if self.FLAGS.xml:
		tree = ET.ElementTree(resultsForXML)
		tree.write(os.path.splitext(img_name)[0] + ".xml")

	if self.FLAGS.json:
		textJSON = json.dumps(resultsForJSON)
		textFile = os.path.splitext(img_name)[0] + ".json"
		with open(textFile, 'w') as f:
			f.write(textJSON)
		#return

	cv2.imwrite(img_name, imgcv)


def build_xml(width, height):
	annotation = ET.Element("annotation")

	# annotation
	ET.SubElement(annotation, "folder").text = "audia6c6"
	ET.SubElement(annotation, "filename").text = ""
	ET.SubElement(annotation, "path").text = ""

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

	return annotation

def add_object_to_xml(annotation, label, top, left, right, bot):
	# annotation/object
	object = ET.SubElement(annotation, "object")

	ET.SubElement(object, "name").text = label
	ET.SubElement(object, "pose").text = "Unspecified"
	ET.SubElement(object, "truncated").text = str(0)
	ET.SubElement(object, "difficult").text = str(0)

	bndbox = ET.SubElement(object, "bndbox")
	ET.SubElement(bndbox, "xmin").text = str(left)
	ET.SubElement(bndbox, "ymin").text = str(top)
	ET.SubElement(bndbox, "xmax").text = str(right)
	ET.SubElement(bndbox, "ymax").text = str(bot)

	return annotation
