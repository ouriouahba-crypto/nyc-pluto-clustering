# NYC PLUTO — Unsupervised Learning Project

## Description

This project applies unsupervised machine learning techniques to the NYC PLUTO dataset
(Primary Land Use Tax Lot Output), a comprehensive real estate dataset published by
New York City covering land use, zoning, and building characteristics across all five
boroughs. The goal is to discover meaningful clusters of properties and extract
actionable insights through dimensionality reduction and clustering algorithms.

---

## Project Phases

| # | Phase | Status |
|---|-------|--------|
| 1 | Exploratory Data Analysis (EDA) | **In progress** |
| 2 | Preprocessing & Feature Selection | Pending |
| 3 | Dimensionality Reduction (PCA / t-SNE / UMAP) | Pending |
| 4 | Clustering (K-Means, DBSCAN, Hierarchical) | Pending |
| 5 | Final Report | Pending |

**Current status: Phase 1 — EDA in progress**

---

## Repository Structure

```
NYC_PLUTO/
├── data/
│   ├── raw/                  # Original dataset (not tracked by git)
│   └── processed/            # Cleaned/transformed data (not tracked by git)
├── notebooks/
│   ├── 01_eda/
│   │   ├── 01_dataset_discovery.ipynb
│   │   ├── 02_visualizations_outliers.ipynb
│   │   └── 03_feature_engineering.ipynb
│   ├── 02_preprocessing/
│   │   └── preprocessing.ipynb
│   ├── 03_dimensionality_reduction/
│   │   └── pca.ipynb
│   └── 04_clustering/
│       └── clustering.ipynb
├── reports/
│   ├── figures/              # Exported charts and plots
│   └── team_notes.md         # Shared team decisions log
├── src/                      # Reusable Python modules (future phases)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd NYC_PLUTO
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch Jupyter:
   ```bash
   jupyter notebook
   ```

---

## Dataset

The NYC PLUTO dataset is published by the NYC Department of City Planning.

- **Official source:** [NYC Open Data — PLUTO](https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page)
- Download the latest version and place the file in `data/raw/`.
- The `data/` folder is excluded from git tracking (files are too large).

---

## Team Members

| Member | EDA Notebook |
|--------|-------------|
| [NAME 1] | `01_dataset_discovery.ipynb` — Basic info, feature understanding, missing values |
| [NAME 2] | `02_visualizations_outliers.ipynb` — Descriptive statistics, outliers, visualizations |
| [NAME 3] | `03_feature_engineering.ipynb` — Feature engineering, imbalanced data, EDA synthesis |

---

## Workflow

We follow a **branch-per-person** strategy to avoid conflicts:

1. Each team member works on their own branch named after their task:
   ```
   git checkout -b eda/dataset-discovery
   git checkout -b eda/visualizations-outliers
   git checkout -b eda/feature-engineering
   ```

2. When a notebook is ready for review, open a **Pull Request** to `main`.

3. At least one other team member reviews the PR before merging.

4. After merging, delete the feature branch and pull the latest `main`:
   ```bash
   git checkout main
   git pull origin main
   ```

All shared decisions and observations should be logged in [reports/team_notes.md](reports/team_notes.md).
