"""
Génère les figures PCA 3D pour K-Means (k=3) et DBSCAN (3 groupes).
Ne modifie aucun notebook. Sauvegarde dans reports/figures/.
"""
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors

RANDOM_STATE = 42
SAMPLE_SIZE = 10_000

PROJECT_ROOT = Path(__file__).parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Charger X_scaled ──────────────────────────────────────────────────────
print("Chargement de X_scaled...")
X_scaled = pd.read_csv(PROCESSED_DIR / "X_scaled.csv")
features_path = PROCESSED_DIR / "X_scaled_features.csv"
if features_path.exists():
    feature_names = pd.read_csv(features_path)["feature"].tolist()
    if len(feature_names) == X_scaled.shape[1]:
        X_scaled.columns = feature_names
print(f"  {X_scaled.shape[0]:,} lignes × {X_scaled.shape[1]} features")

# ── 2. Reproduire l'échantillon exact de Part 2 (même RNG) ───────────────────
print("Reconstruction de l'échantillon 10 000 lignes...")
rng = np.random.RandomState(RANDOM_STATE)
shared_sample_idx = pd.read_csv(PROCESSED_DIR / "sample_index.csv").iloc[:, 0].astype(int).to_numpy()
subset_size = min(SAMPLE_SIZE, len(shared_sample_idx))
selected_positions = rng.choice(len(shared_sample_idx), size=subset_size, replace=False)
sample_idx = shared_sample_idx[selected_positions]
X_sample = X_scaled.iloc[sample_idx].values
print(f"  Échantillon : {X_sample.shape}")

# ── 3. K-Means k=3 ───────────────────────────────────────────────────────────
print("K-Means k=3...")
km3 = KMeans(n_clusters=3, init="k-means++", n_init=10, max_iter=300, random_state=RANDOM_STATE)
kmeans_labels = km3.fit_predict(X_sample)
print(f"  Tailles : {dict(zip(*np.unique(kmeans_labels, return_counts=True)))}")

# ── 4. DBSCAN → trouver une config avec ~3 clusters ──────────────────────────
print("Recherche DBSCAN avec 3 clusters...")
# Elbow method sur k-distance pour min_samples=40
min_samples = 40
nn = NearestNeighbors(n_neighbors=min_samples, n_jobs=-1)
nn.fit(X_sample)
kd_raw, _ = nn.kneighbors(X_sample)
kd_sorted = np.sort(kd_raw[:, -1])

n = len(kd_sorted)
x_norm = np.linspace(0, 1, n)
y_norm = (kd_sorted - kd_sorted.min()) / (kd_sorted.max() - kd_sorted.min())
perp = np.abs(y_norm - x_norm) / np.sqrt(2)
eps_elbow = float(kd_sorted[int(np.argmax(perp))])
print(f"  eps elbow : {eps_elbow:.4f}")

# Tester quelques eps autour de l'elbow pour trouver 3 clusters non-bruit
best_eps = None
best_labels = None
for eps_try in np.linspace(eps_elbow * 0.7, eps_elbow * 1.3, 20):
    lbl = DBSCAN(eps=eps_try, min_samples=min_samples, n_jobs=-1).fit_predict(X_sample)
    n_clust = len(set(lbl)) - (1 if -1 in lbl else 0)
    noise_pct = (lbl == -1).mean() * 100
    if n_clust == 3 and noise_pct < 60:
        best_eps = eps_try
        best_labels = lbl
        print(f"  Config retenue : eps={eps_try:.4f}, bruit={noise_pct:.1f}%")
        break

if best_labels is None:
    # fallback : eps qui donne le plus proche de 3 clusters
    best_n_diff = 999
    for eps_try in np.linspace(eps_elbow * 0.5, eps_elbow * 2.0, 40):
        lbl = DBSCAN(eps=eps_try, min_samples=min_samples, n_jobs=-1).fit_predict(X_sample)
        n_clust = len(set(lbl)) - (1 if -1 in lbl else 0)
        noise_pct = (lbl == -1).mean() * 100
        diff = abs(n_clust - 3)
        if diff < best_n_diff and noise_pct < 60:
            best_n_diff = diff
            best_eps = eps_try
            best_labels = lbl
    n_found = len(set(best_labels)) - (1 if -1 in best_labels else 0)
    print(f"  Fallback : eps={best_eps:.4f}, {n_found} clusters, bruit={(best_labels==-1).mean()*100:.1f}%")

dbscan_labels = best_labels
n_dbscan_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)

# ── 5. PCA 3D ────────────────────────────────────────────────────────────────
print("PCA 3D...")
pca3 = PCA(n_components=3, random_state=RANDOM_STATE)
X_3d = pca3.fit_transform(X_sample)
var = pca3.explained_variance_ratio_
print(f"  Variance expliquée : PC1={var[0]*100:.1f}%  PC2={var[1]*100:.1f}%  PC3={var[2]*100:.1f}%  total={sum(var)*100:.1f}%")

# ── 6. Figure K-Means 3D ─────────────────────────────────────────────────────
print("Figure K-Means 3D...")
COLORS_KM = ["#E41A1C", "#377EB8", "#4DAF4A"]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

for k, col in enumerate(COLORS_KM):
    mask = kmeans_labels == k
    ax.scatter(
        X_3d[mask, 0], X_3d[mask, 1], X_3d[mask, 2],
        s=6, alpha=0.4, color=col, label=f"Cluster {k}",
    )

ax.set_xlabel(f"PC1 ({var[0]*100:.1f}%)", labelpad=8)
ax.set_ylabel(f"PC2 ({var[1]*100:.1f}%)", labelpad=8)
ax.set_zlabel(f"PC3 ({var[2]*100:.1f}%)", labelpad=8)
ax.set_title("K-Means k=3 — PCA 3D", fontsize=13, fontweight="bold", pad=12)
ax.legend(markerscale=2.5, loc="upper left")

plt.tight_layout()
out_km = FIGURES_DIR / "02_pca_kmeans_k3_3d.png"
plt.savefig(out_km, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Sauvegardé : {out_km}")

# ── 7. Figure DBSCAN 3D ──────────────────────────────────────────────────────
print("Figure DBSCAN 3D...")
unique_labels = sorted(set(dbscan_labels))
COLORS_DB = ["#E41A1C", "#377EB8", "#4DAF4A", "#FF7F00", "#984EA3"]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

for label in unique_labels:
    mask = dbscan_labels == label
    if label == -1:
        ax.scatter(
            X_3d[mask, 0], X_3d[mask, 1], X_3d[mask, 2],
            s=4, alpha=0.15, color="lightgray", label="Bruit (-1)",
        )
    else:
        col = COLORS_DB[label % len(COLORS_DB)]
        ax.scatter(
            X_3d[mask, 0], X_3d[mask, 1], X_3d[mask, 2],
            s=6, alpha=0.5, color=col, label=f"Cluster {label}",
        )

noise_pct = (dbscan_labels == -1).mean() * 100
ax.set_xlabel(f"PC1 ({var[0]*100:.1f}%)", labelpad=8)
ax.set_ylabel(f"PC2 ({var[1]*100:.1f}%)", labelpad=8)
ax.set_zlabel(f"PC3 ({var[2]*100:.1f}%)", labelpad=8)
ax.set_title(
    f"DBSCAN {n_dbscan_clusters} clusters — PCA 3D\n(eps={best_eps:.2f}, min_samples={min_samples}, bruit={noise_pct:.1f}%)",
    fontsize=12, fontweight="bold", pad=12,
)
ax.legend(markerscale=2.5, loc="upper left")

plt.tight_layout()
out_db = FIGURES_DIR / "02_pca_dbscan_k3_3d.png"
plt.savefig(out_db, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Sauvegardé : {out_db}")

print("\nTerminé.")
