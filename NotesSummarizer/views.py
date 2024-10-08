from django.shortcuts import render
from django.http import HttpResponse
import os
import easyocr
from decouple import config
from fpdf import FPDF
from utils.emptyDir import empty_dir
from utils.pdfToImage import pdfToImage
from utils.summarizeText import summarizeText
from utils.summaryPDF import create_summary_pdf
# from utils.cleanText import cleanText

def home(request):
    return render(request, 'home.html')

def upload_file(request):
    if request.method == 'POST':
        if 'notesFile' in request.FILES:
            
            noteFile = request.FILES['notesFile']
            
            current_directory = os.path.dirname(__file__)
            outputpath = os.path.join(current_directory, "Dir2")
            inputpath = os.path.join(current_directory, "Dir1")
            txt_files_path = os.path.join(current_directory, 'txtFiles')
            
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
            
            reader = easyocr.Reader(['en'])
            text = ""
            
            # process each generated image directory
            for subdir in files_out:
                subdir_path = os.path.join(outputpath, subdir)
                if os.path.isdir(subdir_path):
                    images = os.listdir(subdir_path)
                    
                    for img in images:
                        img_path = os.path.join(subdir_path, img)
                        print(f"Processing image:", {img_path})
                        
                        output = reader.readtext(img_path)
                        for item in output:
                            text += item[1] + "\n"
                            
            
            # text = cleanText(text)                
            summary_text_path = os.path.join(txt_files_path, "output.txt")
            summary = summarizeText(text)
            
            output_text_path = os.path.join(txt_files_path, "output.txt")
            with open(output_text_path, "w") as text_file:
                text_file.write(summary)
            
            create_summary_pdf(summary_text_path, os.path.join(txt_files_path, "Summary.pdf"))
            
            empty_dir(outputpath)
            empty_dir(inputpath)
            
    return render(request, "summary.html") 

def download_file(request):
    
    current_dir = os.path.dirname(__file__)
    pdf_dir = os.path.join(current_dir, "txtFiles")
    
    pdf_file = None
    files_in_dir = os.listdir(pdf_dir)
    
    for file_name in files_in_dir:
        if file_name.lower().endswith(".pdf"):
            pdf_file = file_name
            break
        
    if pdf_file:
        pdf_file_path = os.path.join(pdf_dir, pdf_file)
        
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type = 'application/pdf')
            
        response['Content-Disposition'] = f'attachment; filename= "{os.path.basename(pdf_file_path)}"'       
        return response
    else:
        return HttpResponse("No PDF Found", status=404)                           