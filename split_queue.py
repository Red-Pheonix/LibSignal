from lxml import etree
import os

# Define the maximum number of data elements per file
max_elements_per_file = 360

# Initialize variables
file_count = 0
element_count = 0
data_to_keep = []

# Function to create and save a new XML file
def save_to_file(data_elements, file_count, input_file):
    output_dir = os.path.dirname(input_file)
    new_root = etree.Element('queue-export', attrib={
        '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/queue_file.xsd'
    })

    for data in data_elements:
        new_root.append(data)

    new_tree = etree.ElementTree(new_root)
    input_file_name = os.path.basename(input_file)
    new_filename = input_file_name.rstrip('.xml') + f'_{file_count}.xml'
    output_file = os.path.join(output_dir, new_filename)
    new_tree.write(output_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    for element in data_elements:
        element.clear()


queue_file = 'ingo_experiments/dqn/ingo_morning_queue.xml'
# Use iterparse to go through the large XML file
for event, element in etree.iterparse(queue_file, events=('end',), tag='data', recover=True):
    # if lanes is not None and len(lanes):
    data_to_keep.append(element)
    element_count += 1

    # If the number of collected elements reaches the maximum, save to a new file
    if element_count >= max_elements_per_file:
        file_count += 1
        save_to_file(data_to_keep, file_count, queue_file)
        data_to_keep = []
        element_count = 0

# Save any remaining data elements to a new file
if data_to_keep:
    file_count += 1
    save_to_file(data_to_keep, file_count)
