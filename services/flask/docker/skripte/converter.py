import os
from pdf2image import convert_from_path

def convert_pdf_to_tif(file_path, output_path):
    images = convert_from_path(file_path)
    page_counter = len(images) 
    for page in range(page_counter):
        images[page].save(output_path + "_" + str(page) + '.tif', 'tiff')
