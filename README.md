# Analyzing Robustness of ATCS-RL Systems
Adapted from [LibSignal](https://github.com/DaRL-LibSignal/LibSignal) for analyzing robustness of ATCS-RL systems. All the experiments were run on Ubuntu 22.04 using python 3.10.

## Scenarios

There are two scenarios for analyzing robustness, [Grid 4x4](https://github.com/Red-Pheonix/Grid-4x4-Scenario) and [Ingolstadt](https://github.com/Red-Pheonix/sumo_ingolstadt). Furthur details about the cases and the specific files used are explained in the respective repos.

## Models

The are five models used in this experiments is listed below:

#### Model Names

| Model  | model_name | Remarks |
| ------------- | ------------- | ------------- |
| IDQN  | `dqn`  | |
| MPLight  | `mplight`  | Not used in `Ingolstadt` scenario |
| CoLight  | `colight`  | |
| MaxPressure  | `maxpressure`  | Non-RL model|
| FixedTime  | `fixedtime`  | Non-RL model|

Note that for the `Ingolstadt` scenario, the `fixedtime` model of LibSignal was not used as noted in the paper. Rather, the output from directly running the `.sumocfg` file from the command line using `sumo` using the flag `--duration-log.statistics` was used.

## Initial Training

For each scenario, the RL models were trained on a training case before deploying the models for experiments. For the training, the models were trained for 200 episodes for the `Grid 4x4` scenario and 100 episodes for the `Ingolstadt` scenario. The default parameters in LibSignal were used for the initial training. After initial training was done, the model weights were saved using the `--save-dir` command line option. Here is the format for running the initial training:

```
python run.py --world sumo --network <case_name> --agent <model_name> --save_dir <save_file_location>
```

Here is an example of how to run the training for the `dqn` model for the `Grid 4x4` scenario.

```
python run.py --world sumo --network robust_grid_morning_6 --agent dqn --save_dir data/output_data/tsc/morning_1_random
```

Here are the cases in the initial training:

#### Case Names

| Cases  | case_name |
| ------------- | ------------- |
| Grid 4x4 Training Case  | `robust_grid_morning_6`  |
| Ingolstadt Training Case  | `ingo_train`  |

## Running the Tests

There are two primary outputs from the experiments:

1. Recovery Time
2. Average Non-zero Queue Length over each Timestep

### Recovery Time
For calculating recovery time, the `*DTL.log` and `*BRF.log` files generated in `data/output_data/tsc` is used for calculation. The raw log files are converted to `.csv` files using `convert_2_csv.py` and `convert_2_csv_brf.py`. Furthur data processing is done in the [Robust Data](https://github.com/Red-Pheonix/robust_data) repo.

For running a case, the format for running it is shown below:

```
python run.py --world sumo --network <case_name> --agent <model_name> --load_dir <save_file_location>
```

Here is an example of how to run the training for `dqn` model for the `Case 1` of the `Grid 4x4` scenario, assuming the model weights were saved in `data/output_data/tsc/morning_1_random`.

```
python run.py --world sumo --network robust_grid_morning_1 --agent dqn --load_dir data/output_data/tsc/morning_1_random
```

For the faulty sensor cases, the `--faulty_sensor` flag is turned on. For example, for `dqn` model for the `Case 8` of the `Grid 4x4` scenario, the command is like so:

```
python run.py --world sumo --network robust_grid_morning_1 --agent dqn --load_dir data/output_data/tsc/morning_1_random --faulty_sensor
```


Here are the cases used in calculating recovery time:

#### Case Names

| Cases  | case_name | Remarks|
| ------------- | ------------- | ------------- |
| Grid 4x4 Case 1  | `robust_grid_morning_1`  | |
| Grid 4x4 Case 2  | `robust_grid_morning_2`  | |
| Grid 4x4 Case 3  | `robust_grid_morning_3`  | |
| Grid 4x4 Case 4  | `robust_grid_morning_4`  | |
| Grid 4x4 Case 5  | `robust_grid_morning_5`  | |
| Grid 4x4 Case 6  | `robust_grid_evening_1`  | |
| Grid 4x4 Case 7  | `robust_grid_pse_1`  | |
| Grid 4x4 Case 8  | `robust_grid_morning_1`  | With `--faulty_sensor` flag on|
| Ingolstadt Case 1  | `ingo_morning`  | |
| Ingolstadt Case 2  | `ingo_noon`  | |
| Ingolstadt Case 3  | `ingo_evening`  | |
| Ingolstadt Case 4  | `ingo_morning`  | With `--faulty_sensor` flag on|

For all these cases, the configuration files found in `configs/tsc` was changed. The `epsilon` parameter was set to the minimum of respective models. And the `learning_start` parameter was set to 70 steps. The `train_mode` parameter was set to `True` and `test_mode` parameter was set to `False`. The cases ran for 20 episodes for `Grid 4x4` scenario and 10 episodes for `Ingolstadt` scenario.

### Queue Length over time
For queue length over time, when running a case, it generates a queue output from running `sumo` using `--queue-output` flag. `split_queue.py` is used for taking the large queue files and making them smaller to handle. Then files are converted to `.csv` files using `process_queue.py` and combined using `combine_csv.py`. Furthur data processing is done in the [Robust Data](https://github.com/Red-Pheonix/robust_data) repo.

The format for running cases is similar to what is shown in the recovery time section with one notable diffrence. All the cases were run only for 1 episode. Since the duration of these cases are longer than one hour, the `trainer.steps` in the `configs/tsc/base.yml` was set to their respective durations.

Here are the cases used for finding the queue length over each timestep:

#### Case Names

| Cases  | case_name | Remarks|
| ------------- | ------------- | ------------- |
| Grid 4x4 Case 9  | `robust_grid_combined`  | |
| Grid 4x4 Case 10  | `robust_grid_combined`  | With `--faulty_sensor` flag on|
| Ingolstadt Case 5  | `ingo_combined`  | |
| Ingolstadt Case 6  | `ingo_combined`  | With `--faulty_sensor` flag on|

## Making the Graphs
This is mainly done in the [Robust Data](https://github.com/Red-Pheonix/robust_data) repo. The `.csv` files generated is furthur analyzed and turned into graphs.