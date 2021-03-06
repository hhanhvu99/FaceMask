import os
import shutil
import glob
import xml.etree.ElementTree as ET
import argparse
import random


'''
Nguồn: https://github.com/skanelo/Face-Mask-Detection/blob/main/xml_to_yolo.py
'''


def convert(size: tuple, box: list):
	"""Takes as input:  (width, height) of an image
						(xmin, ymin, xmax, ymax) of the bounding box
	   and returns (x, y, w, h) of the bounding box in yolo format.
	"""
	dw = 1. / size[0]
	dh = 1. / size[1]
	x = (box[2] + box[0]) / 2.0
	y = (box[3] + box[1]) / 2.0
	w = abs(box[2] - box[0])
	h = abs(box[3] - box[1])
	x = x * dw
	w = w * dw
	y = y * dh
	h = h * dh

	return (x, y, w, h)


def xml_to_txt(input_path: str, output_path: str):
	"""Iterates through all .xml files (generated by labelImg) in the given directory,
	and generates .txt files that comply with yolo format for each .xml file.
	"""
	class_mapping = {'with_mask': '0',
					 'without_mask': '1',
					 'mask_weared_incorrect': '1'}

	if not glob.glob(input_path + '/*.xml'):
		raise (ValueError(f"Empty folder, there are no .xml files in {input_path}."))

	for xml_file in glob.glob(input_path + '/*.xml'):
		tree = ET.parse(xml_file)
		root = tree.getroot()

		txt_list = []
		for member in root.findall("object"):
			f_name = root.find("filename").text
			width, height = int(root.find('size')[0].text), int(root.find("size")[1].text)
			c = member[0].text

			b = float(member[5][0].text), float(member[5][1].text), float(member[5][2].text), float(member[5][3].text)
			bb = convert((width, height), b)

			txt_list.append(class_mapping.get(c) + " " + " ".join([str(l) for l in bb]) + "\n")

		print(f"Building: {f_name.split('.')[0]}.txt")
		with open(output_path + "\\" + f_name.split(".")[0] + ".txt", "w") as writer:
			for obj in txt_list:
				writer.write(obj)


'''
Nguồn: https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth/13814557
'''
def copy_images(src_path: str, des_path: str):
	count = 0

	for item in os.listdir(src_path):
		count += 1
		s = os.path.join(os.path.abspath(src_path), item)
		d = os.path.join(os.path.abspath(des_path), item)
		if os.path.isdir(s):
			shutil.copytree(s, d, False, None)
		else:
			shutil.copy(s, d)

	return count


def split_train_test(train_path: str, test_path: str, numberOfData, testPercent):
	listOfTest = random.sample(range(numberOfData), int(numberOfData/100 * testPercent))

	''' Xóa các file trong test'''
	folder = os.path.abspath(test_path)
	for filename in os.listdir(test_path):
		file_path = os.path.join(folder, filename)

		if os.path.isfile(file_path) or os.path.islink(file_path):
			os.unlink(file_path)

	''' Di chuyển file sang test '''
	for fileNumber in listOfTest:
		fileTxtSrc = os.path.join(os.path.abspath(train_path), "maksssksksss" + str(fileNumber) + ".txt")
		fileImgSrc = os.path.join(os.path.abspath(train_path), "maksssksksss" + str(fileNumber) + ".png")

		fileTxtDes = os.path.join(os.path.abspath(test_path), "maksssksksss" + str(fileNumber) + ".txt")
		fileImgDes = os.path.join(os.path.abspath(test_path), "maksssksksss" + str(fileNumber) + ".png")

		os.replace(fileTxtSrc, fileTxtDes)
		os.replace(fileImgSrc, fileImgDes)


def parser() -> None:
	parser = argparse.ArgumentParser(
		description="Converts .xlm annotations into .txt files that conform to yolo format.")
	parser.add_argument("--inputAnno", type=str, default="",
						help="The path of the input annotation folder that contains the .png images with their corresponding txt annotations.")
	parser.add_argument("--inputImages", type=str, default="",
						help="The path of the input image folder that contains the .png images with their corresponding txt annotations.")
	parser.add_argument("--outputTrain", type=str, default="",
						help="The path of the output train folder in which .txt annotations will be saved.")
	parser.add_argument("--outputTest", type=str, default="",
						help="The path of the output test folder in which .txt annotations will be saved.")
	return parser.parse_args()


def check_arguments_errors(args: argparse.Namespace) -> None:
	if not os.path.exists(args.inputAnno):
		raise (ValueError(f"Invalid input folder path: {os.path.abspath(args.inputAnno)}"))
	if not os.path.exists(args.inputImages):
		raise (ValueError(f"Invalid input folder path: {os.path.abspath(args.inputImages)}"))
	if not os.path.exists(args.outputTrain):
		raise (ValueError(f"Invalid output folder path: {os.path.abspath(args.outputTrain)}"))
	if not os.path.exists(args.outputTest):
		raise (ValueError(f"Invalid output folder path: {os.path.abspath(args.outputTest)}"))


def main() -> None:
	args = parser()
	check_arguments_errors(args)
	xml_to_txt(args.inputAnno, args.outputTrain)
	numberOfData = copy_images(args.inputImages, args.outputTrain)
	split_train_test(args.outputTrain, args.outputTest, numberOfData, 10)


if __name__ == "__main__":
	main()