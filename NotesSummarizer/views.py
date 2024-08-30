from django.shortcuts import render
from django.http import HttpResponse
import os
import easyocr
from groq import Groq
from decouple import config
from fpdf import FPDF
from utils.emptyDir import empty_dir
from utils.pdfToImage import pdfToImage

def home(request):
    return render(request, 'home.html')

def upload_file(request):
    if request.method == 'POST':
        if 'notesFile' in request.FILES:
            
            noteFile = request.FILES['notesFile']
            
            current_directory = os.path.dirname(__file__)
            outputpath = os.path.join(current_directory, "Dir2")
            inputpath = os.path.join(current_directory, "Dir1")
            
            file_path = os.path.join(inputpath, noteFile.name)
            
            empty_dir("Dir1")
            empty_dir("Dir2")
            
            # Save the files to specified path
            with open(file_path, 'wb') as destination:
                for chunk in noteFile.chunks():
                    destination.write(chunk)
            
            print("current directory:", current_directory)
            print("inputpath", inputpath)
            print("outputpath", outputpath)
            
            files = os.listdir(inputpath)
            print("Files:", files)
            
            # Process each PDF in the input directory
            for element in files:
                path = os.path.join(inputpath, element)
                print(path)
                element_name = os.path.splitext(element)[0] # element name in extension
                element_dir = os.path.join(outputpath, element_name + '_dir') # Dir for element
                os.makedirs(element_dir, exist_ok=True)
                
                # pdf to image
                pdfToImage(path, element_dir, element_name)
            
            files_out = os.listdir(outputpath)
            
            
            