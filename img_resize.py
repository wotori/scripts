from PIL import Image
import os, glob
import argparse

parser = argparse.ArgumentParser(description = 'Resizing images')
parser.add_argument('rVal', type = int, help = 'Resize factor')
args = parser.parse_args()
rVal = args.rVal

for fileName in glob.glob('*.jpg'):
	file, ext = os.path.splitext(fileName)
	im = Image.open(fileName)
	size = im.width // rVal, im.height // rVal
	im2 = im.resize(size)
	im2.save('compressed/x' + str(rVal) + '_' + file + '_compressed.jpg', 'JPEG')
	print(file + ' was saved')