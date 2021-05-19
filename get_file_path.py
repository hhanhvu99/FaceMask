import argparse
import os

'''
Nguồn: https://github.com/skanelo/Face-Mask-Detection/blob/main/facemask_detector.ipynb
'''
def create_file_text(train_path: str, test_path: str):
	''' Tạo file chứa absolute path của tập train và tập test '''
	for dataset, txtname in zip([train_path, test_path], ['train.txt', 'test.txt']):
		image_files = []
		# Given we are already being located into /face_mask_detection folder
		os.chdir(os.path.abspath(dataset))
		for filename in os.listdir(os.getcwd()):
			if filename.endswith(".png"):
				image_files.append(os.path.abspath(os.getcwd()) + '/' + filename)

		os.chdir("..")
		with open(txtname, "w") as outfile:
			for image in image_files:
				outfile.write(image)
				outfile.write("\n")
			outfile.close()


def parser() -> None:
	parser = argparse.ArgumentParser(
		description="Converts .xlm annotations into .txt files that conform to yolo format.")
	parser.add_argument("--inputTrain", type=str, default="",
						help="The path of the input train folder that contains the .png images with their corresponding txt annotations.")
	parser.add_argument("--inputTest", type=str, default="",
						help="The path of the input test folder that contains the .png images with their corresponding txt annotations.")
	return parser.parse_args()


def check_arguments_errors(args: argparse.Namespace) -> None:
	if not os.path.exists(args.inputTrain):
		raise (ValueError(f"Invalid input folder path: {os.path.abspath(args.inputTrain)}"))
	if not os.path.exists(args.inputTest):
		raise (ValueError(f"Invalid input folder path: {os.path.abspath(args.inputTest)}"))


def main() -> None:
	args = parser()
	check_arguments_errors(args)
	create_file_text(args.inputTrain, args.inputTest)


if __name__ == "__main__":
	main()
