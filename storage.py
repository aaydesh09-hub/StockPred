import json
import os
import pandas as pd

def save_result(symbol, result, filename="final_data.json"):

    # Convert any DataFrames to JSONable dicts
    for k, v in result.items():
        if isinstance(v, pd.DataFrame):
            result[k] = v.to_dict(orient="records")

    # Load file if exists
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Update or add new entry
    data[symbol] = result

    # Write back
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)