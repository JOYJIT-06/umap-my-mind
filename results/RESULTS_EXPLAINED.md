# Mouse Brain Single-Cell Analysis: A Non-Technical Guide

This document breaks down the single-cell RNA sequencing (scRNA-seq) results into everyday language, explaining what each chart shows and what it means for brain biology.

---

## Chapter 1: Sorting Healthy Cells (Quality Control)

Before analyzing brain function, we must filter out damaged cells and background noise.

* **`qc_violin_plots.png` & `qc_stats.csv`**:
  * **What it shows**: Three violin-shaped distribution plots displaying the number of active genes, total RNA count, and mitochondrial gene percentage per cell.
  * **Plain-English Meaning**: Imagine taking a census of a city, but needing to remove people who are ill or unresponsive. High mitochondrial RNA indicates a cell membrane ruptured during sample preparation. Cells exceeding 15% mitochondrial content were filtered out to ensure only live, healthy brain cells were analyzed.

---

## Chapter 2: Mapping the Brain Neighborhood (UMAP Plots)

Single-cell sequencing measures thousands of genes per cell. We compress this complex high-dimensional data into a 2D visual map.

* **`umap_clusters.png`**:
  * **What it shows**: A scatter plot where each dot represents an individual cell, colored by mathematical grouping (clusters 0 through 12).
  * **Plain-English Meaning**: Cells with similar genetic activity automatically land close to one another on the map, forming distinct "neighborhoods."

* **`umap_cell_types.png`**:
  * **What it shows**: The same UMAP map, but with biological names assigned to each cluster neighborhood.
  * **Plain-English Meaning**: This gives us our final census map, identifying where Excitatory Neurons, Inhibitory Neurons, Astrocytes, and OPCs reside.

---

## Chapter 3: The Brain Census & Cell Roles

* **`analysis_summary.txt` & `cluster_annotations.csv`**:
  * **Excitatory Neurons**: The "Go" signals of the brain. They send active electrical messages to trigger neighboring cells.
  * **Inhibitory Neurons**: The "Brakes" of the brain. They prevent over-excitation and maintain balanced neural circuits.
  * **Astrocytes**: The support crew. They provide nutrients, maintain the blood-brain barrier, and clean up excess chemical signals.
  * **OPCs (Oligodendrocyte Progenitor Cells)**: The insulation builders. They generate the protective coating (myelin) that wraps around neural wiring.

---

## Chapter 4: Genetic ID Badges (Marker Genes)

* **`marker_genes_dotplot.png` & `top_markers_per_cluster.png`**:
  * **What it shows**: Dot plots and heatmaps revealing which specific genes are switched "ON" in each cell group.
  * **Plain-English Meaning**: Every cell type wears a unique genetic uniform. For example, *Slc17a7* acts like a badge identifying Excitatory Neurons, while *Aqp4* identifies Astrocytes. These plots confirm that our automatic cell labeling accurately matched established biological identity markers.

---

## Chapter 5: Next Steps & Raw Data

* **`mouse_brain_processed.h5ad`**:
  * **What it is**: A self-contained digital archive holding all cell coordinates, gene expressions, and assigned labels. Scientists can open this file in Python or R to run deeper custom analyses.
