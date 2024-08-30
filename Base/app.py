import PyPDF2
import os
import pandas as pd
from natsort import natsorted
import aspose.pdf as ap

def estimate(input_pdf_path, output_pdf_directory, output_excel_directory, pole_value, mccb_value, fault_duty_value):
    # Ensure output directories exist
    os.makedirs(output_pdf_directory, exist_ok=True)
    os.makedirs(output_excel_directory, exist_ok=True)

    # Extract pages from the PDF
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_path = os.path.join(output_pdf_directory, f'page_{page_num + 1}.pdf')

            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

    # Convert PDFs to Excel
    for filename in os.listdir(output_pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(output_pdf_directory, filename)
            document = ap.Document(pdf_path)
            excel_filename = f'{os.path.splitext(filename)[0]}.xlsx'
            excel_path = os.path.join(output_excel_directory, excel_filename)
            save_option = ap.ExcelSaveOptions()
            document.save(excel_path, save_option)

    # Load and process Excel files
    sliced_dfs = {}
    excel_files = natsorted([f for f in os.listdir(output_excel_directory) if f.endswith('.xlsx')])

    for idx, filename in enumerate(excel_files):
        excel_path = os.path.join(output_excel_directory, filename)
        df = pd.read_excel(excel_path)
        sliced_df = df.iloc[0:31]  # Adjust as necessary
        key = f'df{idx + 1}'
        sliced_dfs[key] = sliced_df

    cleaned_dfs = {}
    for idx, (key, df) in enumerate(sliced_dfs.items(), start=1):
        df = df.copy()
        cleaned_df = df.dropna(how='all').copy()
        cleaned_dfs[f'df{idx}'] = cleaned_df

    for key, df in cleaned_dfs.items():
        if df.shape[1] >= 6:
            df.columns = [
                df.columns[0],  
                'POLE',
                'ACCB',
                'MCCB',
                'MCB',
                'FAULT DUTY'
            ] + list(df.columns[6:])

    product_counts = {}
    for key, df in cleaned_dfs.items():
        if df.shape[1] >= 6:
            if 'POLE' in df.columns:
                product_series = df['POLE']
                for product in product_series:
                    if product in product_counts:
                        product_counts[product] += 1
                    else:
                        product_counts[product] = 1

    return product_counts