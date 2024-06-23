from lxml import etree
import pandas as pd
import os
import glob

queue_file = "robust grid4x4 experiments/dqn/morning_1_queue.xml"

# Parse the XML data from a file

def process_queue(queue_file):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(queue_file, parser)
    root = tree.getroot()

    # Extract data and store it in a list of dictionaries
    data = []
    for timestep in root.findall('data'):
        time = timestep.get('timestep')
        for lane in timestep.findall('.//lane'):
            lane_data = {
                'timestep': time,
                'lane_id': lane.get('id'),
                'queueing_time': lane.get('queueing_time'),
                'queueing_length': lane.get('queueing_length')
            }            
            lane_data['queueing_time'] = lane_data['queueing_time'] if lane_data['queueing_time'] else 0
            lane_data['queueing_length'] = lane_data['queueing_length'] if lane_data['queueing_length'] else 0
            data.append(lane_data)

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    df = df.dropna()
    
    df['timestep'] = df['timestep'].astype(float)
    df['queueing_time'] = df['queueing_time'].astype(float)
    df['queueing_length'] = df['queueing_length'].astype(float)

    df = df[~df['lane_id'].str.startswith(':')]

    df['interval'] = (df['timestep'] // 360).astype(int)

    dataframes = [(interval,group) for interval, group in df.groupby('interval')]
    ag_dataframes = []

    for interval,dataframe in dataframes:
        ag_df = dataframe[['lane_id','queueing_time', 'queueing_length']].groupby(['lane_id']).mean().reset_index()
        timestep = 360.0 * (interval+1)
        ag_df = ag_df.assign(timestep=timestep)
        
        # handle missing lanes
        missing_lanes = list(set(df['lane_id']) - set(ag_df['lane_id']))
        missing_rows = [{"lane_id": lane, "queueing_time": 0, "queueing_length": 0, "timestep": timestep} for lane in missing_lanes]
        ag_df = pd.concat([ag_df, pd.DataFrame(missing_rows)])
        ag_dataframes.append(ag_df)

    combined_df = pd.concat(ag_dataframes)
    combined_df = combined_df.sort_values(by=['lane_id', 'timestep'])
    
    return combined_df

# df = process_queue(queue_file)

folder_path = 'robust grid4x4 experiments/*/'
pattern = os.path.join(folder_path, '*queue.xml')
matching_files = glob.glob(pattern)

# Print the list of matching files
for filename in matching_files:
    print(f"Processing {filename}...")
    df = process_queue(filename)
    sub_folder_path = "/".join(filename.split("/")[:-1])
    csv_filename = filename.split("/")[-1].rstrip("xml") + "csv"
    csv_filename = os.path.join(sub_folder_path, csv_filename)
    df.to_csv(csv_filename, index=False)



# combined_df.to_csv("test.csv", index=False)
# print(df)
