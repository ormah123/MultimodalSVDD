import datetime
import glob
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil  # for CPU and memory usage monitoring
import tensorflow as tf
from tqdm import tqdm  # for progress bar


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

# Create a new directory for images
if not os.path.exists('Images'):
    os.makedirs('Images')

# Scan the Data folder and subfolders to detect all csv files
data_files = glob.glob(os.path.join('Data', '**/*.csv'), recursive=True)
print('Detected %d csv files in the Data folder and subfolders' % len(data_files))

# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(20,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),
              loss=tf.losses.MeanSquaredError())

# Define the progress bar
pbar = tqdm(total=len(data_files), desc='Processed files', position=0)

# Start processing data files
for f in data_files:
    try:
        # Load the data
        data = np.loadtxt(f, delimiter=',')
        if data.ndim == 1:
            data = data.reshape(1, -1) # reshape if the data has only one sample

        # If shape is incompatible, reduce to 20 and try to process again
        if data.shape[1] != 20:
            data = data[:, :20]
            if data.ndim == 1:
                data = data.reshape(1, -1) # reshape if the data has only one sample

        # Train the model
        model.fit(data, data, epochs=100, batch_size=32, verbose=0)

        # Predict the reconstruction error
        reconstruction_error = np.mean(np.square(data - model.predict(data)), axis=1)

        # Set the threshold for anomaly detection
        threshold = np.percentile(reconstruction_error, 95)

        # Detect anomalies
        anomalies = data[reconstruction_error > threshold]

        # Print the number of anomalies detected
        print('Detected %d anomalies in %s' % (anomalies.shape[0], f))

        # Update the progress bar with CPU and memory usage information
        mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        cpu_usage = psutil.cpu_percent()
        pbar.set_postfix({'Memory (MB)': mem_usage, 'CPU (%)': cpu_usage})
        pbar.update(1)

        # Wait for a short period to make the progress bar look real-time
        time.sleep(0.1)

        # Save the anomalies as an image in the Images folder
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(data, label='Data')
        ax.scatter(anomalies, anomalies, label='Anomalies', color='green')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.set_title('Anomalies Detected')
        ax.legend()
        plt.savefig(os.path.join('Images', os.path.basename(f).replace('.csv', '.png')))
        plt.close()

    except Exception as e:
        print('Error processing file: %s' % f)
        print('Error successfully diverted')
        continue

# Close the progress bar
pbar.close()
