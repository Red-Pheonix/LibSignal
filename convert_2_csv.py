import os
import glob
import pandas as pd

def process_log_file(log_file):

    items = []

    with open(log_file, 'r') as file:
        for line in file:
            model_name, mode, episode, travel_time, q_loss, reward, queue, delay, throughoutput = line.strip().split()
            item = (model_name, mode, episode, travel_time, q_loss, reward, queue, delay, throughoutput)
            items.append(item)

    df = pd.DataFrame(items, columns=[
        'model_name', 'mode', 'episode', 'travel_time', 'q_loss', 'reward',
        'queue', 'delay', 'throughoutput'])

    final_df = df[df['mode'] == 'TRAIN']

    return final_df

folder_path = 'ingo_experiments/*/'
pattern = os.path.join(folder_path, '*DTL.log')
matching_files = glob.glob(pattern)

# Print the list of matching files
for filename in matching_files:
    print(f"Processing {filename}...")
    df = process_log_file(filename)
    sub_folder_path = "/".join(filename.split("/")[:-1])
    csv_filename = filename.split("/")[-1].rstrip("DTL.log").rstrip("_") + ".csv"
    csv_filename = os.path.join(sub_folder_path, csv_filename)
    df.to_csv(csv_filename, index=False)

print("e")
# df = process_log_file(log_fileprint("e")
