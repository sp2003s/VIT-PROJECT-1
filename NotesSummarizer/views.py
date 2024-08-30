from django.shortcuts import render
from django.http import HttpResponse
import os, shutil
from pdf2image import convert_from_path
import easyocr
import cv2
from groq import Groq
from decouple import config
from fpdf import FPDF

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