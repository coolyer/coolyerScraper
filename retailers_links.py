import json

def retailersFile():
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            enabled_retailers = [r for r in config['retailers'] if r['enabled']]
            if not enabled_retailers:
                print("All retailers are disabled. Please enable at least one retailer in the config.json file.")
                exit(1)
            retailers = {r['name']: r['url'] for r in enabled_retailers}
        return retailers
    except FileNotFoundError:
        print("Configuration file (config.json) is missing. This file should be included in the zip.")