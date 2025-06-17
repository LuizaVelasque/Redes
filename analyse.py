import pandas as pd
import json

with open("results.json", "r") as f:
    dados = json.load(f)

valores = []
for item in dados["metrics"]["http_req_duration"]["values"].items():
    print(f"{item[0]}: {item[1]}")
