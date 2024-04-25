import fitz
import pdfplumber
import pandas as pd


pdf_path = "C:\\Users\\kyle\\Downloads\\lazards-lcoeplus-april-2023.pdf"
tables = set()
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        for table in page.find_tables():
            #txt = table.extract(x_tolerance = 0.5,y_tolerance = 0.5)
            #df = pd.DataFrame(table[1:], columns=table[0])
            tables.add(i)
#unique = set(tables)
#print(tables)
pagelist = sorted(tables)


# Path for the output PDF file 
output_file = "C:\\Users\\kyle\\Downloads\\cutpdf.pdf"

# Opening the PDF file and creating a handle for it 
file_handle = fitz.open(pdf_path) 
'''
# The index (page no.) from where the pages are to be deleted 
start = 7

# The index to which the pages are to be deleted 
end = 56
'''
# Passing the pages to keep as arguments 
file_handle.select(pagelist)

# Saving the file 
file_handle.save(output_file)
            
#Reads a pdf and deletes any pages that don't have data
#Detected data might not be data
