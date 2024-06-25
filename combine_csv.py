import os
import glob
import pandas as pd

folder_path = "ingo_experiments/dqn/"
pattern = os.path.join(folder_path, "*combined_queue.csv")
matching_files = glob.glob(pattern)

dataframes = []

for filename in matching_files:
    df = pd.read_csv(filename)
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
combined_df = combined_df.sort_values(by=['lane_id', 'timestep'])
output_file = os.path.join(os.path.dirname(folder_path), "ingo_combined_queue.csv")

combined_df.to_csv(output_file, index=False)