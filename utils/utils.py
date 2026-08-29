import json

def read_json(file):
    with open(file) as f:
        return json.load(f)

def load_config():
    return read_json("config.json")

def save_guilds(guilds):
    with open('data/guilds.json', 'w') as f:
        f.write(json.dumps(guilds))

def load_guilds():
    return read_json("data/guilds.json")

    