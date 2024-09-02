import yaml
from pathlib import Path

# Load config file
my_path = Path(__file__).resolve()
config_path = my_path.parent/'config.yml'
with config_path.open() as config_file: config = yaml.safe_load(config_file)

# Dataset parameters
dataset_dir             = config['dataset']['dir']
subject_id              = config['dataset']['subject_id']

# sICA parameters
sic_candidate            = config['sica']['candidate']