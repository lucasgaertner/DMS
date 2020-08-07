def folder_check(sys_folder, data_path, new_folder_path):
	import os
	train_folders = os.listdir(data_path)
	for folder in sys_folder:
		# Check existing folders
		if folder in train_folders:    
			train_folders.remove(folder)
		# Setting not existing extraction folder
		elif folder not in train_folders:
			print(folder)
			try:
				os.mkdir(new_folder_path + "/" + folder)
			except:
				pass # Logging
			for doc_type_folder in train_folders:
				try:
					os.mkdir(new_folder_path + "/" + folder + "/" + doc_type_folder)
				except:
					pass #Logging
			train_folders.append(folder)
			train_folders.remove(folder)
	return train_folders
