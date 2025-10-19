# 🧭 McA_RPB— Clustering & Visualization Toolkit 

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

McA_Vision is an extensible **clustering and visualization solution** designed to help researchers **quickly explore, analyze, and present data distributions and clustering results**.

McA_Vision 是一个可扩展的 **聚类分析与可视化工具**，帮助科研人员快速、直观地探索数据分布并输出聚类结果。

---

## ✨ Key Features 主要功能
- ✅ Top-N 样本筛选，聚焦重点数据
- 🧠 支持层次聚类（Ward）与 KMeans 聚类
- 📊 PCA 降维 + 聚类可视化
- 🧪 内置多种聚类评估指标：Silhouette、Davies-Bouldin、Calinski-Harabasz
- 📈 可视化输出（PCA、热图、指标曲线、树状图等）
- 🈳 默认英文界面，可选中文字体（SimHei）
- ⚡ 轻量、开箱即用，可自由扩展算法

---

## ⚠ Important Notice about CAS Numbers  
### ⚠ CAS 号 Excel 自动格式化风险提醒

> **Please note / 请注意：**  
> Due to the presence of **CAS numbers** in the data, **do not open the CSV file directly with Microsoft Excel**.  
> Excel will automatically interpret certain CAS numbers (e.g., `50-00-0`) as **dates**, causing irreversible data corruption.  
>
> **由于数据中存在 CAS 号，请勿直接使用 Microsoft Excel 打开 CSV 文件。**  
> Excel 会自动将某些 CAS 号（如 `50-00-0`）识别为“日期”，从而造成数据被不可逆修改。

✅ Recommended 建议使用：
- 文本编辑器（VSCode、Sublime Text）  
- Python/Pandas (`pd.read_csv`)  
- 支持 CSV 原始格式的 IDE 或命令行工具

🚫 如果你已经用 Excel 打开过文件，请 **重新下载原始文件** 后再进行分析。

---

## 📂 Project Structure 项目结构
```
McA_Vision/
├─ data/                      # 示例数据
├─ src/
│  ├─ cluster_analyzer.py     # 核心聚类模块 (Hierarchical or KMeans)
│  └─ ...
├─ static/
│  └─ results/
│     └─ clusters/            # 聚类结果与可视化图像输出目录
├─ requirements.txt
├─ run.py                     # 命令行入口
└─ README.md
```

---

## 🛠 Installation 安装
```bash
# 1. 创建虚拟环境（可选）
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scriptsctivate

# 2. 安装依赖
pip install -r requirements.txt
```

---

## 🚀 Usage 使用方法

### Command Line 命令行
```bash
python run.py --csv data/example.csv --algo hier --n_clusters 3
```

### Python API
```python
import pandas as pd
from src.cluster_analyzer import ClusterAnalyzer

df = pd.read_csv("data/example.csv")
an = ClusterAnalyzer(results_dir="static/results")

df_top = an.filter_top_substances("data/example.csv", top_n=200)
res_df, csv_path, figs = an.perform_clustering(df_top, n_clusters=3)
print(csv_path)
print(figs)
```

---

## 📊 Visualization Outputs 可视化输出

| Visualization 图表类型 | File Name 文件名 | Description 描述 |
|------------------------|------------------|-------------------|
| Metrics Comparison 聚类效果评估 | `*_cluster_metrics.png` | Silhouette、DBI、CH 及归一化曲线 |
| PCA Scatter Plot 聚类散点图 | `*_pca_visualization.png` | 聚类二维分布 |
| Cluster Scores 簇均值柱状图 | `*_cluster_scores.png` | 各簇平均评估得分 |
| Feature Heatmap 特征热图 | `*_feature_heatmap.png` | 聚类中心特征 z-score |
| Score Distribution 得分分布 | `*_score_distribution.png` | 簇内样本得分分布 |
| Dendrogram 树状图 | `*_dendrogram.png` | Ward 层次聚类结构 |

---

## 📝 Note 说明
`MCA_Vision.zip` provides an **extensible clustering visualization solution** to help you quickly and easily explore and present data distributions and clustering results.  
`cluster.py` is the final clustering implementation script, allowing you to freely customize the analysis workflow according to your specific needs.  

MCA_Vision.zip 提供了一个 **可扩展的聚类可视化解决方案**，帮助你快速、便捷地探索并展示数据分布与聚类结果。  
`cluster.py` 是最终的聚类实现脚本，支持根据你的实际需求自由定制分析流程。

For implementation details not covered in this guide, please feel free to **contact us anytime** with any questions.  
如本指南未涵盖具体实现细节，欢迎随时联系我们。

---

## 📜 License 许可证
This project is licensed under the **[MIT license](https://github.com/XimuCloud/McA_RPB#MIT-1-ov-file)**.  

---
