"""Local educational demo. No authentication or persistent uploads."""
from functools import lru_cache
import math
import numpy as np
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from sales_model import CATEGORIES, FEATURES, train_model

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@lru_cache(maxsize=1)
def get_model():
    return train_model()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    if request.method == 'GET':
        return redirect(url_for('upload'))
    dataset = request.files.get('datasetfile')
    if not dataset or not dataset.filename.lower().endswith('.csv'):
        return render_template('upload.html', error='Choose a CSV file.'), 400
    try:
        df = pd.read_csv(dataset, nrows=100)
    except (ValueError, UnicodeError, pd.errors.ParserError):
        return render_template('upload.html', error='Unable to read this CSV file.'), 400
    return render_template('preview.html', df_view=df)

@app.errorhandler(413)
def too_large(error):
    return render_template('upload.html', error='Upload must be at most 2 MiB.'), 413

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        values = {name: float(request.form[name]) for name in FEATURES}
        if not all(math.isfinite(value) for value in values.values()):
            raise ValueError('Values must be finite numbers.')
        for name, labels in CATEGORIES.items():
            if values[name] not in range(len(labels)):
                raise ValueError(f'Choose a valid {name}.')
        if values['Item_Weight'] <= 0 or values['Item_MRP'] <= 0:
            raise ValueError('Weight and MRP must be positive.')
        if not 0 <= values['Item_Visibility'] <= 1:
            raise ValueError('Visibility must be between 0 and 1.')
        year = values['Outlet_Establishment_Year']
        if year != int(year) or not 1800 <= year <= 2100:
            raise ValueError('Enter a whole establishment year from 1800 to 2100.')
    except (KeyError, ValueError):
        return render_template('result.html', error='Invalid input. Check all fields, numeric ranges and category choices.'), 400
    if values['Item_Visibility'] == 0:
        values['Item_Visibility'] = np.nan
    prediction = get_model().predict(pd.DataFrame([values], columns=FEATURES))[0]
    return render_template('result.html', prediction_text=f'{prediction:,.2f}')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

if __name__ == '__main__':
    app.run()
