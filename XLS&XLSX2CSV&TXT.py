import pandas as pd
import os
import datetime

data_dir = 'Data/'

# Recursively get a list of all Excel files in the data directory and its subdirectories
excel_files = []
for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            excel_files.append(os.path.join(subdir, file))

# Check if there are any Excel files to convert
if not excel_files:
    print(f'No Excel files found in {data_dir} and its subdirectories.')
else:
    # Convert all Excel files to CSV and TXT files with the same name
    num_files_converted = 0
    for file in excel_files:
        excel_path = file
        base_path = os.path.splitext(file)[0]
        csv_path = base_path + '.csv'
        txt_path = base_path + '.txt'
        if file.endswith('.xlsx'):
            df = pd.read_excel(excel_path)
        elif file.endswith('.xls'):
            df = pd.read_excel(excel_path, engine='xlrd')
        df.to_csv(csv_path, index=False)
        df.to_csv(txt_path, index=False, sep='\t')
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{current_time}: Converted {excel_path} to {csv_path} and {txt_path}')
        num_files_converted += 1

    print(f'Total number of files converted: {num_files_converted}')
