import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist

# Enable Chinese/chemical labels (e.g., H2O -> H₂O)
def format_label(label):
    return re.sub(r"(\d+)", r"$_{\1}$", label)

# Load dataset
file_path = 'XXXX.csv'  # choose the best csv
data_df = pd.read_csv(file_path)

# Extract and format chemical ID labels
id_labels = data_df['id'].apply(format_label).tolist()

# Remove irrelevant columns
columns_to_remove = ['cas', 'id', 'evaluation_score']
data_cleaned = data_df.drop(columns=columns_to_remove)

# Feature matrix
X = data_cleaned.values

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA (2D for visualization)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Hierarchical clustering on PCA-reduced data
Z = linkage(X_pca, method='ward', optimal_ordering=True)

# Evaluate different numbers of clusters
range_n_clusters = [2, 3, 4, 5, 6]
sc_scores, db_scores, ch_scores = [], [], []

for k in range_n_clusters:
    labels = fcluster(Z, k, criterion='maxclust')
    if len(np.unique(labels)) < 2:
        sc_scores.append(np.nan)
        db_scores.append(np.nan)
        ch_scores.append(np.nan)
        continue
    sc_scores.append(silhouette_score(X_pca, labels))
    db_scores.append(davies_bouldin_score(X_pca, labels))
    ch_scores.append(calinski_harabasz_score(X_pca, labels))

# Plot evaluation metrics
fig, axs = plt.subplots(2, 2, figsize=(20, 16))

# Subplot (a): Silhouette
axs[0, 0].bar(range_n_clusters, sc_scores, color='#43A3EF')
axs[0, 0].set_title('Silhouette', fontsize=20, weight='bold')
axs[0, 0].set_xlabel('Number of Clusters', fontsize=18)
axs[0, 0].set_ylabel('Silhouette Score', fontsize=18)
axs[0, 0].grid(alpha=0.2)
axs[0, 0].text(0.05, 0.99, '(a)', transform=axs[0, 0].transAxes, fontsize=16, weight='bold')

# Subplot (b): Davies-Bouldin
axs[0, 1].bar(range_n_clusters, db_scores, color='#EF767B')
axs[0, 1].set_title('Davies-Bouldin', fontsize=20, weight='bold')
axs[0, 1].set_xlabel('Number of Clusters', fontsize=18)
axs[0, 1].set_ylabel('Davies-Bouldin Index', fontsize=18)
axs[0, 1].grid(alpha=0.2)
axs[0, 1].text(0.05, 0.99, '(b)', transform=axs[0, 1].transAxes, fontsize=16, weight='bold')

# Subplot (c): Calinski-Harabasz
axs[1, 0].plot(range_n_clusters, ch_scores, marker='o', linestyle='--', color='forestgreen')
axs[1, 0].set_title('Calinski-Harabasz', fontsize=20, weight='bold')
axs[1, 0].set_xlabel('Number of Clusters', fontsize=18)
axs[1, 0].set_ylabel('Calinski-Harabasz Score', fontsize=18)
axs[1, 0].grid(alpha=0.2)
axs[1, 0].text(0.05, 0.99, '(c)', transform=axs[1, 0].transAxes, fontsize=16, weight='bold')

# Subplot (d): Combined (normalized)
sc_min, sc_max = min(sc_scores), max(sc_scores)
db_min, db_max = min(db_scores), max(db_scores)
ch_min, ch_max = min(ch_scores), max(ch_scores)

norm_sc = [(x - sc_min)/(sc_max - sc_min) for x in sc_scores]
norm_db = [1 - (x - db_min)/(db_max - db_min) for x in db_scores]
norm_ch = [(x - ch_min)/(ch_max - ch_min) for x in ch_scores]

axs[1, 1].plot(range_n_clusters, norm_sc, 'o--', label='Silhouette (norm)', color='blue')
axs[1, 1].plot(range_n_clusters, norm_db, 's--', label='Davies-Bouldin (1-norm)', color='red')
axs[1, 1].plot(range_n_clusters, norm_ch, 'd--', label='Calinski-Harabasz (norm)', color='green')
axs[1, 1].set_title('Combined (Normalized)', fontsize=20, weight='bold')
axs[1, 1].set_xlabel('Number of Clusters', fontsize=18)
axs[1, 1].set_ylabel('Normalized Score', fontsize=18)
axs[1, 1].legend()
axs[1, 1].grid(alpha=0.2)
axs[1, 1].text(0.05, 0.99, '(d)', transform=axs[1, 1].transAxes, fontsize=16, weight='bold')

plt.subplots_adjust(hspace=0.25, wspace=0.21)
plt.savefig('Cluster_Comparison_Metrics.tiff', dpi=300, format='tiff', bbox_inches='tight')
plt.show()

# Weight combination scores
def compute_combined_scores(weights, sc, db, ch):
    return [
        weights['sc'] * sc[i] + weights['db'] * db[i] + weights['ch'] * ch[i]
        for i in range(len(sc))
    ]

weights_list = [
    {'sc': 0.4, 'db': 0.3, 'ch': 0.3},
    {'sc': 0.3, 'db': 0.4, 'ch': 0.3},
    {'sc': 0.3, 'db': 0.3, 'ch': 0.4},
]

for idx, weights in enumerate(weights_list, 1):
    combined_scores = compute_combined_scores(weights, norm_sc, norm_db, norm_ch)
    best_k = range_n_clusters[np.argmax(combined_scores)]
    print(f"\n=== Weight Set {idx} ({weights}) ===")
    print("Clusters | SC(norm) | DB(1-norm) | CH(norm) | Combined")
    for i, k in enumerate(range_n_clusters):
        print(f"{k:<8} {norm_sc[i]:>9.4f} {norm_db[i]:>11.4f} {norm_ch[i]:>10.4f} {combined_scores[i]:>10.4f}")
    print(f"Best k = {best_k}, score = {max(combined_scores):.4f}")

# Final clustering with a fixed distance threshold
distance_threshold = 3
clusters = fcluster(Z, distance_threshold, criterion='distance')
data_df['Cluster'] = clusters

# Dendrogram
plt.figure(figsize=(16, 12))
dendrogram(Z, labels=id_labels, leaf_rotation=90, leaf_font_size=10,
           color_threshold=distance_threshold, above_threshold_color='blue')
plt.xticks(rotation=25, fontsize=14)
plt.yticks(fontsize=20)
plt.xlabel('Pollutants', fontsize=22)
plt.ylabel('Inter-Group Distance (IGD)', fontsize=22)
plt.savefig('Hierarchical_Dendrogram.tiff', dpi=350, format='tiff')
plt.show()

# Print statistics per cluster
for cluster_num, group in data_df.groupby('Cluster'):
    print(f"\nCluster {cluster_num}:")
    for _, row in group[['id', 'evaluation_score']].iterrows():
        print(f"ID: {row['id']}, evaluation_score: {row['evaluation_score']}")
    print(f"Stats -> Min: {group['evaluation_score'].min()}, Max: {group['evaluation_score'].max()}, "
          f"Mean: {group['evaluation_score'].mean():.4f}, Var: {group['evaluation_score'].var():.4f}")

# Save output
output_file_path = 'Clustered_Data_With_Scores.csv'
data_df.to_csv(output_file_path, index=False)
print(f"Clustering results saved to '{output_file_path}'")
