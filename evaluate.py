"""Holdout evaluation in original sales units; no saved model required."""
import json
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sales_model import load_data, new_model

def evaluate():
    x, y = load_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    prediction = new_model().fit(x_train, y_train).predict(x_test)
    return {'train_rows': len(x_train), 'test_rows': len(x_test),
            'MAE': mean_absolute_error(y_test, prediction),
            'RMSE': mean_squared_error(y_test, prediction) ** 0.5,
            'R2': r2_score(y_test, prediction)}

if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
