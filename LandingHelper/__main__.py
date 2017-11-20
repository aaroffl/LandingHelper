import json
import core
with open('config.json') as config_data:
    config = json.load(config_data)
core.load(config);
core.run()