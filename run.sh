# run sumo
python run.py --world sumo --network tempe --agent maxpressure
# python run.py --world sumo --network tempe --agent dqn
# python run.py --world sumo --network tempe --agent presslight
# python run.py --world sumo --network tempe --agent colight

# run cityflow
python run.py --world cityflow --network cityflow_tempe --agent maxpressure
python run.py --world cityflow --network cityflow_tempe --agent dqn
python run.py --world cityflow --network cityflow_tempe --agent presslight
python run.py --world cityflow --network cityflow_tempe --agent colight