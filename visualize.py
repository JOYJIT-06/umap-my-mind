
"""Rule: visualize
Generates every figure needed for the CV/portfolio write-up at 300 dpi,
then writes a touchfile so Snakemake can track completion without
depending on an exact, brittle list of filenames.
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scanpy as sc

from common import load_config, MARKER_GENES
def make_all_plots(adata, cfg):
    fig_dir = cfg["paths"]["figures_dir"]

    sc.pl.umap(adata, color="leiden", show=False, title="Clusters")
    plt.savefig(f"{fig_dir}/umap_clusters.png", dpi=300, bbox_inches="tight")
    plt.close()

    sc.pl.umap(adata, color="cell_type", show=False, legend_loc="on data",
               title="Mouse Brain Cell Types", frameon=False)
    plt.savefig(f"{fig_dir}/umap_cell_types.png", dpi=300, bbox_inches="tight")
    plt.close()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    sc.pl.violin(adata, ["n_genes_by_counts"], jitter=0.4, ax=axes[0], show=False)
    axes[0].set_title("Genes per Cell")
    sc.pl.violin(adata, ["total_counts"], jitter=0.4, ax=axes[1], show=False)
    axes[1].set_title("Total Counts per Cell")
    sc.pl.violin(adata, ["pct_counts_mt"], jitter=0.4, ax=axes[2], show=False)
    axes[2].set_title("Mitochondrial % per Cell")
    plt.tight_layout()
    plt.savefig(f"{fig_dir}/qc_violin_plots.png", dpi=300)
    plt.close(fig)

    qc_metrics = [m for m in ["n_genes_by_counts", "total_counts", "pct_counts_mt"] if m in adata.obs]
    if qc_metrics:
        sc.pl.umap(adata, color=qc_metrics, show=False)
        plt.savefig(f"{fig_dir}/umap_qc_metrics.png", dpi=300, bbox_inches="tight")
        plt.close()

    all_markers = list(dict.fromkeys(
        g for markers in MARKER_GENES.values() for g in markers if g in adata.var_names
    ))
    if all_markers:
        sc.pl.dotplot(adata, all_markers, groupby="cell_type", show=False,
                       title="Marker Genes per Cell Type")
        plt.savefig(f"{fig_dir}/marker_genes_dotplot.png", dpi=300, bbox_inches="tight")
        plt.close()

    sc.pl.rank_genes_groups(adata, n_genes=10, sharey=False, show=False)
    plt.savefig(f"{fig_dir}/top_markers_per_cluster.png", dpi=300, bbox_inches="tight")
    plt.close()

    first_cluster = adata.obs["leiden"].cat.categories[0]
    top_gene = sc.get.rank_genes_groups_df(adata, group=first_cluster)["names"].iloc[0]
    sc.pl.violin(adata, [top_gene], groupby="cell_type", rotation=90, show=False)
    plt.savefig(f"{fig_dir}/top_gene_first_cluster_violin.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    config_file = sys.argv[1] if (len(sys.argv) > 1 and not sys.argv[1].startswith("-f")) else "config.yaml"
    cfg = load_config(config_file)
    adata = sc.read_h5ad(cfg["paths"]["processed_h5ad"])
    make_all_plots(adata, cfg)
    with open(f"{cfg['paths']['figures_dir']}/.done", "w") as f:
        f.write("ok")
    print("All figures saved.")