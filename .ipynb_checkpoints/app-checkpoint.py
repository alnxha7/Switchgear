{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "28e547c5-c73f-45fe-be2b-b1ebc437cf95",
   "metadata": {},
   "outputs": [],
   "source": [
    "import PyPDF2\n",
    "import os\n",
    "import pandas as pd\n",
    "from natsort import natsorted"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "6184dff0-3c0a-4955-a058-fcc0b3d9db13",
   "metadata": {},
   "outputs": [],
   "source": [
    "input_pdf_path = 'input_pdf/LVP&SMDB.pdf'\n",
    "output_directory = r\"output/pdf/\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "300c7ed0-1c82-4bba-95c6-7aaf51aead4c",
   "metadata": {},
   "outputs": [],
   "source": [
    "os.makedirs(output_directory, exist_ok=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "c23e78a8-0b0e-4f6b-85c0-53e67dd5c9b4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Extraction of pdf completed!\n"
     ]
    }
   ],
   "source": [
    "with open(input_pdf_path, 'rb') as file:\n",
    "    pdf_reader = PyPDF2.PdfReader(file)\n",
    "    for page_num in range(21):\n",
    "        pdf_writer = PyPDF2.PdfWriter()\n",
    "        pdf_writer.add_page(pdf_reader.pages[page_num])\n",
    "\n",
    "        output_path = os.path.join(output_directory, f'page_{page_num + 1}.pdf')\n",
    "\n",
    "        with open(output_path, 'wb') as output_file:\n",
    "            pdf_writer.write(output_file)\n",
    "print('Extraction of pdf completed!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "d1146efe-f299-46c3-8f60-c4031b336f92",
   "metadata": {},
   "outputs": [],
   "source": [
    "pdf_directory = r'output/pdf/'\n",
    "excel_directory = r'output/excel/'\n",
    "data = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "e2f7cc98-93c0-4280-b12f-f482d5754a71",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Conversion to Excel complete!\n"
     ]
    }
   ],
   "source": [
    "import aspose.pdf as ap\n",
    "\n",
    "for filename in os.listdir(pdf_directory):\n",
    "    if filename.endswith('.pdf'):\n",
    "        pdf_path = os.path.join(pdf_directory, filename)\n",
    "        document = ap.Document(pdf_path)\n",
    "        excel_filename = f'{os.path.splitext(filename)[0]}.xlsx'\n",
    "        excel_path = os.path.join(excel_directory, excel_filename)\n",
    "        save_option = ap.ExcelSaveOptions()\n",
    "        document.save(excel_path, save_option)\n",
    "print('Conversion to Excel complete!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "93f3f77a-7287-4d61-89f7-8106bf03c737",
   "metadata": {},
   "outputs": [],
   "source": [
    "df1 = pd.read_excel(r'output/excel/page_1.xlsx')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "d251caeb-af5f-46c2-a25f-7ab663504e6f",
   "metadata": {},
   "outputs": [],
   "source": [
    "sliced_dfs = {}\n",
    "excel_files = natsorted([f for f in os.listdir(excel_directory) if f.endswith('.xlsx')])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "276f5a8a-a530-435b-ad35-519c51502b11",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Slicing, storing, and saving DataFrames complete!\n"
     ]
    }
   ],
   "source": [
    "for idx, filename in enumerate(excel_files):\n",
    "    excel_path = os.path.join(excel_directory, filename)\n",
    "    \n",
    "    # Load the Excel file into a DataFrame\n",
    "    df = pd.read_excel(excel_path)\n",
    "    \n",
    "    # Slice the DataFrame (rows 4 to 30)\n",
    "    sliced_df = df.iloc[4:31]\n",
    "    \n",
    "    # Store the sliced DataFrame in the dictionary\n",
    "    key = f'df{idx + 1}'\n",
    "    sliced_dfs[key] = sliced_df\n",
    "\n",
    "    # Save the sliced DataFrame to a CSV file\n",
    "    csv_filename = f'{key}.csv'\n",
    "    csv_path = os.path.join(excel_directory, csv_filename)\n",
    "    sliced_dfs[key].to_csv(csv_path, index=False)\n",
    "\n",
    "print('Slicing, storing, and saving DataFrames complete!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "c37e9bb9-7522-493c-91a0-3fde4df78a81",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Total number of rows with only NaN values: 93\n"
     ]
    }
   ],
   "source": [
    "total_nan_rows = 0\n",
    "for key, sliced_df in sliced_dfs.items():\n",
    "    nan_rows_count = sliced_df.isna().all(axis=1).sum()\n",
    "    total_nan_rows += nan_rows_count\n",
    "print(f'Total number of rows with only NaN values: {total_nan_rows}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "860baabb-6b8d-4fe9-be68-150d36c8dc85",
   "metadata": {},
   "outputs": [],
   "source": [
    "cleaned_dfs = {}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "dbb62d08-6889-4908-9b4e-3798373d0573",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Rows with only NaN values have been removed from all DataFrames.\n"
     ]
    }
   ],
   "source": [
    "for idx, (key, df) in enumerate(sliced_dfs.items(), start=1):\n",
    "    # Ensure working with a copy to avoid warnings\n",
    "    df = df.copy()\n",
    "    \n",
    "    # Drop rows where all elements are NaN\n",
    "    cleaned_df = df.dropna(how='all').copy()\n",
    "    \n",
    "    # Dynamically create a key like df1, df2, etc.\n",
    "    cleaned_dfs[f'df{idx}'] = cleaned_df\n",
    "print('Rows with only NaN values have been removed from all DataFrames.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "234b0a52-ee58-40e7-946c-77fb8451b364",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Third column has been renamed to \"MCB\" in all DataFrames.\n"
     ]
    }
   ],
   "source": [
    "for key, df in cleaned_dfs.items():\n",
    "    # Check if the DataFrame has at least three columns\n",
    "    if df.shape[1] >= 3:\n",
    "        # Rename the third column to 'MCB'\n",
    "        df.columns = [df.columns[0], df.columns[1], 'MCB'] + list(df.columns[3:])\n",
    "print('Third column has been renamed to \"MCB\" in all DataFrames.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "95dd484a-d7cf-415e-9a0f-f3f29e009a93",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter the value:  LVP-01\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "df1: \"LVP-01\" MCB value 1600 @0.85.\n",
      "df2: No matching rows found for the value \"LVP-01\"\n",
      "df3: No matching rows found for the value \"LVP-01\"\n",
      "df4: No matching rows found for the value \"LVP-01\"\n",
      "df5: No matching rows found for the value \"LVP-01\"\n",
      "df6: No matching rows found for the value \"LVP-01\"\n",
      "df7: No matching rows found for the value \"LVP-01\"\n",
      "df8: No matching rows found for the value \"LVP-01\"\n",
      "df9: No matching rows found for the value \"LVP-01\"\n",
      "df10: No matching rows found for the value \"LVP-01\"\n",
      "df11: No matching rows found for the value \"LVP-01\"\n",
      "df12: No matching rows found for the value \"LVP-01\"\n",
      "df13: No matching rows found for the value \"LVP-01\"\n",
      "df14: No matching rows found for the value \"LVP-01\"\n",
      "df15: No matching rows found for the value \"LVP-01\"\n",
      "df16: No matching rows found for the value \"LVP-01\"\n",
      "df17: No matching rows found for the value \"LVP-01\"\n",
      "df18: No matching rows found for the value \"LVP-01\"\n",
      "df19: No matching rows found for the value \"LVP-01\"\n",
      "df20: No matching rows found for the value \"LVP-01\"\n",
      "df21: No matching rows found for the value \"LVP-01\"\n",
      "Finished retrieving \"MCB\" column values.\n"
     ]
    }
   ],
   "source": [
    "search_value = input('Enter the value: ')\n",
    "\n",
    "for key, df in cleaned_dfs.items():\n",
    "    # Check if the DataFrame has at least three columns and the 'MCB' column\n",
    "    if df.shape[1] >= 3 and 'MCB' in df.columns:\n",
    "        # Retrieve the value from the 'MCB' column where the first column matches search_value\n",
    "        matching_row = df[df.iloc[:, 0] == search_value]\n",
    "        \n",
    "        if not matching_row.empty:\n",
    "            mcb_value = matching_row['MCB'].values[0]\n",
    "            print(f'{key}: \"{search_value}\" MCB value {mcb_value}.')\n",
    "        else:\n",
    "            print(f'{key}: No matching rows found for the value \"{search_value}\"')\n",
    "    else:\n",
    "        print(f'{key}: DataFrame does not contain the required columns.')\n",
    "\n",
    "print('Finished retrieving \"MCB\" column values.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "d0b196ba-1b4f-4938-9d27-307258fa64b4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "df1: The value \"LVP-01\" with MCB value \"1600 @0.85\" appears 1 times.\n",
      "The combination of \"LVP-01\" and \"1600 @0.85\" appears in: df1.\n"
     ]
    }
   ],
   "source": [
    "if mcb_value is None:\n",
    "    print(f'No MCB value found for the search value \"{search_value}\".')\n",
    "else:\n",
    "    # Track DataFrames that contain the (search_value, mcb_value) pair\n",
    "    dataframes_with_value = []\n",
    "\n",
    "    for key, df in cleaned_dfs.items():\n",
    "        if df.shape[1] >= 3 and 'MCB' in df.columns:\n",
    "            # Find rows where the first column matches search_value and MCB column matches mcb_value\n",
    "            matching_rows = df[(df.iloc[:, 0] == search_value) & (df['MCB'] == mcb_value)]\n",
    "            \n",
    "            if not matching_rows.empty:\n",
    "                # Print the DataFrame key and the count of matching rows\n",
    "                count = matching_rows.shape[0]\n",
    "                dataframes_with_value.append(key)\n",
    "                print(f'{key}: The value \"{search_value}\" with MCB value \"{mcb_value}\" appears {count} times.')\n",
    "\n",
    "    if not dataframes_with_value:\n",
    "        print(f'The combination of \"{search_value}\" and \"{mcb_value}\" does not appear in any DataFrame.')\n",
    "    else:\n",
    "        print(f'The combination of \"{search_value}\" and \"{mcb_value}\" appears in: {\", \".join(dataframes_with_value)}.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7f969c99-a84f-483e-83a2-e1aa76b7d563",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "99db9d32-317d-4729-b204-b50c0f9692e5",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
