# Team Notes and Decisions

## Phase 4 - Dimensionality Reduction & choosing k (Elie Hamou)

### PCA - `notebooks/03_dim_reduction/01_pca.ipynb`
- PCA applied to the standardized 16-feature matrix (`X_scaled.csv`).
- Reaching 90% of the variance needs **10 of the 16 components** -> only modest
  compression. The value of PCA here is decorrelation, mild denoising and 2D
  visualization, not strong compression.
- PC1 (24.5%) = residential vs commercial contrast; PC2 (19.2%) = residential
  development intensity; PC3 (10%) = large lots vs dense/old buildings.
- Silhouette (k=2) is essentially unchanged between full 16D (~0.47) and PCA-10D
  (~0.48): **PCA does not degrade clustering**.

### Choosing k - `notebooks/03_dim_reduction/02_choosing_k.ipynb`
- Independent re-examination of the k=2 choice (8 criteria, full 16D and PCA space),
  prompted by feedback that k=2 looked suspicious and should be re-tested after PCA.
- k=2 is the **best-separated, perfectly stable** split (silhouette + Calinski-Harabasz
  + ARI=1.00), and the ranking is **unchanged after PCA** -> it is not a silhouette
  artifact.
- However the **gap statistic -> k=1** and **GMM BIC -> large k**: the data is a
  **continuum** with one dominant gradient (residential vs non-residential), not a set
  of discrete islands.
- For a descriptive segmentation we compared **k=5 vs k=6** with four targeted tests:
  hierarchical nesting (k=6 nests perfectly into k=2, purity 1.00), per-cluster
  silhouette, **cross-algorithm robustness** (KMeans/GMM/Ward agree more at k=5,
  mean ARI ~0.44 vs ~0.35 at k=6), and centroid distances (at k=6 the two "house"
  clusters are near-duplicates, d~2.4 vs mean ~7).
- **Decision:** two-level segmentation. Report **k=2** as the dominant, statistically
  validated split (the backbone), and use **k=5** as the descriptive segmentation for
  interpretation. k=5 is the finest partition that stays distinct and reproducible across
  algorithms and nests cleanly inside k=2. The five typologies:
  ~53% single-family houses, ~32% dense older residential (walk-ups), ~8% mixed
  residential/commercial, ~6% commercial/public, ~1% industrial.
