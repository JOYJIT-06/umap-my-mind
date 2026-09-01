
"""Rule: report
Builds the plain-text analysis summary: cell/gene totals, neuron vs.
glia composition, and per-cell-type top marker genes.
"""
import sys
import scanpy as sc

from common import load_config, NEURON_TYPES, GLIA_TYPES


def top_markers_by_type(adata, n=3):
    result = {}
    for cell_type in adata.obs["cell_type"].unique():
        clusters = adata.obs.loc[adata.obs["cell_type"] == cell_type, "leiden"].unique()
        genes = []
        for cl in clusters:
            genes += sc.get.rank_genes_groups_df(adata, group=cl)["names"].head(n).tolist()
        result[cell_type] = list(dict.fromkeys(genes))[:n]
    return result


if __name__ == "__main__":
    config_file = sys.argv[1] if (len(sys.argv) > 1 and not sys.argv[1].startswith("-f")) else "config.yaml"
    cfg = load_config(config_file)
    adata = sc.read_h5ad(cfg["paths"]["processed_h5ad"])

    total = adata.n_obs
    counts = adata.obs["cell_type"].value_counts()
    neuron_n = counts.reindex(NEURON_TYPES, fill_value=0).sum()
    glia_n = counts.reindex(GLIA_TYPES, fill_value=0).sum()
    other_n = total - neuron_n - glia_n
    top_markers = top_markers_by_type(adata)

    lines = [
        "MOUSE BRAIN scRNA-seq ANALYSIS SUMMARY",
        "=" * 50, "",
        f"Total cells analyzed: {total}",
        f"Total genes: {adata.n_vars}",
        f"Cell types found: {adata.obs['cell_type'].nunique()}", "",
        "BRAIN COMPOSITION:",
        f"  Neurons: {neuron_n} ({neuron_n/total*100:.1f}%)",
        f"  Glia:    {glia_n} ({glia_n/total*100:.1f}%)",
        f"  Other:   {other_n} ({other_n/total*100:.1f}%)", "",
        "CELL TYPE BREAKDOWN:",
    ]
    for cell_type, n in counts.items():
        lines.append(f"  {cell_type}: {n} cells ({n/total*100:.1f}%) "
                      f"| top markers: {', '.join(top_markers.get(cell_type, []))}")

    with open(f"{cfg['paths']['tables_dir']}/analysis_summary.txt", "w") as f:
        f.write("\n".join(lines))
    print("Report written.")