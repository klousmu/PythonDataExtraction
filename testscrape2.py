import pdfplumber
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO


def extract_tables_from_web(url):
    response = requests.get(url)
    html_content = response.text
    # Wrap the HTML string in a StringIO object
    string_data = StringIO(html_content)
    dfs = pd.read_html(string_data)  # Use the StringIO object
    return dfs

'''
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    dfs = pd.read_html(str(tables))
    return dfs
'''

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        
        '''
        for i, page in enumerate(pdf.pages):
            if i !=5:
                continue
        '''
            #for table in page.find_tables():
         refor table in page.extract_tables():
                #txt = table.extract(x_tolerance = 0.5,y_tolerance = 0.5)
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
                #tables.append((page,txt))
        
        '''
        for i, page in enumerate(pdf.pages):
            if i != 5:
                continue
            tables.append((page,page.extract_text(x_tolerance = 0.5,y_tolerance = 0.5))) #x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None, **kwargs)
        '''
    return tables
#
def save_to_excel(dfs, excel_path):
    with pd.ExcelWriter(excel_path) as writer:
        for i, df in enumerate(dfs):
            df.to_excel(writer, sheet_name=f'Sheet{i+1}')
            #print(f" text: {j[1]}")
            #print(f" page: {j[0]}")
            #print(f" text: {j[2]}")

def main(source, path_or_url):
    #path_or_url = "C:\\Users\\kyle\\Downloads\\lazards-lcoeplus-april-2023.pdf"
    
    if source == 'web':
        dfs = extract_tables_from_web(path_or_url)
    elif source == 'pdf':
        dfs = extract_tables_from_pdf(path_or_url)
    else:
        print("Unsupported source. Choose 'web' or 'pdf'.")
        return

    output_path = 'testeia.xlsx'
    save_to_excel(dfs, output_path)
    print(f"Data saved to {output_path}")

# Example usage:
# main('web', 'https://example.com/tablepage')

# main('pdf', '/path/to/file.pdf')
