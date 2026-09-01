
import scanpy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from common import load_config, MARKER_GENES

def cluster_sweep(adata, cfg):
    c = cfg["clustering"]
    sc.pp.highly_variable_genes(adata, n_top_genes=cfg["preprocessing"]["n_top_genes"])
    adata_hvg = adata[:, adata.var.highly_variable].copy()
    sc.pp.scale(adata_hvg, max_value=cfg["preprocessing"]["scale_max_value"])

    # Fix 4: PCA & Elbow Plot
    sc.tl.pca(adata_hvg, n_comps=c["n_pca_comps"])
    sc.pl.pca_variance_ratio(adata_hvg, n_pcs=c["n_pca_comps"], show=False)
    plt.savefig(f"{cfg['paths']['figures_dir']}/pca_elbow_plot.png")
    plt.close()

    sc.pp.neighbors(adata_hvg, n_neighbors=c["n_neighbors"], n_pcs=c["n_pcs"])

    # Fix 2: Resolution Sweep
    best_res, best_score = 0.5, -1
    results = []
    for res in c["leiden_resolutions"]:
        sc.tl.leiden(adata_hvg, resolution=res, key_added=f"leiden_{res}")
        score = silhouette_score(adata_hvg.obsm["X_pca"][:, :c["n_pcs"]], adata_hvg.obs[f"leiden_{res}"])
        n_clusters = len(adata_hvg.obs[f"leiden_{res}"].unique())
        results.append({"resolution": res, "n_clusters": n_clusters, "silhouette": score})
        if score > best_score:
            best_score = score
            best_res = res

    pd.DataFrame(results).to_csv(f"{cfg['paths']['tables_dir']}/resolution_sweep.csv", index=False)

    # Apply best
    adata.obs["leiden"] = adata_hvg.obs[f"leiden_{best_res}"]
    adata.obsm["X_pca"] = adata_hvg.obsm["X_pca"]
    sc.pp.neighbors(adata, n_neighbors=c["n_neighbors"], n_pcs=c["n_pcs"])
    sc.tl.umap(adata)
    return adata

def annotate_scored(adata):
    # Fix 3: sc.tl.score_genes
    for ct, markers in MARKER_GENES.items():
        valid = [m for m in markers if m in adata.var_names]
        if valid: sc.tl.score_genes(adata, valid, score_name=f"score_{ct}")

    score_cols = [f"score_{ct}" for ct in MARKER_GENES.keys() if f"score_{ct}" in adata.obs.columns]
    cluster_map = {}
    for cl in adata.obs["leiden"].cat.categories:
        avg_scores = adata.obs.loc[adata.obs["leiden"] == cl, score_cols].mean()
        cluster_map[cl] = avg_scores.idxmax().replace("score_", "")

    adata.obs["cell_type"] = adata.obs["leiden"].map(cluster_map)
    return adata

if __name__ == "__main__":
    cfg = load_config()
    adata = sc.read_h5ad("data/adata_normalized.h5ad")
    adata = cluster_sweep(adata, cfg)
    sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")
    adata = annotate_scored(adata)
    adata.write(cfg["paths"]["processed_h5ad"])
    print("Clustering, Sweep, and Scoring complete.")