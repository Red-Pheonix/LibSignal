import task
import trainer
import agent
import dataset
from common.registry import Registry
from common import interface
from utils.logger import build_config, setup_logging
import logging
import os
import time

class Runner:
    def __init__(self,
                thread_num=4,
                ngpu=-1,
                prefix='test',
                seed=None,
                debug=True,
                interface="libsumo",
                delay_type="apx",
                task="tsc",
                agent="dqn",
                world="sumo",
                network="sumo1x3",
                dataset="onfly",
                save_dir="",
                save_prefix="final",
                load_dir="",
                load_prefix="final",
        ):
        """
        instantiate runner object with processed config and register config into Registry class
        """
        runner_config = {}
        runner_config['thread_num'] = thread_num
        runner_config['ngpu'] = ngpu
        runner_config['prefix'] = prefix
        runner_config['seed'] = seed
        runner_config['debug'] = debug
        runner_config['interface'] = interface
        runner_config['delay_type'] = delay_type
        runner_config['task'] = task
        runner_config['agent'] = agent
        runner_config['world'] = world
        runner_config['network'] = network
        runner_config['dataset'] = dataset
        runner_config['save_dir'] = save_dir
        runner_config['save_prefix'] = save_prefix
        runner_config['load_dir'] = load_dir
        runner_config['load_prefix'] = load_prefix

        self.config, self.duplicate_config = build_config(runner_config)
        self.config_registry()

    def config_registry(self):
        """
        Register config into Registry class
        """

        interface.Command_Setting_Interface(self.config)
        interface.Logger_param_Interface(self.config)  # register logger path
        interface.World_param_Interface(self.config)
        if self.config['model'].get('graphic', False):
            param = Registry.mapping['world_mapping']['setting'].param
            if self.config['command']['world'] in ['cityflow', 'sumo']:
                roadnet_path = param['dir'] + param['roadnetFile']
            else:
                roadnet_path = param['road_file_addr']
            interface.Graph_World_Interface(roadnet_path)  # register graphic parameters in Registry class
        interface.Logger_path_Interface(self.config)
        # make output dir if not exist
        if not os.path.exists(Registry.mapping['logger_mapping']['path'].path):
            os.makedirs(Registry.mapping['logger_mapping']['path'].path)
        interface.Trainer_param_Interface(self.config)
        interface.ModelAgent_param_Interface(self.config)

    def run(self):
        
        logging_level = logging.INFO
        if Registry.mapping['command_mapping']['setting'].param['debug']:
            logging_level = logging.DEBUG
        logger = setup_logging(logging_level)
        
        self.trainer = Registry.mapping['trainer_mapping']\
            [Registry.mapping['command_mapping']['setting'].param['task']](logger)
        self.task = Registry.mapping['task_mapping']\
            [Registry.mapping['command_mapping']['setting'].param['task']](self.trainer)
        start_time = time.time()
        self.task.run()
        logger.info(f"Total time taken: {time.time() - start_time}")