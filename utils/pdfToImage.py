import os
from pdf2image import convert_from_path
import cv2

def pdfToImage(path_file, DOWNLOAD_FOLDER, element):
    
    pages = convert_from_path(path_file, dpi = 220, poppler_path = r'C:\Program Files\poppler-23.07.0\Library\bin')
    image_counter = 1
    page_lst = []
    
    for page in pages:
        filename = os.path.join(DOWNLOAD_FOLDER, f"{image_counter-1}_{element}.jpg")
        page.save(filename, 'JPEG')
        p_img = cv2.imread(filename)
        
        height, width, channel = p_img.shape
        page_lst.append(filename)
        image_counter += 1
    
    filelimit = image_counter - 1
    print('Totoal no. of Pages:', filelimit)
    return page_lst