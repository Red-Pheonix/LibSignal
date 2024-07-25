from utils.runner import Runner
import argparse
import os


# parseargs
parser = argparse.ArgumentParser(description='Run Experiment')
parser.add_argument('--thread_num', type=int, default=4, help='number of threads')  # used in cityflow
parser.add_argument('--ngpu', type=str, default="-1", help='gpu to be used')  # choose gpu card
parser.add_argument('--prefix', type=str, default='test', help="the number of prefix in this running process")
parser.add_argument('--seed', type=int, default=None, help="seed for pytorch backend")
parser.add_argument('--debug', type=bool, default=True)
parser.add_argument('--interface', type=str, default="libsumo", choices=['libsumo','traci'], help="interface type") # libsumo(fast) or traci(slow)
parser.add_argument('--delay_type', type=str, default="apx", choices=['apx','real'], help="method of calculating delay") # apx(approximate) or real
parser.add_argument('--faulty_sensor', action=argparse.BooleanOptionalAction)
parser.set_defaults(faulty_sensor=False)

parser.add_argument('-t', '--task', type=str, default="tsc", help="task type to run")
parser.add_argument('-a', '--agent', type=str, default="dqn", help="agent type of agents in RL environment")
parser.add_argument('-w', '--world', type=str, default="cityflow", choices=['cityflow','sumo'], help="simulator type")
parser.add_argument('-n', '--network', type=str, default="cityflow1x1", help="network name")
parser.add_argument('-d', '--dataset', type=str, default='onfly', help='type of dataset in training process')
parser.add_argument('-s', '--save_dir', type=str, default='', help='path where models are saved')
parser.add_argument('-sp', '--save_prefix', type=str, default='final', help='prefix of saved model weights')
parser.add_argument('-l', '--load_dir', type=str, default='', help='path where models are loaded before training')
parser.add_argument('-lp', '--load_prefix', type=str, default='final', help='prefix of loaded model weights')

args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = args.ngpu

if __name__ == '__main__':
    test = Runner(**vars(args))
    test.run()