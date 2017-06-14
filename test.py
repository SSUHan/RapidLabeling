from xml.etree.ElementTree import Element, SubElement, dump
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import ElementTree

tree = parse("voc_xml_example1.xml")
note = tree.getroot()
dump(note)
print("*"*20)

print(note.find('name'))
exit()
size = note.find('size')
width = int(size.find('width').text)
height = int(size.find('height').text)

for obj in note.findall('object'):
	bndbox = obj.find('bndbox')
	xmin = int(bndbox.find('xmin').text)
	ymin = int(bndbox.find('ymin').text)
	xmax = int(bndbox.find('xmax').text)
	ymax = int(bndbox.find('ymax').text)
	bndbox.find('xmin').text = str(width - xmax)
	bndbox.find('xmax').text = str(width - xmin)

dump(note)

# ElementTree(note).write("note.xml")