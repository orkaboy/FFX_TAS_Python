import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# TODO: Make this be set by an argument instead
CONFIG_FILE_PATH = "config.yaml"

# TODO: It's not ideal to open this file many times over, but also not a huge problem
def open_config():
    # Open the config file and parse the yaml contents
    try:
        with open(CONFIG_FILE_PATH) as config_file:
            try:
                return yaml.load(config_file, Loader=Loader)
            except Exception as E:
                print("Failed to parse config file: ", E)
                return {}
    except Exception as E:
        print("Unable to load config file: ", CONFIG_FILE_PATH, E)
        return {}
