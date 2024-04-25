import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_tables_from_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    dfs = pd.read_html(str(tables))
    return dfs

import pdfplumber

#def clean_text(df):
    #"""Cleans dataframe text by removing excessive spaces."""
    #for col in df.columns:
        #df.loc[:, col] = df.loc[:, col].apply(lambda x: ' '.join(str(x).split()))
    #return df

def clean_text(text):
    if isinstance(text, str):
        return ' '.join(text.split())
    return text

def clean_dataframe_applymap(df):
    return df.map(clean_text)

def extract_tables_from_pdf(pdf_path, x_tolerance=3, y_tolerance=3):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i!=5:
                continue
            # Use the tolerance values in the extract_tables method
            for table in page.extract_tables({
                "vertical_strategy": "text", 
                "horizontal_strategy": "text",
                "explicit_vertical_lines": [],
                "explicit_horizontal_lines": [],
                "snap_tolerance": 3,
                "join_tolerance": 3,
                "edge_min_length": 3,
                "min_words_vertical": 3,
                "min_words_horizontal": 1,
                
                "text_tolerance": 3,
                "text_x_tolerance": x_tolerance,
                "text_y_tolerance": y_tolerance,
                "intersection_x_tolerance": x_tolerance,
                "intersection_y_tolerance": y_tolerance
            }):
                df = pd.DataFrame(table[1:], columns=table[0])
                df = clean_dataframe_applymap(df)
                tables.append(df)
    return tables


def save_to_excel(dfs, excel_path):
    print(dfs[0].to_string().split('\n')[0])
    #with pd.ExcelWriter(excel_path) as writer:
        #for i, df in enumerate(dfs):
            #print(df.to_string())
           # df.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)
            
def main(source='pdf', path_or_url=''):
    path_or_url = "C:\\Users\\kyle\\Downloads\\lazards-lcoeplus-april-2023.pdf"
    if source == 'web':
        dfs = extract_tables_from_web(path_or_url)
    elif source == 'pdf':
        t=0
        for i in range(2):
            dfs = extract_tables_from_pdf(path_or_url, x_tolerance=t, y_tolerance=t)
            t+=0.1
            print(i)
            output_path = 'output.xlsx'
            save_to_excel(dfs, output_path)
    else:
        print("Unsupported source. Choose 'web' or 'pdf'.")
        return

    output_path = 'output.xlsx'
    #save_to_excel(dfs, output_path)
    print(f"Data saved to {output_path}")

# Example usage:
# main('web', 'https://example.com/tablepage')

# main('pdf', '/path/to/file.pdf')
