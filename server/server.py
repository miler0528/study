import os
from datetime import datetime

from flask import Flask, request
import pandas as pd



app = Flask(__name__)
csv_file = 'data.csv'

@app.route('/data', methods=['POST'])
def data():
    data = request.json
    t = datetime.today()
    if not os.path.isfile(csv_file):
        df = pd.DataFrame(columns=['datetime','temperature', 'humidity'])
        df.to_csv(csv_file, index=False)

    with open(csv_file, mode='a', newline='') as file:
        df = pd.DataFrame([data])
        df['datetime'] = t
        df = df[['datetime','temperature', 'humidity']]
        df.to_csv(file, header=False, index=False, mode = "false")

        return 'Data received', 200
    return 'Data received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)