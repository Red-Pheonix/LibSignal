import pandas as pd
from lxml import etree
import os
import glob


# Read the CSV file
# csv_file_path = 'robust grid4x4 experiments/dqn/morning_1_queue.csv'

def conver_queue_to_edge(csv_file_path, output_file):

    df = pd.read_csv(csv_file_path)

    # Group the DataFrame by timestep intervals
    df['interval'] = df['timestep'] // 360  # Assuming 3600 seconds interval
    df['interval'] = df['interval'].astype(int)
    intervals = df.groupby('interval')

    # Create the root element of the XML
    root = etree.Element('meandata')

    # Iterate over each interval group to construct the XML
    for interval, group in intervals:
        interval_elem = etree.SubElement(
            root,
            'interval',
            begin=str(interval * 360 - 360),
            end=str((interval) * 360),
            id="1"
        )

        edges = group.groupby('lane_id')

        for lane_id, edge_group in edges:
            edge_id = lane_id.split('_')[0] + '_' + lane_id.split('_')[1]
            edge_elem = interval_elem.find(f".//edge[@id='{edge_id}']")
            if edge_elem is None:
                edge_elem = etree.SubElement(interval_elem, 'edge', id=edge_id)

            for _, row in edge_group.iterrows():
                etree.SubElement(
                    edge_elem,
                    'lane',
                    id=row['lane_id'],
                    queueing_time=f"{row['queueing_time']:.2f}",
                    queueing_length=f"{row['queueing_length']:.2f}"
                )
        
    # convert lane data to edge data
    for edge in root.findall(f".//edge"):
        queue_times = []
        queue_lengths = []
        for lane in edge.findall(".//lane"):
            queue_times.append(float(lane.attrib['queueing_time']))
            queue_lengths.append(float(lane.attrib['queueing_length']))
            edge.remove(lane)
            
        queueing_time = sum(queue_times) / len(queue_times)
        queueing_length = sum(queue_lengths) / len(queue_lengths)
        edge.set('queueing_time', f"{queueing_time:.2f}")
        edge.set('queueing_length', f"{queueing_length:.2f}")

    # Convert the XML tree to a string and print it
    xml_str = etree.tostring(root, pretty_print=True, encoding='UTF-8').decode('UTF-8')

    # Optionally, write the XML to a file
    with open(output_file, 'w') as xml_file:
        xml_file.write(xml_str)

folder_path = 'robust grid4x4 experiments/*/'
pattern = os.path.join(folder_path, '*queue.csv')
matching_files = glob.glob(pattern)

# Print the list of matching files
for filename in matching_files:
    print(f"Processing {filename}...")
    sub_folder_path = "/".join(filename.split("/")[:-1])
    edgedata_filename = filename.split("/")[-1].rstrip("queue.csv") + "edgedata.xml"
    edgedata_filename = os.path.join(sub_folder_path, edgedata_filename)
    conver_queue_to_edge(filename, edgedata_filename)