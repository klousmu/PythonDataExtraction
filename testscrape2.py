import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        
        for i, page in enumerate(pdf.pages):
            if i !=5:
                continue
            for table in page.find_tables():
                txt = table.extract(x_tolerance = 0.5,y_tolerance = 0.5)
                #df = pd.DataFrame(table[1:], columns=table[0])
                tables.append((page,txt))
        
        '''
        for i, page in enumerate(pdf.pages):
            if i != 5:
                continue
            tables.append((page,page.extract_text(x_tolerance = 0.5,y_tolerance = 0.5))) #x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None, **kwargs)
        '''
    return tables

def save_to_excel(dfs, excel_path):
    #with pd.ExcelWriter(excel_path) as writer:
        for i, j in enumerate(dfs):
            #j[1].to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)
            print(f" text: {j[1]}")
            print(f" page: {j[0]}")
            #print(f" text: {j[2]}")

def main(source='pdf', path_or_url=''):
    path_or_url = "C:\\Users\\kyle\\Downloads\\lazards-lcoeplus-april-2023.pdf"
    if source == 'web':
        dfs = extract_tables_from_web(path_or_url)
    elif source == 'pdf':
        dfs = extract_tables_from_pdf(path_or_url)
    else:
        print("Unsupported source. Choose 'web' or 'pdf'.")
        return

    output_path = 'output.xlsx'
    save_to_excel(dfs, output_path)
    print(f"Data saved to {output_path}")
