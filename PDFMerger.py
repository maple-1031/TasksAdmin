# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:13:43 2021

@author: maple
"""

from pathlib import Path
import PyPDF2

def pdfMerger(mdir, save_name):
    pdf_dir = Path(mdir)
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    
    pdf_writer = PyPDF2.PdfFileWriter()
    for pdf_file in pdf_files:
        pdf_reader = PyPDF2.PdfFileReader(str(pdf_file))
        for i in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(i))
            
    with open(save_name, "wb") as f:
        pdf_writer.write(f)
    