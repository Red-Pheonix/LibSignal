import os
import glob
import pandas as pd
import re

folder_path = 'robust grid4x4 experiments/maxpressure/'
pattern = os.path.join(folder_path, '*BRF.log')
matching_files = glob.glob(pattern)

# log_file = "robust grid4x4 experiments/fixedtime/robust_morning_1_BRF.log"
MODEL_NAME = "maxpressure"
MODE = "TRAIN"
EPISODE = 0
Q_LOSS = 0

def process_log_file(log_file):
    with open(log_file, 'r') as f:
        first_line = list(f)[0]
        travel_time, reward, queue, delay, throughoutput = re.findall(r'\d+\.\d+|\d+', first_line)
    
    items = [(MODEL_NAME, MODE, EPISODE, travel_time, Q_LOSS, reward, queue, delay, throughoutput)]
    df = pd.DataFrame(items, columns=[
        'model_name', 'mode', 'episode', 'travel_time', 'q_loss', 'reward',
        'queue', 'delay', 'throughoutput'])
    return df

# Print the list of matching files
for filename in matching_files:
    print(f"Processing {filename}...")
    df = process_log_file(filename)
    sub_folder_path = "/".join(filename.split("/")[:-1])
    csv_filename = filename.split("/")[-1].rstrip("_BRF.log") + ".csv"
    csv_filename = os.path.join(sub_folder_path, csv_filename)
    df.to_csv(csv_filename, index=False)

print("e")