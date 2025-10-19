# 🧭 McA_RPB — Clustering & Visualization Toolkit

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

**McA_Vision** is a flexible and extensible **clustering and visualization toolkit** designed to support rapid data exploration, model interpretability, and presentation of clustering results.  

---

## ✨ Key Features
- ✅ Top-N sample filtering for focused analysis
- ✅ Hierarchical clustering (Ward) and PCA visualization
- ✅ Clustering evaluation using Silhouette, Davies-Bouldin, Calinski-Harabasz
- ✅ Six visualization outputs (metrics curve, PCA scatter, scores, heatmap, distribution, dendrogram)
- ✅🧪 SHAP feature importance analysis (multiple model types supported)

---

## ⚠ Important — CAS Numbers in Data

> **Please note:**  
> Due to the presence of **CAS numbers** in the dataset,  
> **do not open the CSV file with Microsoft Excel**.  
> Excel will automatically interpret some CAS numbers (e.g. `50-00-0`) as **dates**, which will irreversibly corrupt the data.

✅ Recommended tools:
- Text editors (VSCode, Sublime Text)  
- Python/Pandas (`pd.read_csv`)  
- IDEs or CLI tools that preserve raw CSV formatting

🚫 If you’ve already opened the file with Excel:  
please re-download the original CSV file.

---

## 📂 McA_Vision Project Structure
```
McA_Vision/
├─ data/                        # Example datasets
├─ src/
│  ├─ cluster_analyzer.py       # Core clustering engine
│  ├─ cluster.py                # Hierarchical clustering implementation
│  ├─ SHAP_Method.py            # SHAP interpretability pipeline
│  └─ ...
├─ static/
│  └─ results/
│     └─ clusters/              # Output figures and results
├─ notebooks/
│  └─ Train_Test_E-Val-10-fold-EN.ipynb   # Model training/evaluation notebook
├─ requirements.txt
├─ run.py
└─ README.md
```

---

## 🛠 Installation
```bash
# 1. (Optional) Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Basic Usage

### Command Line
```bash
python run.py 
```

### Python API
```python
import pandas as pd
from src.cluster_analyzer import ClusterAnalyzer

df = pd.read_csv("data/example.csv")
analyzer = ClusterAnalyzer(results_dir="static/results")

df_top = analyzer.filter_top_substances("data/example.csv", top_n=200)
result_df, csv_path, figs = analyzer.perform_clustering(df_top, n_clusters=3)
```

---

## 📊 Visualization Outputs

| Visualization            | File Name                    | Description |
|--------------------------|-------------------------------|-------------|
| Metrics Comparison       | `*_cluster_metrics.png`       | SC, DBI, CH, normalized curves |
| PCA Scatter Plot         | `*_pca_visualization.png`     | Cluster visualization in 2D |
| Cluster Score Bars       | `*_cluster_scores.png`        | Average score per cluster |
| Feature Heatmap          | `*_feature_heatmap.png`       | z-score cluster centers |
| Score Distribution       | `*_score_distribution.png`    | Sample scores by cluster |
| Dendrogram               | `*_dendrogram.png`            | Hierarchical tree structure |

---

## 🧰 Script Usage Guide

### `cluster.py` — Clustering Implementation
- Loads dataset, performs PCA, hierarchical clustering.
- Outputs evaluation metrics, dendrogram, and result CSV.
- **Run:** `python cluster.py` (edit file_path before running).

### `SHAP_Method.py` — Feature Importance
- Runs SHAP analysis for multiple model architectures.
- Outputs SHAP values and summary plots.
- **Run:** `python SHAP_Method.py` (ensure model weights exist).

### `Train_Test_E-Val-10-fold-EN.ipynb` — Training & Validation
- Jupyter notebook for model training, validation, and evaluation.
- **Run:** open with Jupyter or VSCode.

---

## 🧪 SHAP Analysis (Optional)
- Supports MLP, CNN, Attention, and hybrid variants.
- Generates:
  - SHAP value CSVs
  - Summary plots
  - Bar plots
  - Dependence plots (top 3 features per model)
- Output path: `results/shap_analysis/`

---

## ⚡ Advanced Options
- Font switching: English / Chinese (`SimHei`)  
- Adjustable number of clusters with evaluation curves
- High-resolution figure export (300 DPI)
- Easy integration with other clustering algorithms (e.g. DBSCAN, GMM)

---

## 📜 License
This project is licensed under the **MIT License**.  
See [LICENSE](./LICENSE) for details.

---
