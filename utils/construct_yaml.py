import yaml

data = {'gpu': 'Tesla', 'restart': ["C:\Program Files\Fan Control\FanControl.exe", ]}
with open('../config.yaml', 'w') as f:
    yaml.dump(data, f)
