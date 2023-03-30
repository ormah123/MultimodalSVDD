import os
import pandas as pd
import datetime

# define function to convert excel files to csv and txt files
def convert_files(folder_path):
    # initialize counters for number of files converted
    num_csv = 0
    num_txt = 0

    # loop through all subdirectories and files in the given folder path
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # check if file is an excel file
            if file.endswith(".xls") or file.endswith(".xlsx"):
                # create file paths for input and output files
                input_path = os.path.join(root, file)
                output_path_csv = os.path.join(root, file.split('.')[0] + '.csv')
                output_path_txt = os.path.join(root, file.split('.')[0] + '.txt')

                try:
                    # read excel file into pandas dataframe
                    df = pd.read_excel(input_path)
                    
                    # write dataframe to csv file
                    df.to_csv(output_path_csv, index=False)
                    print(f"[{datetime.datetime.now()}] {file} converted to {file.split('.')[0]}.csv")

                    # write dataframe to txt file
                    df.to_csv(output_path_txt, sep='\t', index=False)
                    print(f"[{datetime.datetime.now()}] {file} converted to {file.split('.')[0]}.txt")

                    # increment counter for number of files converted
                    num_csv += 1
                    num_txt += 1

                except Exception as e:
                    # print error message if file cannot be converted
                    print(f"[{datetime.datetime.now()}] Error converting {file}: {e}")
            
    # print total number of files converted
    print(f"\nTotal number of csv files converted: {num_csv}")
    print(f"Total number of txt files converted: {num_txt}")

# test function with given folder path
folder_path = 'Data'
convert_files(folder_path)
