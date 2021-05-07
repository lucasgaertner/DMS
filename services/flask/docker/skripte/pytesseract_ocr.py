def get_text_from_tif(data_path, file_name):
	try:
		import os
		import pytesseract
		import cv2
		import re
		from PIL import Image
	except ImportError:
		import Image
	txt_path = 'extracted_text'

	for files in os.listdir(os.path.join(data_path, "tif")):
		if file_name in files:
			print(files)
			file = re.search(r'(.+)(.pdf|.PDF)(_[0-9]+)(.tif)', files)#(.+)(.pdf|.PDF)(.+)?
			file = file.group(1) + file.group(3)
			img = cv2.imread(os.path.join(data_path, "tif", files))
			extracted_text = pytesseract.image_to_string(img)
			joined_file = open(os.path.join(data_path, txt_path, file + ".txt"),"w")
			joined_file.write(extracted_text)
			joined_file.close()

def merge_files(data_path, file_name): 
	#document_type, data_path
	import os
	import re
	extracted_text_folders = os.path.join(data_path, "extracted_text")
	joined_text_folders = os.path.join(data_path, "joined_text")
	
	for files in os.listdir(extracted_text_folders):
		if file_name[:-4] in files:
			read_file = open(os.path.join(extracted_text_folders, files), "r")
			write_merged_file = open(os.path.join(joined_text_folders, file_name[:-4]) + ".txt", "a+")
			write_merged_file.write(read_file.read())
			read_file.close()
			write_merged_file.close()
	getFile = open(os.path.join(joined_text_folders, file_name[:-4]) + ".txt", "r")
	textList = [x.strip() for x in getFile.readlines() if x.strip() != '' ]

	getText = ' '.join(textList)
	return getText

