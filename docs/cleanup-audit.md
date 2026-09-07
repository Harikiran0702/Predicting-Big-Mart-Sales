# Repository cleanup audit

Inspected the original single commit (`f1eb9d2`), application, templates, notebook code, tracked assets and CSV schemas. This remains the author's original bachelor's project, with a maintained local execution path.

## Changes

- Added a README describing purpose, implemented features, setup, usage, structure, provenance, screenshot status and limitations.
- Replaced unsupported legacy dependency pins with versions installed and tested on Python 3.12.10: Flask 3.1.3, NumPy 2.5.3, pandas 2.3.3 and scikit-learn 1.9.0. Removed matplotlib from runtime requirements because the app does not use it. Removed the malformed `runtime .txt` containing `python--3.8.13`.
- Replaced import-time pickle loading with local training cached on the first prediction. Removed both generated `dtrs.pkl` copies. Kept the nine feature/category mappings, depth-20 decision tree and cube-root sales target; added a deterministic seed and train-fitted imputation. Removed the unsupported Non-Edible form choice (code 2), which was not used in notebook training.
- Added separate holdout evaluation. Unlike the original notebook, it fits both imputation and model only on the training partition. Predictions may differ from the original pickle.
- Read prediction inputs by field name, not submission order; reject missing, nonnumeric, nonfinite, invalid category and out-of-range input. Keep fractional sales rather than truncating to an integer.
- Bound uploads to 2 MiB and previews to 100 rows. Handle missing/empty/invalid files, remove the mandatory `Id` column, and preserve HTML escaping. Uploads are not persisted.
- Removed the browser-only admin/admin login and its form; `/login` redirects to the demo upload page. This was a hard-coded demo credential, not real authentication. No replacement credential was added.
- Removed the fake training delay/success alert; the preview now links directly to prediction and explains its purpose.
- Corrected localhost-only form action and broken home, preview and missing asset links. Removed static chart values and unsupported performance claims from live pages; retained labeled historical metrics under `docs/legacy-metrics.txt`.
- Removed notebook checkpoints and cleared notebook outputs/execution counts while retaining all notebook source cells. The notebook remains historical and contains obsolete APIs; supported execution uses the new scripts.
- Added ignore rules for environments, secrets/key files, serialized models, generated outputs, caches and IDE files.
- Replaced the unused CodeSee integration (including its `pull_request_target` trigger and external secret dependency) with read-only Python test/evaluation CI.
- Added six application regression tests covering pages, predictions, field order, invalid input, CSV escaping, invalid files and upload limits.

## Retained intentionally

- `model/Train.csv`: 8,523 labeled rows; `model/Test.csv`: 5,681 unlabeled rows.
- `data.csv`: a 4,599-row historical export with an Id column; root `Test.csv`: seven encoded example rows. These are not duplicate files and are not used by the maintained training path.
- Original styling, images and vendored third-party distribution files/source maps remain to avoid an unrelated frontend migration. These are intentional static assets, not newly generated application build outputs. Their age and licensing require separate review before public deployment.
- No license was invented for the project, datasets or images.

## Security review

Checked tracked filenames and text in the initial commit and working tree for environment/key files, private key headers, AWS/GitHub token patterns and common secret assignments. The assignment matches in Bootstrap were `DATA_API_KEY = '.data-api'` event constants, not credentials. No actual service credentials or private keys were identified. The original demo login was removed. This pattern/manual review is not a guarantee that every possible secret format is absent. The existing commit history was not rewritten; the old demo login remains in that history.

## Validation

- Six unittest tests pass on Windows with Python 3.12.10.
- `python -m pip check` passes.
- All local href/src links on the rendered home, upload, prediction, chart and performance pages resolve without a 4xx/5xx response.
- `git diff --check` passes.
- Holdout: 6,818 training rows, 1,705 test rows; MAE 1085.2145, RMSE 1547.8268, R² 0.18145. These are measured original-sales-unit metrics for this run, not production guarantees or a time/outlet-based validation.
- No existing test/build/lint configuration was present. CI repeats dependency checks, tests and evaluation on Linux; its result is separate from local validation. Browser visual layout and full archival notebook execution were not tested.
