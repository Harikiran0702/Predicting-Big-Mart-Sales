# Predicting Big Mart Sales

An machine-learning web application. It estimates item sales from product and outlet attributes using a decision tree, with a Flask interface for individual predictions and CSV previews.

The project explores how historical retail data can inform sales estimates. It is a learning prototype, not a validated production forecasting system.

## Features

- Predict one item's `Item_Outlet_Sales` from nine product/outlet inputs.
- Preview the first 100 rows of a CSV upload (maximum 2 MiB); files are not saved.
- Reproduce a separate 80/20 holdout evaluation from the included training data.
- Inspect the original exploratory notebook, retained as academic history.

## Technology

Python 3.12, Flask/Jinja, pandas, NumPy, and scikit-learn. The original interface uses bundled Bootstrap, Bootstrap Icons, Animate.css and Swiper assets with the EstateAgency template.

## Setup

Run these commands from the repository root with Python 3.12 installed:

```sh
git clone https://github.com/Harikiran0702/Predicting-Big-Mart-Sales.git
cd Predicting-Big-Mart-Sales
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Then install and start:

```sh
python -m pip install -r requirements.txt
python app.py
```


## Usage

1. Open **Prediction** and choose the product and outlet categories.
2. Enter positive item weight and MRP, visibility between 0 and 1, and a whole outlet establishment year. For example: Dairy, 9.3, 249.8092, 0.016047301, Low Fat, 1999, Medium, Tier 1, Supermarket Type1.
3. Select **Predict** to see estimated sales in the dataset's target units. No currency conversion is performed.
4. Open **Upload** to preview a CSV, such as `model/Test.csv`. An `Id` column is not required.

The first prediction trains a model from `model/Train.csv` and caches it in memory for that process. Restart after changing the training data. Zero visibility is treated as missing, consistent with the original analysis. No external or legacy pickle is loaded.

## Model and evaluation

The implementation preserves the original nine features, category codes, `DecisionTreeRegressor(max_depth=20)`, and cube-root target transformation, reversing that transformation for displayed sales. It adds a fixed random seed and training-only mean/mode imputation. Retraining and corrected preprocessing can change predictions from the old saved model.

```sh
python evaluate.py
python -m unittest discover -s tests -v
python -m pip check
```

Evaluation uses an 80/20 random split with seed 0. Preprocessing and the tree fit only the training split; MAE, RMSE and R² are reported on held-out rows in original sales units. The interactive demo separately trains on all available rows. Regression does not have an "accuracy percentage."

The old notebook fitted its final tree on the full dataset before scoring a subset. Its historical scores therefore contain training/evaluation overlap and should not be used as evidence of generalization. They are preserved, with a warning, in `docs/legacy-metrics.txt`. Static chart values were removed from the live interface.

## Structure

```text
app.py                    Flask routes, validation and CSV preview
sales_model.py            Data preparation and decision-tree pipeline
evaluate.py               Reproducible holdout evaluation
requirements.txt          Runtime dependencies
templates/                HTML pages
static/assets/            Original images, styles and third-party assets
model/Train.csv            Labeled training data
model/Test.csv             Original unlabeled dataset
model/Untitled1.ipynb      Historical exploratory notebook (outputs cleared)
data.csv, Test.csv         Original alternate CSV exports
tests/                    Automated application checks
docs/                     Audit notes and historical metrics
.github/workflows/        Automated checks
```

## Screenshots / demo

No hosted demo or verified screenshots are currently supplied. Future screenshots should show the actual prediction form and CSV preview; no sample image or result is presented as a measured outcome.

## Limitations and provenance

- A random row split does not test future periods or unseen outlets. Further validation is needed for practical use.
- Predictions are estimates from historical data, with no uncertainty interval or guarantee. Inputs outside the training distribution can be unreliable.
- Category codes are retained for continuity; their numeric ordering is an academic modeling choice, not a statement of category similarity.
- The original notebook is an archival record, not the supported setup path. It includes obsolete APIs such as `Ridge(normalize=True)` and old exploratory dependencies. Use the scripts above for a clean run.
- The datasets and images were already in the repository. Their original source and redistribution permissions have not been independently verified. This cleanup does not grant a new license.
- Third-party template notices are retained. See [EstateAgency](https://bootstrapmade.com/real-estate-agency-bootstrap-template/) and its [license terms](https://bootstrapmade.com/license/). Confirm applicable rights before redistribution or public deployment.
- Generated models, environment files, keys, virtual environments, caches and IDE files are ignored. Never upload confidential data to a publicly exposed demo.

Saved scikit-learn models are not supported across library versions; see the official [model persistence guidance](https://scikit-learn.org/stable/model_persistence.html). This project regenerates its model locally instead.
