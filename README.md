# Introduction
This repo is slightly modified from [LibSignal](https://github.com/DaRL-LibSignal/LibSignal) for the Tempe test project.
# Specifications
All the experiments were run in the following environment:

| Item             | Version         |
| ---------------- | --------------- |
| Operating System | Linux Mint 22.1 |
| Python Version   | 3.9.23          |
| SUMO Version     | 1.23.1          |
| Cityflow Version | 0.1             |

# Instructions
1. Follow the same installation instructions from the main repo, [LibSignal](https://github.com/DaRL-LibSignal/LibSignal)
2. There is one additional dependency compared to the original, run this:

```bash
pip install tqdm
```

Alternatively, you may install using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

3. Run the `run.sh` script. Wait for the results to come in. There are a total of 5 experiments. 1 for SUMO and the rest are from Cityflow. If more trials are needed modify the `run.sh` script as needed.

```bash
chmod +x run.sh
./run.sh
```

4. Wait for the results to come in. Grab the DTL log files from `data/output_data` and put it into the experiments folder. Refer to the `show.ipynb` notebook on this.
5. The `show.ipynb` notebook generates the plot and final metrics table. Run it.

# Notes
There are some minor modifications made in this repo compared to the original.
## SUMO Max Distance
This is a setting present in the SUMO world object. It is supposed to be the maximum distance from an intersection vehicles can be detected. 

```python
@Registry.register_world('sumo')
class World(object):
def __init__(self, sumo_config, placeholder=0, **kwargs):
...
self.max_distance = 10000 # default is 200
```

The main reason for this change is in Cityflow, there are no maximum distance for detecting vehicles. At least, it's not implemented in the Cityflow world object. To make the two versions closer to each other, the max distance was set to a high value.

## Load Model
There is a hacky checkpoint feature added. To enable loading from saved weights, go to the  `configs/tsc/base.yml` file. Set the `load_model` variable to `True`. The new `load_model_episode` variable also needs to be the set to the episode number of the saved model.

## Tempe Network
The cityflow network and flow file is taken from here: [Tempe Cityflow Network](https://github.com/Red-Pheonix/utdf2gmns/tree/convert_2_cityflow/datasets/data_Tempe_network/utdf_to_cityflow). The file is converted using the converter in the same repo.