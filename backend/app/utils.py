import json
from pathlib import Path




def load_json(path):
with open(path,'r') as f:
return json.load(f)




def save_json(path, obj):
Path(path).parent.mkdir(parents=True, exist_ok=True)
with open(path,'w') as f:
json.dump(obj, f, indent=2)