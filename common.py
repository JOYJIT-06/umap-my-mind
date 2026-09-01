
"""Shared configuration, marker genes, and helper functions. Every script (Colab notebook, Snakemake rules, Docker entrypoint) imports from here so the biology and thresholds are defined in exactly one place.
"""
import os
import yaml

MARKER_GENES = {
    "Excitatory neurons": ["Slc17a7", "Neurod6", "Neurod2", "Satb2"],
    "Inhibitory neurons": ["Gad1", "Gad2", "Pvalb", "Sst", "Vip"],
    "Astrocytes": ["Aqp4", "Gfap", "Slc1a3", "Aldh1l1"],
    "Oligodendrocytes": ["Mbp", "Plp1", "Mog", "Olig2"],
    "Microglia": ["Cx3cr1", "P2ry12", "C1qa", "Trem2"],
    "OPCs": ["Pdgfra", "Vcan", "Cspg4"],
    "Endothelial": ["Cldn5", "Pecam1", "Flt1"],
    "Pericytes": ["Pdgfrb", "Acta2", "Rgs5"],
}
NEURON_TYPES = ["Excitatory neurons", "Inhibitory neurons"]
GLIA_TYPES = ["Astrocytes", "Oligodendrocytes", "Microglia", "OPCs"]

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def ensure_dirs(cfg):
    os.makedirs(cfg["paths"]["figures_dir"], exist_ok=True)
    os.makedirs(cfg["paths"]["tables_dir"], exist_ok=True)
    os.makedirs("data", exist_ok=True)