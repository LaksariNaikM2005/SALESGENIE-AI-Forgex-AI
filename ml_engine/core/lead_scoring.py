import pickle
import os

import yaml

yaml_path = os.path.join(os.path.dirname(__file__), '../config/signal_taxonomy.yaml')
with open(yaml_path, 'r') as file:
    taxonomy = yaml.safe_load(file)

print(f"Hot lead threshold is: {taxonomy['thresholds']['hot_lead']}")

ARTIFACT_PATH = os.path.join(os.path.dirname(__file__), '../artifacts/lead_scoring_model.pkl')

def predict_score(features: list) -> int:
    """Loads the compiled model and returns a 0-100 conversion probability."""
    if not os.path.exists(ARTIFACT_PATH):
        return 50 # Fallback for MVP if model isn't trained yet
        
    with open(ARTIFACT_PATH, 'rb') as f:
        model = pickle.load(f)
    probability = model.predict_proba(features)[0][1]
    return int(probability * 100)
    