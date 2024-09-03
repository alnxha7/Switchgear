import PyPDF2
import os
import pandas as pd
from natsort import natsorted
import sys

input_pdf_path = sys.argv[1]
output_directory = sys.argv[2]

os.makedirs(output_directory, exist_ok=True)

with open(input_pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    for page_num in range(21):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])

        output_path = os.path.join(output_directory, f'page_{page_num + 1}.pdf')

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
print('Extraction of pdf completed!')

excel_directory = os.path.join(output_directory, "excel")
pdf_directory = os.path.join(output_directory, "pdf")

os.makedirs(pdf_directory, exist_ok=True)
os.makedirs(excel_directory, exist_ok=True)

data = []

import aspose.pdf as ap

for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        document = ap.Document(pdf_path)
        excel_filename = f'{os.path.splitext(filename)[0]}.xlsx'
        excel_path = os.path.join(excel_directory, excel_filename)
        save_option = ap.ExcelSaveOptions()
        document.save(excel_path, save_option)
print('Conversion to Excel complete!')

df1 = pd.read_excel(r'output/excel/page_1.xlsx')

sliced_dfs = {}
excel_files = natsorted([f for f in os.listdir(excel_directory) if f.endswith('.xlsx')])

for idx, filename in enumerate(excel_files):
    excel_path = os.path.join(excel_directory, filename)
    
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_path)
    
    # Slice the DataFrame (rows 4 to 30)
    sliced_df = df.iloc[0:33]
    
    # Store the sliced DataFrame in the dictionary
    key = f'df{idx + 1}'
    sliced_dfs[key] = sliced_df

    # Save the sliced DataFrame to a CSV file
    csv_filename = f'{key}.csv'
    csv_path = os.path.join(excel_directory, csv_filename)
    sliced_dfs[key].to_csv(csv_path, index=False)

print('Slicing, storing, and saving DataFrames complete!')

total_nan_rows = 0
for key, sliced_df in sliced_dfs.items():
    nan_rows_count = sliced_df.isna().all(axis=1).sum()
    total_nan_rows += nan_rows_count
print(f'Total number of rows with only NaN values: {total_nan_rows}')

cleaned_dfs = {}
for idx, (key, df) in enumerate(sliced_dfs.items(), start=1):
    # Ensure working with a copy to avoid warnings
    df = df.copy()
    
    # Drop rows where all elements are NaN
    cleaned_df = df.dropna(how='all').copy()
    
    # Dynamically create a key like df1, df2, etc.
    cleaned_dfs[f'df{idx}'] = cleaned_df
print('Rows with only NaN values have been removed from all DataFrames.')

for key, df in cleaned_dfs.items():
    # Check if the DataFrame has at least five columns
    if df.shape[1] >= 6:
        # Rename the columns as specified
        df.columns = [
            df.columns[0],  # Keep the first column name unchanged
            'POLE',
            'FS/IS', # Rename the third column to 'ACB'
            'ACB/MCCB',         # Rename the fourth column to 'MCCB'
            'MCB',          # Rename the fifth column to 'MCB'
            'FAULT DUTY'    # Rename the sixth column to 'FAULT DUTY'
        ] + list(df.columns[6:])  # Keep the remaining columns unchanged

        # Keep only the first 8 columns
        df = df.iloc[:, :8]
        
        cleaned_dfs[key] = df

print('Columns have been renamed and trimmed to the first 8 columns in all DataFrames.')

combined_df = pd.concat(cleaned_dfs.values(), ignore_index=True)

# Count occurrences of each product in the first column
product_counts = combined_df.iloc[:, 0].value_counts().to_dict()

# Add the count column to each DataFrame in cleaned_dfs
for key, df in cleaned_dfs.items():
    # Use .loc[] to avoid SettingWithCopyWarning
    df['Count'] = df.iloc[:, 0].map(product_counts).fillna(0).astype(int)

    # Update the DataFrame in the dictionary
    cleaned_dfs[key] = df

print('Count column has been added to each DataFrame in cleaned_dfs.')

combined_df = pd.concat(cleaned_dfs.values(), ignore_index=True)

# Count occurrences of each product in the first column
product_counts = combined_df.iloc[:, 0].value_counts().to_dict()

# Add the count column to each DataFrame in cleaned_dfs
for key, df in cleaned_dfs.items():
    # Ensure we're working with a copy of the DataFrame to avoid SettingWithCopyWarning
    df_copy = df.copy()
    
    # Add the count column
    df_copy.loc[:, 'Count'] = df_copy.iloc[:, 0].map(product_counts).fillna(0).astype(int)
    
    # Update the DataFrame in the dictionary
    cleaned_dfs[key] = df_copy

print('Count column has been added as integers to all DataFrames in cleaned_dfs.')

cleaned_dfs['df10']

lv_dfs = []
smdb_dfs = []
db_dfs = []
other_dfs = []

# Define the pattern for identifying rows with "REF"
ref_pattern = "REF"

# Define a function to preprocess DataFrames
def preprocess_dataframe(df):
    # Keep rows where the first column contains "REF"
    ref_rows = df[df.iloc[:, 0].astype(str).str.contains(ref_pattern, na=False)]
    
    # Drop rows with more than 6 NaN values, except for rows with "REF"
    df_filtered = df[~df.index.isin(ref_rows.index)]  # Exclude REF rows from deletion
    df_filtered = df_filtered[df_filtered.isna().sum(axis=1) <= 5]
    
    # Concatenate REF rows back to the filtered DataFrame
    df_preprocessed = pd.concat([df_filtered, ref_rows]).sort_index()
    return df_preprocessed

# Define a function to categorize DataFrames
def categorize_dataframe(df):
    # Limit checking to the first 7 rows
    rows_to_check = df.head(7)
    
    # Check if any row in the first 7 rows contains "REF" in the first column
    for _, row in rows_to_check.iterrows():
        if ref_pattern in str(row.iloc[0]):
            # Check the values in the first 3 columns of the matched row
            first_column_value = str(row.iloc[0]).strip()
            second_column_value = str(row.iloc[1]).strip() if df.shape[1] > 1 else ""
            third_column_value = str(row.iloc[2]).strip() if df.shape[1] > 2 else ""
            
            # Categorize based on the content of the columns
            if "LV" in first_column_value or "LV" in second_column_value or "LV" in third_column_value:
                return 'LV'
            elif "SMDB" in first_column_value or "SMDB" in second_column_value or "SMDB" in third_column_value:
                return 'SMDB'
            elif "DB" in first_column_value or "DB" in second_column_value or "DB" in third_column_value:
                return 'DB'
            else:
                return 'Other'
    return 'Other'

# Iterate over each DataFrame in cleaned_dfs
for key, df in cleaned_dfs.items():
    print(f"Processing DataFrame: {key}")
    
    # Preprocess the DataFrame
    df = preprocess_dataframe(df)
    
    # Categorize the DataFrame
    category = categorize_dataframe(df)
    
    # Categorize DataFrames based on the determined category
    if category == 'LV':
        lv_dfs.append(df)
    elif category == 'SMDB':
        smdb_dfs.append(df)
    elif category == 'DB':
        db_dfs.append(df)
    else:
        other_dfs.append(df)

# Concatenate DataFrames for each category
lv_df = pd.concat(lv_dfs, ignore_index=True) if lv_dfs else pd.DataFrame()
smdb_df = pd.concat(smdb_dfs, ignore_index=True) if smdb_dfs else pd.DataFrame()
db_df = pd.concat(db_dfs, ignore_index=True) if db_dfs else pd.DataFrame()
other_df = pd.concat(other_dfs, ignore_index=True) if other_dfs else pd.DataFrame()

print('DataFrames have been categorized and combined into LV, SMDB, DB, and Others.')

# Optionally, check the lengths of the lists to ensure they contain DataFrames
print(f"Number of DataFrames in LV: {len(lv_dfs)}")
print(f"Number of DataFrames in SMDB: {len(smdb_dfs)}")
print(f"Number of DataFrames in DB: {len(db_dfs)}")
print(f"Number of DataFrames in Others: {len(other_dfs)}")

file_path = os.path.join(output_directory, 'categorized_dataframes.xlsx')

# Create an Excel writer object using openpyxl
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    # Ensure at least one DataFrame is written to ensure visibility
    sheets_written = False

    if not lv_df.empty:
        lv_df.to_excel(writer, sheet_name='COST LV', index=False)
        sheets_written = True
    if not smdb_df.empty:
        smdb_df.to_excel(writer, sheet_name='COST SMDB', index=False)
        sheets_written = True
    if not db_df.empty:
        db_df.to_excel(writer, sheet_name='COST DB', index=False)
        sheets_written = True
    if not other_df.empty:
        other_df.to_excel(writer, sheet_name='Others', index=False)
        sheets_written = True

    # Check if any sheets were actually written
    if not sheets_written:
        raise ValueError("No DataFrames were written to the Excel file. Ensure at least one DataFrame has data.")

print(file_path)

