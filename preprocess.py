
import sys
import scanpy as sc
import pandas as pd
import scrublet as scr
from common import load_config, ensure_dirs

def run_doublet_detection(adata, cfg):
    print("Running Scrublet for doublet detection...")
    scrub = scr.Scrublet(adata.X, expected_doublet_rate=cfg['qc']['expected_doublet_rate'])
    doublet_scores, predicted_doublets = scrub.scrub_doublets(min_counts=2, min_cells=3, n_prin_comps=30)
    adata.obs['doublet_score'] = doublet_scores
    adata.obs['predicted_doublet'] = predicted_doublets
    return adata

def run_qc_and_normalize(adata, cfg):
    qc = cfg["qc"]
    adata.var["mt"] = adata.var_names.str.startswith(qc["mt_prefix"])
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

    stats_log = []
    n_before = adata.n_obs

    # Fix 1: Filter doublets
    adata = adata[~adata.obs.predicted_doublet].copy()
    n_after_doublets = adata.n_obs

    sc.pp.filter_cells(adata, min_genes=qc["min_genes"])
    sc.pp.filter_genes(adata, min_cells=qc["min_cells"])
    adata = adata[adata.obs.pct_counts_mt < qc["mt_threshold"]].copy()
    n_final = adata.n_obs

    sc.pp.normalize_total(adata, target_sum=cfg["preprocessing"]["target_sum"])
    sc.pp.log1p(adata)

    stats = pd.DataFrame([{
        "cells_start": n_before,
        "doublets_removed": n_before - n_after_doublets,
        "cells_final": n_final,
        "genes_retained": adata.n_vars
    }])
    return adata, stats

if __name__ == "__main__":
    cfg = load_config()
    ensure_dirs(cfg)
    try:
        adata = sc.read_10x_h5(cfg["data"]["raw_h5"])
    except:
        adata = sc.read_10x_mtx(cfg["data"]["raw_mtx_dir"])
    adata.var_names_make_unique()

    adata = run_doublet_detection(adata, cfg)
    adata, stats = run_qc_and_normalize(adata, cfg)

    stats.to_csv(f"{cfg['paths']['tables_dir']}/qc_stats.csv", index=False)
    adata.write("data/adata_normalized.h5ad")
    print(f"Preprocess complete. Doublets removed: {stats['doublets_removed'].values[0]}")