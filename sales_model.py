"""Reproducible decision tree retaining the original nine features and target transform."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor

ROOT = Path(__file__).resolve().parent
FEATURES = ['Item_Type', 'Item_Weight', 'Item_MRP', 'Item_Visibility', 'Item_Fat_Content', 'Outlet_Establishment_Year', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
CATEGORIES = {
    'Item_Type': ['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 'Household', 'Baking Goods', 'Snack Foods', 'Frozen Foods', 'Breakfast', 'Health and Hygiene', 'Hard Drinks', 'Canned', 'Breads', 'Starchy Foods', 'Others', 'Seafood'],
    'Item_Fat_Content': ['Regular', 'Low Fat'],
    'Outlet_Size': ['Small', 'Medium', 'High'],
    'Outlet_Location_Type': ['Tier 1', 'Tier 2', 'Tier 3'],
    'Outlet_Type': ['Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3', 'Grocery Store'],
}

def load_data():
    data = pd.read_csv(ROOT / 'model' / 'Train.csv')
    x = data[FEATURES].copy()
    x['Item_Fat_Content'] = x['Item_Fat_Content'].replace({'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular'})
    for name, labels in CATEGORIES.items():
        if not x[name].dropna().isin(labels).all():
            raise ValueError(f'Unknown category in {name}')
        x[name] = x[name].map({label: i for i, label in enumerate(labels)})
    x['Item_Visibility'] = x['Item_Visibility'].replace(0, np.nan)
    return x, data['Item_Outlet_Sales']

def cube(values):
    return values ** 3

def new_model():
    numeric = [name for name in FEATURES if name not in CATEGORIES]
    preprocessing = ColumnTransformer([
        ('numeric', SimpleImputer(strategy='mean'), numeric),
        ('category', SimpleImputer(strategy='most_frequent'), list(CATEGORIES)),
    ])
    return make_pipeline(preprocessing, TransformedTargetRegressor(
        regressor=DecisionTreeRegressor(max_depth=20, random_state=0),
        func=np.cbrt, inverse_func=cube))

def train_model():
    x, y = load_data()
    return new_model().fit(x, y)
